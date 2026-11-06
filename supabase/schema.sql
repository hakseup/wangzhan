create extension if not exists pgcrypto with schema extensions;
create schema if not exists noix_private;
revoke all on schema noix_private from public,anon,authenticated;
grant usage on schema noix_private to authenticated;
create table noix_private.admin_emails(email text primary key);
alter table noix_private.admin_emails enable row level security;
insert into noix_private.admin_emails values ('meilinheyhey@outlook.com');
create table public.noix_access(user_id uuid primary key references auth.users on delete cascade,expires_at timestamptz);
create table public.noix_codes(code_hash text primary key,label text not null,days integer not null check(days between 0 and 3650),used_by uuid references auth.users,used_at timestamptz);
create index noix_codes_used_by_idx on public.noix_codes(used_by);
create table public.noix_progress(user_id uuid primary key references auth.users on delete cascade,revision bigint not null,state jsonb not null,updated_at timestamptz not null default now());
create table public.noix_notices(id uuid primary key default gen_random_uuid(),title text not null check(length(title) between 1 and 150),body text not null check(length(body) between 1 and 10000),published_at timestamptz not null default now());
create index noix_notices_published_idx on public.noix_notices(published_at desc);
create table public.noix_settings(key text primary key,value jsonb not null);
alter table public.noix_access enable row level security;
alter table public.noix_codes enable row level security;
alter table public.noix_progress enable row level security;
alter table public.noix_notices enable row level security;
alter table public.noix_settings enable row level security;
create function noix_private.verified() returns boolean language sql stable security definer set search_path='' as $$
 select auth.uid() is not null and exists(select 1 from auth.users u join auth.sessions s on s.user_id=u.id where u.id=auth.uid() and u.email_confirmed_at is not null and s.id=(auth.jwt()->>'session_id')::uuid);
$$;
create function noix_private.is_admin() returns boolean language sql stable security definer set search_path='' as $$
 select noix_private.verified() and exists(select 1 from auth.users u join noix_private.admin_emails a on lower(u.email)=a.email where u.id=auth.uid());
$$;
create function noix_private.has_access() returns boolean language sql stable security definer set search_path='' as $$
 select noix_private.verified() and (noix_private.is_admin() or exists(select 1 from public.noix_access where user_id=auth.uid() and (expires_at is null or expires_at>now())));
$$;
create policy access_read on public.noix_access for select to authenticated using(user_id=(select auth.uid()));
create policy progress_read on public.noix_progress for select to authenticated using(user_id=(select auth.uid()) and (select noix_private.verified()));
create policy notices_read on public.noix_notices for select to anon,authenticated using(true);
create policy settings_read on public.noix_settings for select to anon,authenticated using(key='release');
create policy notices_admin on public.noix_notices for all to authenticated using((select noix_private.is_admin())) with check((select noix_private.is_admin()));
create policy settings_admin on public.noix_settings for all to authenticated using((select noix_private.is_admin())) with check((select noix_private.is_admin()));
create function noix_private.redeem(raw_code text) returns void language plpgsql security definer set search_path='' as $$
declare c public.noix_codes; expiry timestamptz;
begin
 if not noix_private.verified() then raise exception 'Verified login required'; end if;
 select * into c from public.noix_codes where code_hash=encode(extensions.digest(upper(regexp_replace(raw_code,'\s','','g')),'sha256'),'hex') for update;
 if not found or c.used_by is not null then raise exception 'Invalid or used code'; end if;
 perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended('access:'||auth.uid()::text,0));
 select expires_at into expiry from public.noix_access where user_id=auth.uid();
 if c.days=0 or (found and expiry is null) then expiry:=null; else expiry:=greatest(coalesce(expiry,now()),now())+make_interval(days=>c.days); end if;
 insert into public.noix_access values(auth.uid(),expiry) on conflict(user_id) do update set expires_at=excluded.expires_at;
 update public.noix_codes set used_by=auth.uid(),used_at=now() where code_hash=c.code_hash;
end; $$;
create function noix_private.save_progress(expected_revision bigint,new_state jsonb) returns bigint language plpgsql security definer set search_path='' as $$
declare rev bigint;
begin
 if not noix_private.verified() then raise exception 'Verified login required'; end if;
 if jsonb_typeof(new_state) is distinct from 'object' or (new_state->>'version') is distinct from '1' or pg_column_size(new_state)>4000000 then raise exception 'Invalid state'; end if;
 perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended('progress:'||auth.uid()::text,0));
 select revision into rev from public.noix_progress where user_id=auth.uid(); rev:=coalesce(rev,0);
 if rev<>expected_revision then raise exception using errcode='40001',message='Progress conflict'; end if;
 insert into public.noix_progress values(auth.uid(),rev+1,new_state,now()) on conflict(user_id) do update set revision=excluded.revision,state=excluded.state,updated_at=excluded.updated_at;
 return rev+1;
end; $$;
create function noix_private.generate_codes(quantity integer,valid_days integer) returns jsonb language plpgsql security definer set search_path='' as $$
declare output jsonb:='[]'; raw text; i integer;
begin
 if not noix_private.is_admin() then raise exception 'Administrator required'; end if;
 if quantity is null or quantity<1 or quantity>100 or valid_days is null or valid_days<0 or valid_days>3650 then raise exception 'Invalid code configuration'; end if;
 for i in 1..quantity loop
  raw:='NOIX-'||upper(encode(extensions.gen_random_bytes(12),'hex'));
  insert into public.noix_codes values(encode(extensions.digest(raw,'sha256'),'hex'),left(raw,10)||'…',valid_days,null,null);
  output:=output||jsonb_build_array(raw);
 end loop;return output;
end; $$;
create function public.noix_session() returns jsonb language sql stable security invoker set search_path='' as $$
 select jsonb_build_object('admin',noix_private.is_admin(),'entitled',noix_private.has_access(),'expires_at',(select expires_at from public.noix_access where user_id=auth.uid()));
$$;
create function public.noix_redeem(raw_code text) returns void language sql security invoker set search_path='' as $$select noix_private.redeem(raw_code);$$;
create function public.noix_save_progress(expected_revision bigint,new_state jsonb) returns bigint language sql security invoker set search_path='' as $$select noix_private.save_progress(expected_revision,new_state);$$;
create function public.noix_generate_codes(quantity integer,valid_days integer) returns jsonb language sql security invoker set search_path='' as $$select noix_private.generate_codes(quantity,valid_days);$$;
revoke all on all functions in schema noix_private from public,anon,authenticated;
grant execute on all functions in schema noix_private to authenticated;
revoke all on function public.noix_session(),public.noix_redeem(text),public.noix_save_progress(bigint,jsonb),public.noix_generate_codes(integer,integer) from public,anon;
grant execute on function public.noix_session(),public.noix_redeem(text),public.noix_save_progress(bigint,jsonb),public.noix_generate_codes(integer,integer) to authenticated;
grant select on public.noix_access,public.noix_progress to authenticated;
grant select on public.noix_notices,public.noix_settings to anon,authenticated;
grant insert,update,delete on public.noix_notices,public.noix_settings to authenticated;
revoke all on public.noix_codes from anon,authenticated;
insert into storage.buckets(id,name,public) values('noix-private','noix-private',false) on conflict(id) do nothing;
create policy noix_storage_read on storage.objects for select to authenticated using(bucket_id='noix-private' and (select noix_private.has_access()));

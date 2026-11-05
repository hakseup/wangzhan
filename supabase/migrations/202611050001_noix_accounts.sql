-- Preparation only: apply through the authorized Supabase project migration flow.
create extension if not exists pgcrypto with schema extensions;
create table public.noix_admins(email text primary key);
alter table public.noix_admins enable row level security;
insert into public.noix_admins values('meilinheyhey@outlook.com') on conflict do nothing;
create or replace function public.noix_is_admin() returns boolean language sql stable security definer set search_path=pg_catalog,public as $$
 select exists(select 1 from auth.users u join public.noix_admins a on lower(a.email)=lower(u.email) where u.id=auth.uid() and u.email_confirmed_at is not null);
$$;
create table public.noix_access(user_id uuid primary key references auth.users on delete cascade, expires_at timestamptz);
create or replace function public.noix_has_access() returns boolean language sql stable security definer set search_path=pg_catalog,public as $$
 select public.noix_is_admin() or exists(select 1 from public.noix_access where user_id=auth.uid() and (expires_at is null or expires_at>now()));
$$;
create table public.noix_codes(code_hash text primary key,label text not null,days integer not null check(days between 0 and 3650),used_by uuid references auth.users,used_at timestamptz);
create table public.noix_progress(user_id uuid primary key references auth.users on delete cascade,revision bigint not null default 0,state jsonb not null,updated_at timestamptz not null default now());
create table public.noix_notices(id uuid primary key default gen_random_uuid(),title text not null check(length(title) between 1 and 150),body text not null check(length(body) between 1 and 10000),published_at timestamptz not null default now());
create table public.noix_settings(key text primary key,value jsonb not null);
alter table public.noix_access enable row level security;
alter table public.noix_codes enable row level security;
alter table public.noix_progress enable row level security;
alter table public.noix_notices enable row level security;
alter table public.noix_settings enable row level security;
create policy access_own_read on public.noix_access for select to authenticated using(user_id=auth.uid());
create policy progress_own_read on public.noix_progress for select to authenticated using(user_id=auth.uid() and public.noix_has_access());
create policy notices_read on public.noix_notices for select to anon,authenticated using(true);
create policy notices_admin on public.noix_notices for all to authenticated using(public.noix_is_admin()) with check(public.noix_is_admin());
create policy settings_read on public.noix_settings for select to anon,authenticated using(key='release');
create policy settings_admin on public.noix_settings for all to authenticated using(public.noix_is_admin()) with check(public.noix_is_admin());
create or replace function public.noix_redeem(raw_code text) returns void language plpgsql security definer set search_path=pg_catalog,public,extensions as $$
declare c public.noix_codes; expiry timestamptz;
begin
 if auth.uid() is null or not exists(select 1 from auth.users where id=auth.uid() and email_confirmed_at is not null) then raise exception 'Verified login required'; end if;
 select * into c from public.noix_codes where code_hash=encode(extensions.digest(upper(regexp_replace(raw_code,'\s','','g')),'sha256'),'hex') for update;
 if not found or c.used_by is not null then raise exception 'Invalid or used code'; end if;
 perform pg_advisory_xact_lock(hashtextextended('access:'||auth.uid()::text,0));
 select expires_at into expiry from public.noix_access where user_id=auth.uid();
 if c.days=0 or (found and expiry is null) then expiry:=null; else expiry:=greatest(coalesce(expiry,now()),now())+make_interval(days=>c.days); end if;
 insert into public.noix_access values(auth.uid(),expiry) on conflict(user_id) do update set expires_at=excluded.expires_at;
 update public.noix_codes set used_by=auth.uid(),used_at=now() where code_hash=c.code_hash;
end; $$;
create or replace function public.noix_save_progress(expected_revision bigint,new_state jsonb) returns bigint language plpgsql security definer set search_path=pg_catalog,public as $$
declare current_revision bigint;
begin
 if auth.uid() is null or not public.noix_has_access() then raise exception 'Access required'; end if;
 if jsonb_typeof(new_state)<>'object' or (new_state->>'version') is distinct from '1' or pg_column_size(new_state)>4000000 then raise exception 'Invalid state'; end if;
 perform pg_advisory_xact_lock(hashtextextended('progress:'||auth.uid()::text,0));
 select revision into current_revision from public.noix_progress where user_id=auth.uid(); current_revision:=coalesce(current_revision,0);
 if current_revision<>expected_revision then raise exception using errcode='40001',message='Progress conflict'; end if;
 insert into public.noix_progress values(auth.uid(),current_revision+1,new_state,now()) on conflict(user_id) do update set revision=excluded.revision,state=excluded.state,updated_at=excluded.updated_at;
 return current_revision+1;
end; $$;
revoke all on function public.noix_redeem(text),public.noix_save_progress(bigint,jsonb) from public,anon;
grant execute on function public.noix_redeem(text),public.noix_save_progress(bigint,jsonb) to authenticated;
-- Code generation and private asset delivery are implemented only after project authorization.

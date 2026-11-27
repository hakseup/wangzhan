-- 胡桃法语合并站点：为 B2 以外的题库（目前为 DALF C1）保存独立学习记录。
-- 只新增表和函数，不修改或删除现有的 noix_progress、noix_access、noix_codes 等数据。
-- 在 Supabase SQL Editor 中执行一次即可；重复执行是安全的。
create table if not exists public.noix_bank_progress(
 user_id uuid not null references auth.users on delete cascade,
 bank text not null check(bank in ('c1')),
 revision bigint not null,
 state jsonb not null,
 updated_at timestamptz not null default now(),
 primary key(user_id,bank)
);
alter table public.noix_bank_progress enable row level security;
drop policy if exists bank_progress_read on public.noix_bank_progress;
create policy bank_progress_read on public.noix_bank_progress for select to authenticated using(user_id=(select auth.uid()) and (select noix_private.verified()));
revoke all on public.noix_bank_progress from anon,authenticated;
grant select on public.noix_bank_progress to authenticated;

create or replace function noix_private.save_bank_progress(bank_id text,expected_revision bigint,new_state jsonb) returns jsonb language plpgsql security definer set search_path='' as $$
declare rev bigint; stamp timestamptz:=now();
begin
 if not noix_private.verified() then raise exception 'Verified login required'; end if;
 if bank_id is distinct from 'c1' then raise exception 'Unknown bank'; end if;
 if jsonb_typeof(new_state) is distinct from 'object' or pg_column_size(new_state)>4000000 then raise exception 'Invalid state'; end if;
 perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended('bank-progress:'||bank_id||':'||auth.uid()::text,0));
 select revision into rev from public.noix_bank_progress where user_id=auth.uid() and bank=bank_id; rev:=coalesce(rev,0);
 if rev<>expected_revision then raise exception using errcode='40001',message='Progress conflict'; end if;
 insert into public.noix_bank_progress values(auth.uid(),bank_id,rev+1,new_state,stamp)
  on conflict(user_id,bank) do update set revision=excluded.revision,state=excluded.state,updated_at=excluded.updated_at;
 return jsonb_build_object('revision',rev+1,'updated_at',stamp);
end; $$;
create or replace function public.noix_save_bank_progress(bank_id text,expected_revision bigint,new_state jsonb) returns jsonb language sql security invoker set search_path='' as $$select noix_private.save_bank_progress(bank_id,expected_revision,new_state);$$;
revoke all on function noix_private.save_bank_progress(text,bigint,jsonb) from public,anon,authenticated;
grant execute on function noix_private.save_bank_progress(text,bigint,jsonb) to authenticated;
revoke all on function public.noix_save_bank_progress(text,bigint,jsonb) from public,anon;
grant execute on function public.noix_save_bank_progress(text,bigint,jsonb) to authenticated;

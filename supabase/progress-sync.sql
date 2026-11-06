drop policy progress_read on public.noix_progress;
create policy progress_read on public.noix_progress for select to authenticated using(user_id=(select auth.uid()) and (select noix_private.verified()));
create or replace function noix_private.save_progress(expected_revision bigint,new_state jsonb) returns bigint language plpgsql security definer set search_path='' as $$
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

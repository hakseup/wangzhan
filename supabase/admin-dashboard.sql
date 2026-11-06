create function noix_private.dashboard() returns jsonb language plpgsql stable security definer set search_path='' as $$
begin
 if not noix_private.is_admin() then raise exception 'Administrator required'; end if;
 return jsonb_build_object('users',(select coalesce(jsonb_agg(jsonb_build_object('id',u.id,'email',u.email,'verified',u.email_confirmed_at is not null)),'[]') from (select id,email,email_confirmed_at from auth.users order by created_at desc limit 1000) u),'codes',(select coalesce(jsonb_agg(jsonb_build_object('label',label,'days',days,'used_by',used_by,'used_at',used_at)),'[]') from (select label,days,used_by,used_at from public.noix_codes order by used_at desc nulls first limit 1000) c));
end;$$;
create function public.noix_dashboard() returns jsonb language sql stable security invoker set search_path='' as $$select noix_private.dashboard();$$;
revoke all on function noix_private.dashboard(),public.noix_dashboard() from public,anon;
grant execute on function noix_private.dashboard(),public.noix_dashboard() to authenticated;
create policy codes_no_direct_access on public.noix_codes for all to anon,authenticated using(false) with check(false);
create policy admin_emails_no_direct_access on noix_private.admin_emails for all to anon,authenticated using(false) with check(false);

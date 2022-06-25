create type unit_type AS ENUM ('OFFER', 'CATEGORY');
create table if not exists public.shop_units (
id UUID not null,
name text not null,
parent_id UUID null,
price int null,
type unit_type,
update_date timestamp without time zone ,
primary key(id)
);
alter table public.shop_units add constraint fk_parent_category foreign key(parent_id) references shop_units(id) on delete cascade;
-- trigger to prevent changing shop unit type.
create or replace function prevent_type_change() returns trigger as $prevent_type_change$
begin
  if old.type != new.type then
    raise exception 'change type is not allowed';
  end if;

  if old.type = 'OFFER' and new.price is null then
    raise exception 'offer must have price';
  end if;

  if old.type = 'CATEGORY' and new.price is not null then
    raise exception 'category must have null price';
  end if;
  if old.type = 'OFFER' and new.price<0 then
    raise exception 'OFFER price must be positiv';
  end if;
  return new;
end;
$prevent_type_change$ language plpgsql;

create trigger prevent_type_change before update on public.shop_units
for each row execute procedure prevent_type_change();
create table if not exists public.statistic_shop_units (
id UUID not null,
name text not null,
parent_id UUID null,
price int null,
type unit_type,
update_date timestamp without time zone
);
alter table public.statistic_shop_units add constraint fk_statistic foreign key(id) references shop_units(id) on delete cascade;

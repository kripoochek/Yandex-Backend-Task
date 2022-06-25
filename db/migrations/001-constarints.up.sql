alter table public.shop_units add constraint fk_parent_category foreign key(parent_id) references shop_units(id) on delete cascade;
alter table public.statistic_shop_units add constraint fk_statistic foreign key(id) references shop_units(id) on delete cascade;

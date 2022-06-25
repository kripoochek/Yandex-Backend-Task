create type unit_type as ENUM ('OFFER', 'CATEGORY');
create table if not exists public.shop_units (
id UUID not null,
name varchar(100) not null,
parent_id UUID null,
price int null,
type unit_type,
update_date timestamp without time zone ,
primary key(id)
);
create table if not exists public.statistic_shop_units (
id UUID not null,
name varchar(100) not null,
parent_id UUID null,
price int null,
type unit_type,
update_date timestamp without time zone
);
-- creation of table
create table local_customers(
	first_name varchar(20),
	last_name varchar(20),
	id serial  primary key
);
-- selection operation
select * from local_customers;

-- insertion operation
insert into local_customers (first_name,last_name)
values ('amshu','rao');

-- bulk insertion
insert into local_customers (first_name,last_name)
values ('amshu','rao'),
('ketan','patel'),
('jack','konan')
;

-- where query
select * from local_customers 
where first_name = 'amshu';
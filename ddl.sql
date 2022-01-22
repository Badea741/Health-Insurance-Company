create database healthInsuranceCompany;
use healthInsuranceCompany;
create table plan
(
    plan_id      int auto_increment,
    customer_ssn varchar(20),
    type         varchar(7) not null check ( type in ('Basic', 'Premium', 'Golden') ),
    primary key (plan_id)
);


create table customer
(
    customer_ssn varchar(20),
    name         varchar(30) not null,
    plan_id      int, # used plan
    address      varchar(60) not null,
    age          int         not null check (age between 18 and 200),
    gender       varchar(6)  not null check ( gender in ('Male', 'Female') ),
    primary key (customer_ssn)
);


alter table plan
    add foreign key (customer_ssn) references customer (customer_ssn) on delete cascade;
# if the customer is deleted, delete all of his bought plans
alter table customer
    add foreign key (plan_id) references plan (plan_id) on delete cascade;
# has been modified 12:02 Tuesday
# if the plan operation is deleted -> customer doesn't benefit now, he can buy a plan later


create table dependent
(
    dependent_ssn varchar(20),
    customer_ssn  varchar(20),
    plan_id       int, # used plan
    name          varchar(30) not null,
    address       varchar(60) not null,
    age           int         not null check (age between 0 and 200),
    gender        varchar(6)  not null check ( gender in ('Male', 'Female') ),
    primary key (customer_ssn, dependent_ssn, name, address, age, gender),
    foreign key (customer_ssn) references customer (customer_ssn) on delete cascade,
    foreign key (plan_id) references plan (plan_id) on delete set null
);

create table hospital
(
    hospital_name varchar(30),
    address       varchar(60) not null,
    primary key (hospital_name)
);


create index plan_type on plan (type);
create table cover
(
    hospital_name varchar(30) not null,
    plan_type     varchar(7)  not null,
    primary key (hospital_name, plan_type),
    foreign key (hospital_name) references hospital (hospital_name) on delete cascade,
    foreign key (plan_type) references plan (type) on delete cascade
);
create table claim
(
    claim_id          int auto_increment,
    customer_ssn      varchar(20)   not null,
    plan_id           int, # beneficiary plan
    beneficiary_id    varchar(20)   not null,
    hospital_name     varchar(30)   not null,
    amount_of_expense numeric(7, 2) not null,
    expense_details   varchar(1024) not null,
    isResolved        varchar(8)    not null check ( isResolved in ('accepted', 'refused', 'pending') ) default 'pending',
    primary key (claim_id),
    foreign key (customer_ssn) references customer (customer_ssn) on delete cascade,
    foreign key (plan_id) references plan (plan_id) on delete cascade # modified 12:34 tuesday
);

insert into plan values (0, null, 'Basic');
insert into plan values (0, null, 'Premium');
insert into plan values (0, null, 'Golden');
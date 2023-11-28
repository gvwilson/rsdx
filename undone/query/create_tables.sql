drop table if exists staff;
create table staff(
       ident		integer primary key autoincrement,
       personal		text not null,
       family		text not null
);

drop table if exists experiment;
create table experiment(
       ident		integer primary key autoincrement,
       kind		text not null,
       started		text not null,
       ended		text
);

drop table if exists performed;
create table performed(
       staff		integer not null,
       experiment	integer not null,
       foreign key (staff) references staff(ident),
       foreign key (experiment) references experiment(ident)
);

drop table if exists plate;
create table plate(
       ident		integer primary key autoincrement,
       experiment	integer not null,
       upload_date	text not null,
       filename		text unique
);

drop table if exists invalidated;
create table invalidated(
       plate		integer not null,
       staff		integer not null,
       invalidate_date	text not null
);

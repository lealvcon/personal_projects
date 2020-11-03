--creating database
create database hospital;

use hospital;

--creating test table
create table test(ID smallint identity(1,1) primary key,
						codigo varchar(11),
						nombre varchar(30) not null,
						marca varchar(20),
						modelo varchar(20),
						serie varchar(15),
						funcional bit not null,
						observaciones varchar(100));
alter table test alter column marca varchar(25);
alter table test alter column modelo varchar(25);
--creating table escolares

create table escolares(ID smallint identity(1,1) primary key,
						codigo varchar(12),
						nombre varchar(30) not null,
						marca varchar(25),
						modelo varchar(25),
						serie varchar(15),
						funcional bit not null,
						observaciones varchar(100));

insert into test(codigo, nombre, marca, modelo, serie, funcional, observaciones)
		values(null, 'cama','HR','A', 'A120',1,null);

select * from escolares;
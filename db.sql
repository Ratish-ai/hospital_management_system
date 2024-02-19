create database hospital;

use hospital;

create table user_login
(
    user_id   int         not null,
    user_name varchar(20) not null,
    password  varchar(16) not null,
    constraint user_pk
        primary key (user_id)
);

create table user_role
(
    user_id   int         not null,
    user_role varchar(20) not null,
    constraint user_pk
        primary key (user_id)
);

create table doctor
(
    d_id   int         not null,
    d_name varchar(50) not null,
    specialist varchar(50) not null,
    time time not null,
    relieve varchar(1) not null,
    constraint doctor_pk
        primary key (d_id)
);

create table receptionist
(
    cl_id   int         not null,
    cl_name varchar(50) not null,
    relieve varchar(1)  not null,
    constraint receptionist_pk
        primary key (cl_id)
);

create table pharmacist
(
    pm_id   int         not null,
    pm_name varchar(50) not null,
    relieve varchar(1)  not null,
    constraint pharmacist_pk
        primary key (pm_id)
);

create table patient
(
    p_id   int         not null,
    p_name varchar(50) not null,
    height FLOAT       not null,
    weight float       not null,
    tok_no int         null,
    constraint patient_pk
        primary key (p_id)
);

create table queue
(
    t_no   int        not null,
    p_id   int        not null,
    d_id   int        not null,
    status varchar(1) not null,
    constraint queue_pk
        primary key (t_no),
    constraint queue_doctor_d_id_fk
        foreign key (d_id) references doctor (d_id),
    constraint queue_patient_p_id_fk
        foreign key (p_id) references patient (p_id)
);

alter table patient
    add constraint patient_queue_t_no_fk
        foreign key (tok_no) references queue (t_no);

create table medicine
(
    med_id    int         not null,
    med_name  varchar(50) not null,
    avail_qty int         not null,
    exp_date  date        not null,
    rate      float       not null,
    constraint medicine_pk
        primary key (med_id)
);

create table prescription
(
    pr_id  int not null,
    p_id   int not null,
    d_id   int not null,
    med_id int not null,
    qty    int not null,
    constraint prescription_pk
        primary key (pr_id),
    constraint prescription_doctor_d_id_fk
        foreign key (d_id) references doctor (d_id),
    constraint prescription_medicine_med_id_fk
        foreign key (med_id) references medicine (med_id),
    constraint prescription_patient_p_id_fk
        foreign key (p_id) references patient (p_id)
);

create table bill
(
    pr_id  int not null,
    med_id int not null,
    cost   int not null,
    constraint bill_medicine_med_id_fk
        foreign key (med_id) references medicine (med_id),
    constraint bill_prescription_pr_id_fk
        foreign key (pr_id) references prescription (pr_id)
);

create table prescription_queue
(
    pr_id  int        not null,
    status VARCHAR(1) not null,
    constraint prescription_queue_prescription_pr_id_fk
        foreign key (pr_id) references prescription (pr_id)
);

INSERT INTO hospital.user_login (user_id, user_name, password)
VALUES (1, 'admin', 'Admin@123');

INSERT INTO hospital.user_login (user_id, user_name, password)
VALUES (2, 'pharmacist', 'Pharmacist@123');

INSERT INTO hospital.user_login (user_id, user_name, password)
VALUES (3, 'doctor', 'Doctor@123');

INSERT INTO hospital.user_login (user_id, user_name, password)
VALUES (4, 'receptionist', 'Receptionist@123');

INSERT INTO hospital.user_login (user_id, user_name, password)
VALUES (5, 'patient', 'Patient@123');

INSERT INTO hospital.user_role (user_id, user_role)
VALUES (1, 'admin');

INSERT INTO hospital.user_role (user_id, user_role)
VALUES (2, 'pharmacist');

INSERT INTO hospital.user_role (user_id, user_role)
VALUES (3, 'doctor');

INSERT INTO hospital.user_role (user_id, user_role)
VALUES (4, 'receptionist');

INSERT INTO hospital.user_role (user_id, user_role)
VALUES (5, 'patient');

INSERT INTO hospital.receptionist (cl_id, cl_name, relieve)
VALUES (4, 'Receptionist', 'N');

INSERT INTO hospital.pharmacist (pm_id, pm_name, relieve)
VALUES (2, 'Pharmacist', 'N');

INSERT INTO hospital.patient (p_id, p_name, height, weight, tok_no)
VALUES (5, 'Patient', 170, 60, null);

alter table doctor
    change time from_time time not null;

alter table doctor
    add to_time time not null after from_time;

INSERT INTO hospital.doctor (d_id, d_name, specialist, from_time, to_time, relieve)
VALUES (3, 'Doctor', 'General', '10:00:00', '12:00:00', 'N');

alter table patient
    add mob_no VARCHAR(10) not null after weight;

UPDATE hospital.patient t
SET t.mob_no = '9876543210'
WHERE t.p_id = 5;
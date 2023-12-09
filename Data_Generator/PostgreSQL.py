import psycopg2
import random
from faker import Faker
from datetime import datetime as DT
from datetime import timedelta
from random import randrange

database_name = "university"
user_name = "postgres"
password = "12345"
host_ip = "localhost"
host_port ="5433"
try:
    connection = psycopg2.connect(
        database=database_name,
        user=user_name,
        password=password,
        host=host_ip,
        port=host_port
    )
    connection.autocommit = True
    cursor = connection.cursor()
except Exception as err:
    print("Error connect to Postgres",err)

#-------------------------------------------таблица Институт-----------------------------------------------

cursor.execute('''CREATE TABLE public.institute  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(256) COLLATE pg_catalog."default",
    CONSTRAINT institute_pkey PRIMARY KEY (id));''')

institutes_array = ['Институт кибербезопасности и цифровых технологий','Институт искусственного интеллекта']
institute_data = []
for i in range(len(institutes_array)):
    institute_data.append((institutes_array[i]))
institute_values = ", ".join(["(%s)"] * len(institute_data))

query_institute = (f"INSERT INTO public.institute (name) VALUES {institute_values}")
cursor.execute(query_institute, institute_data)

#-------------------------------------------таблица Кафедра-----------------------------------------------

cursor.execute('''CREATE TABLE public.kafedra  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    institute_id integer,
    CONSTRAINT kafedra_pkey PRIMARY KEY (id),
    CONSTRAINT kafedra_institute_id_fkey FOREIGN KEY (institute_id)
        REFERENCES public.institute (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION);''')

cafedras_array = ['КБ-2','КБ-3','КБ-5']

kafedra_data = []
get_array_institute_id = "SELECT array_agg(id) FROM public.institute"
cursor.execute(get_array_institute_id)
array_ids=cursor.fetchall()

for i in range(len(cafedras_array)):
    kafedra_data.append((cafedras_array[i], random.randint(1,2)))

kafedra_values = ", ".join(["%s"] * len(kafedra_data))
insert_query = (f"INSERT INTO public.kafedra (name,institute_id) VALUES {kafedra_values}")
cursor.execute(insert_query, kafedra_data)

#-------------------------------------------таблица Специальность-----------------------------------------------

cursor.execute('''CREATE TABLE public.specialnost  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    kafedra_id integer,
    CONSTRAINT specialnost_pkey PRIMARY KEY (id),
    CONSTRAINT specialnost_kafedra_id_fkey FOREIGN KEY (kafedra_id)
        REFERENCES public.kafedra (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
    );''')

specialnosts_array = ['Информационные системы и технологии','Информационная безопасность','Системный анализ и управление','Бизнес-информатика','Инноватика',]

specialnosts_data = []
get_array_kafedra_id = "SELECT array_agg(id) FROM public.kafedra"
cursor.execute(get_array_kafedra_id)
array_ids=cursor.fetchall()

for i in range(len(specialnosts_array)):
    specialnosts_data.append((specialnosts_array[i],  random.randint(1,3)))

specialnosts_values = ", ".join(["%s"] * len(specialnosts_data))
insert_query = (f"INSERT INTO public.specialnost (name,kafedra_id) VALUES {specialnosts_values}")
cursor.execute(insert_query, specialnosts_data)



#-------------------------------------------таблица Группа-----------------------------------------------

cursor.execute('''CREATE TABLE public.group  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    kurs integer,
    spec_id integer,
    CONSTRAINT group_pkey PRIMARY KEY (id),
    CONSTRAINT group_spec_id_fkey FOREIGN KEY (spec_id)
        REFERENCES public.specialnost (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
    );''')

groups_array = ['БСБО-01-20','БСБО-02-20','БСБО-03-20','БСБО-04-20','БСБО-05-20','БСБО-06-20']

group_data = []
get_array_spec_id = "SELECT array_agg(id) FROM public.specialnost"
cursor.execute(get_array_spec_id)
array_ids=cursor.fetchall()
for i in range(len(groups_array)):
    id = random.randint(0,len(array_ids[0][0])-1)
    spec_id = array_ids[0][0][id]
    group_data.append((groups_array[i], random.randint(1,4),spec_id))
group_values = ", ".join(["%s"] * len(group_data))

query_group = (f"INSERT INTO public.group (name,kurs,spec_id) VALUES {group_values}")
cursor.execute(query_group, group_data)

#-------------------------------------------таблица Студенты-----------------------------------------------

cursor.execute('''CREATE TABLE public.students
(
    id_stud_code integer NOT NULL,
    fio character varying COLLATE pg_catalog."default",
    group_id integer,
    CONSTRAINT student_pkey PRIMARY KEY (id_stud_code),
    CONSTRAINT student_group_id_fkey FOREIGN KEY (group_id)
        REFERENCES public."group" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')

kolvo_students = 100
def get_stud_code():
    return random.randint(1000000,9999999)

fake = Faker('ru_RU')

students_data = []

get_array_group_id = "SELECT array_agg(id) FROM public.group"
cursor.execute(get_array_group_id)
array_ids=cursor.fetchall()

for _ in range(kolvo_students):
    stud_code = get_stud_code()
    fio = fake.name()
    id = random.randint(0,len(array_ids[0][0])-1)
    group_id = array_ids[0][0][id]
    students_data.append((stud_code,fio, group_id))

studens_values = ", ".join(["%s"] * len(students_data))
insert_query = (f"INSERT INTO students (id_stud_code,fio,group_id) VALUES {studens_values}")
cursor.execute(insert_query, students_data)

#-------------------------------------------таблица Дисциплины-----------------------------------------------

cursor.execute('''CREATE TABLE public.disciplines
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    spec_id integer,
    check_type character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    tag boolean,
    technical character varying,
    CONSTRAINT disciplines_pkey PRIMARY KEY (id),
    CONSTRAINT disciplines_specialnost_id_fkey FOREIGN KEY (spec_id)
        REFERENCES public."specialnost" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')

disciplines_array = ['Облачные технологии', 'Алгоритмы компонентов цифровой обработки данных', 
'Методы системной инженерии', 'Проектирование архитектуры программного обеспечения',
'Технологии обеспечения информационной безопасности','Физкультура','Иностранный язык','Матанализ',
'Линейная алгебра','Криптография']

disciplines_data = []
for i in range(len(disciplines_array)):
    # name + check_type + description + tag
    disciplines_data.append((disciplines_array[i], random.randint(1,5),random.choice(['экзамен','зачет']), 'Описание курса',  random.choice([True, False]),random.choice(['', 'Требуется компьютерный класс'])))
disciplines_values = ", ".join(["%s"] * len(disciplines_data))

query_disciplines = (f"INSERT INTO public.disciplines (name,spec_id,check_type,description,tag,technical) VALUES {disciplines_values}")
cursor.execute(query_disciplines, disciplines_data)

#-------------------------------------------таблица Лекции-----------------------------------------------

cursor.execute('''CREATE TABLE public.lecture
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    discip_id integer,
    CONSTRAINT lecture_pkey PRIMARY KEY (id),
    CONSTRAINT lecture_discip_id_fkey FOREIGN KEY (discip_id)
        REFERENCES public.disciplines (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')
kolvo_lectures = 20
lecture_data = []

get_array_discip_id = "SELECT array_agg(id) FROM public.disciplines"
cursor.execute(get_array_discip_id)
array_discip_ids=cursor.fetchall()

for _ in range(kolvo_lectures):
    for i in range(len(array_discip_ids[0][0])):
        name = random.choice(['лекция','практика','лабораторная работа'])
        discip_id = array_discip_ids[0][0][i]
        #name + discip_id
        lecture_data.append((name, discip_id))

lecture_values = ", ".join(["%s"] * len(lecture_data))
insert_query = (f"INSERT INTO public.lecture (name,discip_id) VALUES {lecture_values}")
cursor.execute(insert_query, lecture_data)

#-------------------------------------------таблица Расписания-----------------------------------------------

cursor.execute('''CREATE TABLE public.\"timeTable\"  
    (
     id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    week integer,
    date date,
    teacher_fio character varying COLLATE pg_catalog."default",
    group_id integer,
    lecture_id integer,
    number_classroom character varying COLLATE pg_catalog."default",
    "time" time without time zone,
    CONSTRAINT "timeTable_pkey" PRIMARY KEY (id),
    CONSTRAINT "timeTable_group_id_fkey" FOREIGN KEY (group_id)
        REFERENCES public."group" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "timeTable_lecture_id_fkey" FOREIGN KEY (lecture_id)
        REFERENCES public.lecture (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
    );''')

timeTable_data = []

get_array_group_id = "SELECT array_agg(id) FROM public.group"
cursor.execute(get_array_group_id)
array_group_ids=cursor.fetchall()

get_array_lecture_id = "SELECT array_agg(id) FROM public.lecture"
cursor.execute(get_array_lecture_id)
array_lecture_ids=cursor.fetchall()

# 1 семестр 23 год
def get_random_date_1_22():
    start = DT.strptime('01.09.2023', '%d.%m.%Y')
    end = DT.strptime('29.12.2023', '%d.%m.%Y')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_date =  start + timedelta(seconds=random_second)
    random_date = str(random_date)
    return ' '.join(random_date.split(' ')[:-1])
# 2 семестр 23 год
def get_random_date_2_22():
    start = DT.strptime('09.01.2023', '%d.%m.%Y')
    end = DT.strptime('31.05.2023', '%d.%m.%Y')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_date =  start + timedelta(seconds=random_second)
    random_date = str(random_date)
    return ' '.join(random_date.split(' ')[:-1])
# 1 семестр 24 год
def get_random_date_1_23():
    start = DT.strptime('01.09.2024', '%d.%m.%Y')
    end = DT.strptime('29.12.2024', '%d.%m.%Y')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_date =  start + timedelta(seconds=random_second)
    random_date = str(random_date)
    return ' '.join(random_date.split(' ')[:-1])
# 2 семестр 24 год
def get_random_date_2_23():
    start = DT.strptime('09.01.2024', '%d.%m.%Y')
    end = DT.strptime('31.05.2024', '%d.%m.%Y')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_date =  start + timedelta(seconds=random_second)
    random_date = str(random_date)
    return ' '.join(random_date.split(' ')[:-1])

for lec in range(len(array_lecture_ids[0][0])):
    week = random.randint(1,16)
    date = random.choice( [get_random_date_1_22(),get_random_date_2_22(),get_random_date_1_23(),get_random_date_2_23()])
    time = random.choice(['9:00','10:40','12:40','14:20','16:20','18:00'])
    teacher_fio = fake.name()
    id = random.randint(0,len(array_group_ids[0][0])-1)
    group_id = array_group_ids[0][0][id]
    lecture_id = array_lecture_ids[0][0][lec]
    number_classroom = random.randint(100,400)
    
    timeTable_data.append((week,date,time,teacher_fio, group_id,lecture_id,number_classroom))

timeTable_values = ", ".join(["%s"] * len(timeTable_data))
insert_query = (f"INSERT INTO public.\"timeTable\" (week,date,time,teacher_fio, group_id,lecture_id,number_classroom) VALUES {timeTable_values}")
cursor.execute(insert_query, timeTable_data)

#-------------------------------------------таблица Посещения-----------------------------------------------

cursor.execute('''CREATE TABLE public.visits
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    student_id integer,
    visited boolean,
    "timeTable_id" integer,
    date_visit date,
    CONSTRAINT visits_pkey PRIMARY KEY (id),
    CONSTRAINT visits_student_id_fkey FOREIGN KEY (student_id)
        REFERENCES public.students (id_stud_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "visits_timeTable_id_fkey" FOREIGN KEY ("timeTable_id")
        REFERENCES public."timeTable" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')

visits_data = []

get_array_student_id = "SELECT array_agg(id_stud_code) FROM public.students"
cursor.execute(get_array_student_id)
array_student_ids=cursor.fetchall()

get_array_timeTable_id = "SELECT array_agg(id) FROM public.\"timeTable\""
cursor.execute(get_array_timeTable_id)
array_timeTable_ids=cursor.fetchall()

for st in range(len(array_student_ids[0][0])):
    for tt in range(len(array_timeTable_ids[0][0])):
        student_id = array_student_ids[0][0][st]
        visited = random.choice([True, False])
        timeTable_id = array_timeTable_ids[0][0][tt]
        date_visit = random.choice( [get_random_date_1_22(),get_random_date_2_22(),get_random_date_1_23(),get_random_date_2_23()])
        visits_data.append((student_id,visited,timeTable_id,date_visit))

visits_values = ", ".join(["%s"] * len(visits_data))
insert_query = (f"INSERT INTO public.visits (student_id,visited,\"timeTable_id\",date_visit) VALUES {visits_values}")
cursor.execute(insert_query, visits_data)

print("Postrges Данные добавлены")
import psycopg2
from neo4j import GraphDatabase

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


uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root12345"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

query_select_students = ("SELECT id_stud_code,fio,group_id FROM public.students;")
cursor.execute(query_select_students)
students=cursor.fetchall()

query_select_groups = ("SELECT id, name, spec_id FROM public.group;")
cursor.execute(query_select_groups)
groups=cursor.fetchall()

query_select_specialnost = ("SELECT id,name,kafedra_id FROM public.specialnost;")
cursor.execute(query_select_specialnost)
specialnosts=cursor.fetchall()

query_select_kafedra = ("SELECT id,name,institute_id FROM public.kafedra;")
cursor.execute(query_select_kafedra)
kafedras=cursor.fetchall()

query_select_institute = ("SELECT id,name FROM public.institute;")
cursor.execute(query_select_institute)
institutes=cursor.fetchall()

query_select_disciplines = ("SELECT id,name,spec_id, technical FROM public.disciplines;")
cursor.execute(query_select_disciplines)
disciplines=cursor.fetchall()

query_select_lecture = ("SELECT id, name,discip_id FROM public.lecture;")
cursor.execute(query_select_lecture)
lectures=cursor.fetchall()

query_select_timeTable = ("SELECT id, date, time, group_id, lecture_id FROM public.\"timeTable\";")
cursor.execute(query_select_timeTable)
timeTables=cursor.fetchall()


with graphDB_Driver.session() as neo_session:
    for st in range(len(students)):
        neo_session.run("CREATE (st:Student{id_stud_code:$id_stud_code, fio: $fio, group_id: $group_id})", id_stud_code = str(students[st][0]),fio = str(students[st][1]), group_id =  str(students[st][2]))
    for gr in range(len(groups)):
        neo_session.run("CREATE (g:Group{iid: $id, name: $name, spec_id: $spec_id})",  id = str(groups[gr][0]),name = str(groups[gr][1]),  spec_id = str(groups[gr][2]))
    for spec in range(len(specialnosts)):
        neo_session.run("CREATE (s:Specialnost{iid: $id, name: $name, kafedra_id: $kafedra_id})", id = str(specialnosts[spec][0]), name = str(specialnosts[spec][1]), kafedra_id = str(specialnosts[spec][2]))
    for kaf in range(len(kafedras)):
        neo_session.run("CREATE (k:Kafedra{iid: $id, name: $name, institute_id: $institute_id})", id = str(kafedras[kaf][0]), name = str(kafedras[kaf][1]), institute_id = str(kafedras[kaf][2]))
    for inst in range(len(institutes)):
        neo_session.run("CREATE (i:Institute{iid: $id, name: $name})", id = str(institutes[inst][0]), name = str(institutes[inst][1]))
    for disc in range(len(disciplines)):
        neo_session.run("CREATE (d:Disciplines{iid: $id,name: $name, spec_id:$spec_id, technical: $technical})", id = str(disciplines[disc][0]),name = str(disciplines[disc][1]),spec_id = str(disciplines[disc][2]), technical = str(disciplines[disc][3]))
    for lec in range(len(lectures)):
        neo_session.run("CREATE (l:Lecture{iid:$id, name: $name, discip_id: $discip_id})",id = str(lectures[lec][0]),name = str(lectures[lec][1]), discip_id = str(lectures[lec][2]))
    for tt in range(len(timeTables)):
        neo_session.run("CREATE (t:TimeTable{iid:$id, date: $date, time: $time, group_id: $group_id, lecture_id: $lecture_id})",id = str(timeTables[tt][0]),date = str(timeTables[tt][1]), time = str(timeTables[tt][2]), group_id = str(timeTables[tt][3]), lecture_id = str(timeTables[tt][4]))

    neo_session.run("MATCH (i:Institute),(k:Kafedra) WHERE i.iid = k.institute_id  CREATE (k)-[:kafedra_institute]->(i)")
    neo_session.run("MATCH (k:Kafedra),(s:Specialnost) WHERE k.iid = s.kafedra_id CREATE (s)-[:specialnost_kafedra]->(k)")
    neo_session.run("MATCH (s:Specialnost),(g:Group) WHERE s.iid = g.spec_id CREATE (g)-[:group_specialnost]->(s)")
    neo_session.run("MATCH (g:Group),(st:Student) WHERE g.iid = st.group_id CREATE (st)-[:group_student]->(g)")
    neo_session.run("MATCH (d:Disciplines),(l:Lecture) WHERE d.iid = l.discip_id CREATE (l)-[:lecture_disciplina]->(d)")
    neo_session.run("MATCH (s:Specialnost),(d:Disciplines) WHERE s.iid = d.spec_id CREATE (d)-[:disciplina_specialnost]->(s)")
    neo_session.run("MATCH (l:Lecture),(t:TimeTable) WHERE l.iid = t.lecture_id CREATE (t)-[:timeTable_lecture]->(l)")
    neo_session.run("MATCH (g:Group),(t:TimeTable) WHERE g.iid = t.group_id CREATE (t)-[:timeTable_group]->(g)")

print("NEO Данные добавлены")
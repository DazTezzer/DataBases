from elasticsearch import Elasticsearch, helpers
from neo4j import GraphDatabase
import psycopg2
import redis
from tabulate import tabulate

# -------------------------------------------Elasticsearch-----------------------------------------------

index_name = "materials"
es = Elasticsearch("http://elastic:12345@localhost:9200")

# -------------------------------------------Neo4j-----------------------------------------------

uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root12345"

graphDB_Driver = GraphDatabase.driver(uri, auth=(userName, password))

# -------------------------------------------Postgres-----------------------------------------------

database_name = "university"
user_name = "postgres"
password = "12345"
host_ip = "localhost"
host_port = "5432"
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
    print("Error connect to Postgres", err)

# -------------------------------------------Redis-----------------------------------------------

redis = redis.Redis(
    host='localhost',
    port='6379',
    db=0)

student_limit = 10
phrase = 'данных'
begin_date = '2023-09-01'
end_date = '2023-12-28'

query_body = {
    "size":300,
    "query": {
        "query_string": {
            "query": "*%s*" % (phrase),
            "default_field": "description"
        }
    }
}

materials_with_phrase = es.search(index='materials', body=query_body)
materials_with_phrase_ids = []
for lection_id in materials_with_phrase['hits']['hits']:
    materials_with_phrase_ids.append(str(lection_id['_source']['lecture_id']))

students = []
print(materials_with_phrase_ids)
with graphDB_Driver.session(database="neo4j") as neo_session:
    students.append(neo_session.run(
        "match (l:Lecture)--(tt:TimeTable)--(gr:Group)--(st:Student) where l.iid in $lec return st.id_stud_code as student_id, collect(distinct tt.iid)",
        lec=(materials_with_phrase_ids)).data())
print(students)
result = []
print(str(students[0][0]['student_id']))
print(students[0][0]['collect(distinct tt.iid)'])
print(','.join(map(str, students[0][0]['collect(distinct tt.iid)'])))
for student in students[0]:
    querry_pattern = '''SELECT (CAST(SUM(CASE WHEN visited THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) AS percent, student_id
    FROM visits
    WHERE student_id = %s
    AND "timeTable_id" in (%s)
    AND date_visit between '%s' AND '%s'
    GROUP BY student_id
    '''
    cursor.execute(querry_pattern % (str(student['student_id']), ','.join(map(str, student['collect(distinct tt.iid)'])), str(begin_date),str(end_date)))
    statistic = cursor.fetchall()
    if statistic != []:
        result.append(statistic)
print(result)
sorted_array = sorted(result, key=lambda x: x[0][0])
for res in result:
    print(res)


headers = ["№", "Студент", "Посещение", "Период", "Искомое слово"]
table_data = []
i = 0
for i, item in enumerate(sorted_array):
    if i >= 10:
        break
    procent, student_id = item[0]
    student_name = redis.get(student_id).decode()
    progress = f"{int(procent * 100)}%"
    period = f"c {begin_date} по {end_date}"
    table_data.append([student_id, student_name, progress, period, phrase])

print(tabulate(table_data, headers, tablefmt="grid"))

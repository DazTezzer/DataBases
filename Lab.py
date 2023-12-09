from elasticsearch import Elasticsearch, helpers
from neo4j import GraphDatabase
import psycopg2
import redis
from tabulate import tabulate
#-------------------------------------------Elasticsearch-----------------------------------------------

index_name = "materials"
es = Elasticsearch("http://elastic:12345@localhost:9200")

#-------------------------------------------Neo4j-----------------------------------------------

uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root12345"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

#-------------------------------------------Postgres-----------------------------------------------

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

#-------------------------------------------Redis-----------------------------------------------

redis = redis.Redis(
     host= 'localhost',
     port= '6379',
     db=0)


student_limit = 10
phrase = 'модели'
begin_date = '2023-09-01'
end_date = '2023-12-28'


query_body = {
    "query": {
        "query_string": {
            "query":  "*%s*" % (phrase),
			"default_field": "description"
        }
    }
}

materials_with_phrase = es.search(index='materials', body=query_body)
materials_with_phrase_ids = []
for lection_id in materials_with_phrase['hits']['hits']:
	materials_with_phrase_ids.append(lection_id['_source']['lecture_id'])

students = []

for lection_id in materials_with_phrase_ids:
    for student in graphDB_Driver.session(database="neo4j").run(
        "MATCH (l:Lecture{iid:$id})--(d:Disciplines)--(s:Specialnost)--(g:Group)--(st:Student) RETURN  st", id=str(lection_id)).data():
        students.append(student['st']['id_stud_code'])
print(students)

querry_pattern = '''SELECT (CAST(SUM(CASE WHEN visited THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) AS percent, student_id
FROM visits
WHERE student_id in (%s)
AND date_visit between '%s' AND '%s'
GROUP BY student_id
ORDER BY percent
LIMIT '%s'
'''
cursor.execute(querry_pattern % (','.join(map(str,students)), str(begin_date), str(end_date), str(student_limit)))
result=cursor.fetchall()

headers = ["№", "Студент", "Посещение", "Период", "Искомое слово"]
table_data = []

for i, item in enumerate(result, 1):
    student_id = item[1]
    student_name = redis.get(student_id).decode()
    progress = f"{int(item[0] * 100)}%"
    period = f"c {begin_date} по {end_date}"

    table_data.append([i, student_name, progress, period, phrase])

print(tabulate(table_data, headers, tablefmt="grid"))


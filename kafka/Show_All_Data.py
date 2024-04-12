from elasticsearch import Elasticsearch
from neo4j import GraphDatabase
from pymongo import MongoClient
import psycopg2
import redis

#python3 kafka/Show_All_Data.py > output.txt

# Подключение к Elasticsearch
es = Elasticsearch("http://elastic:12345@localhost:9200")

# Подключение к Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "root12345"))

# Подключение к MongoDB
CONNECTION_STRING = "mongodb://admin:12345@localhost:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)

db = client.university
# Подключение к Postgres
conn = psycopg2.connect(database="university", user="postgres", password="12345", host="localhost", port="5432")
cur = conn.cursor()

# Подключение к Redis
redis = redis.Redis(
     host= 'localhost',
     port= '6379',
     db=0)

# Извлечение данных из Elasticsearch
try:
    es_data = es.search(index='university.public.materials', body={'query': {'match_all': {}}})
    es_data = str(es_data)
    es_data = es_data.replace("{'_index':",'\n\n' + "Elasticsearch data: {'_index':")
    substrings = [es_data[i: i + 300] for i in range(0, len(es_data), 300)]
    print("Elasticsearch data:")
    for substring in substrings:
        print(substring)
    print("\nElasticsearch Complited\n")
except Exception as err:
    print("\nElasticsearch Error\n", err)


# Извлечение данных из Neo4j
try:
    with driver.session() as session:
        neo4j_data = session.run("MATCH (n) RETURN n")
        for record in neo4j_data:
            print("Neo4j data:", record)
    print("\nNeo4j Complited\n")
except Exception as err:
    print("\nNeo4j Error\n", err)

# Извлечение данных из MongoDB
try:
    mongo_data = db.institute.find({})
    for document in mongo_data:
        print("MongoDB data:", document)
    print("\nMongoDB Complited\n")
except Exception as err:
    print("\nMongoDB Error\n", err)
# Извлечение данных из Postgres
try:
    cur.execute("SELECT * From institute")
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data institute:", row)

    cur.execute("SELECT * From kafedra")
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data kafedra:", row)

    cur.execute("SELECT * From specialnost")
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data specialnost:", row)

    cur.execute('SELECT * From "group"')
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data group:", row)

    cur.execute("SELECT * From students")
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data students:", row)

    cur.execute("SELECT * From disciplines")
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data disciplines:", row)

    cur.execute("SELECT * From lecture")
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data lecture:", row)

    cur.execute('SELECT * From "timeTable"')
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data timeTable:", row)

    cur.execute("SELECT * From visits")
    postgres_data = cur.fetchall()
    for row in postgres_data:
        print("Postgres data visits:", row)


    print("\nPostgres Complited\n")
except Exception as err:
    print("\nPostgres Error\n", err)

# Извлечение данных из Redis
try:
    redis_data = redis.keys('*')
    for key in redis_data:
        print("Redis data:", redis.get(key).decode('utf-8'))
    print("\nRedis Completed\n")
except Exception as err:
    print("\nRedis Error:\n", err)

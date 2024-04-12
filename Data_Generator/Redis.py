import psycopg2
import redis

database_name = "university"
user_name = "postgres"
password = "12345"
host_ip = "localhost"
host_port ="5432"
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
redis = redis.Redis(
     host= 'localhost',
     port= '6379')

query_for_redis = ("SELECT id_stud_code,fio FROM public.students;")
cursor.execute(query_for_redis)
result=cursor.fetchall()

for i in range(len(result)):
    redis.set(str(result[i][0]),str(result[i][1]))

print("Redis Данные добавлены")
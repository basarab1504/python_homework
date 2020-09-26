import table
import categorizer
import cx_Oracle
import json


credentials = json.load(open(input("Путь до файла конфигурации")))

cx_Oracle.init_oracle_client(credentials["client"])

def clear():
    conn = cx_Oracle.connect(credentials["login"], credentials["password"], credentials["host"], encoding="UTF-8")
    cur = conn.cursor()
    cur.execute("drop table petrushin_test")

    cur.execute(f"""
    CREATE TABLE petrushin_test (
    id NUMBER GENERATED BY DEFAULT AS identity,
    name VARCHAR2(100),
    phone_number VARCHAR2(100),
    inn VARCHAR2(12),
    post_index VARCHAR2(6),
    email VARCHAR2(100),
	website VARCHAR2(100))
    """)

    cur.executemany(f"insert into petrushin_test(name, phone_number, inn, post_index, email) values (:1, :2, :3, :4, :5)", [
        ("Филимошин Роман Владимирович", "+7 (495) 913-09-65",
         "4025062831", None, "Mail@service-nalog.ru"),
        ("Мелешкин Михаил Федорович", None,
         "+7707288107", "127381", "prodez@mail.ru"),
        ("Мурашов Сергей Борисович", "+7 (812) 492-20-58", "7814001461", None, None)
    ])
    conn.commit()


clear()

c = categorizer.categorizer()

t1 = table.oracle_table(credentials["login"], credentials["password"], credentials["host"], "petrushin_test")
t2 = table.oracle_table(credentials["login"], credentials["password"], credentials["host"], "petrushin_test_csv")

t1.categories = c.get_category(t1.get_data())
t2.categories = c.get_category(t2.get_data())

print("Данные petrushin_test до обогащения")
print(t1.get_data())
print("=======")
print("Данные petrushin_test после обогащения")
t1.update_from_table(t2)
print(t1.get_data())

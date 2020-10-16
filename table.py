import cx_Oracle
import csv


class table:
    def __init__(self):
        self.categories = {}

    def categorize(self, categorizer):
        for data in self.get_data().items():
            self.categories[data[0]] = categorizer.get_category(data[1])

    def update_from_table(self, other_table):
        self._update_tables(other_table)

    # возвращает словарь - заголовок:данные
    def get_data(self):
        pass

    def commit(self):
        pass

    def _update_tables(self, other_table):
        pass

    def _update_data(self, other_table):
        pass


class csv_table(table):
    def __init__(self, table_name):
        self.table_name = table_name

    def get_data(self):
        columns = []
        with open(self.table_name, encoding="UTF-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            data = [d for d in csv_reader]
            columns = data[0]
            del data[0]

        column_data = {}

        for index in range(len(columns)):
            column_data[columns[index]] = [d[index] for d in data]
        return column_data


class online_db_table(table):
    def get_connection(self):
        pass


class oracle_table(online_db_table):
    def __init__(self, login, password, host, table_name):
        super().__init__()
        self.table_name = table_name
        self.login = login
        self.password = password
        self.host = host

    def get_connection(self):
        return cx_Oracle.connect(self.login, self.password, self.host, encoding="UTF-8")

    def get_data(self):
        cursor = self.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")

        data = [data for data in cursor]
        column_data = {}

        for index in range(len(cursor.description)):
            column_data[cursor.description[index][0]] = [d[index]
                                                         for d in data]
        return column_data

    def update_from_table(self, other_table):
        self._update_tables(other_table)
        self._update_data_per_record(other_table)

    def commit(self):
        self.get_connection().commit()

    def _update_tables(self, other_table):
        cursor = self.get_connection().cursor()
        for c in other_table.categories.items():
            if c[0] not in self.categories.keys():
                self.categories[c[0]] = c[1]
                cursor.execute(
                    f"ALTER TABLE {self.table_name} ADD {c[1]} VARCHAR2(100)")

    def _update_data_per_record(self, other_table):
        conn = self.get_connection()
        cursor = conn.cursor()
        column_name = self.categories['inn']
        other_column_name = other_table.categories['inn']
        for key in self.get_data()[column_name]:
            index = self.get_data()[column_name].index(key)
            if key in other_table.get_data()[other_column_name]:
                other_index = other_table.get_data()[other_column_name].index(key)
                for c in self.categories.items():
                    db_column_name = c[0]
                    if db_column_name in other_table.categories:
                        data = self.get_data()[c[1]][index]
                        if data is None:
                            other_data = other_table.get_data()[other_table.categories[db_column_name]][other_index]
                            print("column_name:", db_column_name, "data:", data, "new data:", other_data)
                            db_column_name = self.categories[db_column_name]
                            cursor.execute(f"""update {self.table_name} set {db_column_name} = '{other_data}' where inn = {key}""")
        conn.commit()

    def _update_data(self, other_table):
        conn = self.get_connection()
        cursor = conn.cursor()

        for column_name in self.categories.values():
            cursor.execute(f"""update {self.table_name} 
            set {column_name} = nvl({self.table_name}.{column_name}, (select {other_table.table_name}.{column_name} 
            from {other_table.table_name} 
            where {self.table_name}.inn = {other_table.table_name}.inn))""")
        conn.commit()

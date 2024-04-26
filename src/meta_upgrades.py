import os
import sqlite3

class Meta:
    def __init__(self, upgrades, player_profile, test=False, test_data=None):
        if not self.database_exists("meta.db"):
            self.init_database()
        self.conn = sqlite3.connect('meta.db')
        self.upgrades = upgrades
        self.profile = player_profile
        if test is True:
            self.meta_status = self.test_init(test_data)
        else:
            self.meta_status = self.fetch_data()

    def database_exists(self, path):
        return os.path.exists(path)

    def init_database(self):
        conn = sqlite3.connect('meta.db')
        cursor = conn.cursor()
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS Profiles (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            upgrades TEXT NOT NULL
        );
        '''
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()
        self.insert_rows()

    def insert_rows(self):
        conn = sqlite3.connect('meta.db')
        cursor = conn.cursor()
        insert_row_sql = '''
            INSERT INTO Profiles (name, upgrades) 
            VALUES (?, ?);
            '''
        for i in range(3):
            values = (f"gamer{i+1}", "0000000")
            cursor.execute(insert_row_sql, values)
            conn.commit()
        values = ("test", "0000000")
        cursor.execute(insert_row_sql, values)
        conn.commit()
        conn.close()

    def apply_meta_upgrades(self):
        for index, count in enumerate(self.meta_status, start=1):
            for _ in range(int(count)):
                self.upgrades.chosen_upgrade(index)

    def fetch_data(self):
        cursor = self.conn.cursor()
        query = '''
        SELECT upgrades
        FROM Profiles
        WHERE name = ?;
        '''
        cursor.execute(query, (self.profile,))
        data = cursor.fetchone()
        return data[0]

    def update_upgrade_data(self, choice):
        meta_list = list(self.meta_status)
        if meta_list[choice-1] != "9":
            meta_list[choice-1] = chr(ord(meta_list[choice-1])+1)
        self.meta_status = "".join(meta_list)

    def update_data(self, choice):
        self.update_upgrade_data(choice)
        cursor = self.conn.cursor()
        query = '''
        UPDATE Profiles
        SET upgrades = ?
        WHERE name = ?;
        '''
        cursor.execute(query, (self.meta_status, self.profile))
        self.conn.commit()
        self.conn.close()

    def test_init(self, test_data):
        self.add_test_profile(test_data)
        return self.fetch_data()

    def add_test_profile(self, upgrade_status):
        cursor = self.conn.cursor()
        query = '''
        INSERT INTO Profiles (username, email) 
        VALUES (?, ?);
        '''
        values = ("test", upgrade_status)
        cursor.execute(query, values)
        self.conn.commit()

    def remove_test_profile(self):
        cursor = self.conn.cursor()
        query = '''
        DELETE FROM Profiles
        WHERE name = ?;
        '''
        cursor.execute(query, ("test",))

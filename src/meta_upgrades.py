import os
import sqlite3

# Database queries made whith some help from Chat-GPT

class Meta:
    """Class to handle all databade interactions and meta upgrade data
    """
    def __init__(self, upgrades, player_profile, database="meta.db"):
        """Class constructor to handle variables of meta class. 
        Also creates database if one does not exist.

        Args:
            upgrades (Upgrades()): upgrades class object
            player_profile (str): profile name which is used

            test (bool, optional): used in testing to access test fuctionality. 
            Defaults to False.

            test_data (str, optional): used in testing to insert custom values to database. 
            Defaults to None.
        """
        if not self.database_exists(database):
            self.init_database(database)
        self.conn = sqlite3.connect(database)
        self.upgrades = upgrades
        self.profile = player_profile
        self.meta_status = self.fetch_data()

    def database_exists(self, path):
        """Checks if database is present in correct location

        Args:
            path (str): path to database. default location "meta.bd"

        Returns:
            bool: result if database was found
        """
        return os.path.exists(path)

    def init_database(self, database):
        """Function to initialise a new database
        """
        conn = sqlite3.connect(database)
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
        self.insert_rows(database)

    def insert_rows(self, database):
        """Inserts default base data to new database
        """
        conn = sqlite3.connect(database)
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
        """Applies upgrades on player based on meta upgrade data.
        """
        for index, count in enumerate(self.meta_status, start=1):
            for _ in range(int(count)):
                self.upgrades.chosen_upgrade(index)

    def fetch_data(self):
        """Gets selected profiles meta upgrades data from database.

        Returns:
            str: profiles meta upgrades data
        """
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
        """Updates database based on upgrade chosen by player

        Args:
            choice (int): integer reflecting an upgrade
        """
        meta_list = list(self.meta_status)
        if meta_list[choice-1] != "9":
            meta_list[choice-1] = chr(ord(meta_list[choice-1])+1)
        self.meta_status = "".join(meta_list)

    def update_data(self, choice):
        """Handles writing the updated meta upgrade data to database

        Args:
            choice (int): integer reflecting an upgrade
        """
        self.update_upgrade_data(choice)
        cursor = self.conn.cursor()
        query = '''
        UPDATE Profiles
        SET upgrades = ?
        WHERE name = ?;
        '''
        cursor.execute(query, (self.meta_status, self.profile))
        self.conn.commit()

    def add_test_profile(self, upgrade_status):
        """Used to add a test profile to the database

        Args:
            test_data (str): custom meta upgrade status
        """
        cursor = self.conn.cursor()
        query = '''
        INSERT INTO Profiles (name, upgrades) 
        VALUES (?, ?);
        '''
        values = ("test", upgrade_status)
        cursor.execute(query, values)
        self.conn.commit()

    def remove_test_profile(self):
        """Used to remove a test profile from database.
        """
        cursor = self.conn.cursor()
        query = '''
        DELETE FROM Profiles
        WHERE name = ?;
        '''
        cursor.execute(query, ("test",))

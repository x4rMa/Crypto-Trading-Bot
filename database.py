import sqlite3

from create_folders import Folder


class Database:
    def __init__(self):
        pass

    def create_connection(self, db_file):
        conn = None
        conn = sqlite3.connect(db_file)
        return conn

    def create_table(self, db_file):
        sql_create_crypto_table = """CREATE TABLE IF NOT EXISTS crypto (
                                        id real PRIMARY KEY,
                                        DATE text,
                                        CRYPTO text,
                                        TREND text,
                                        ROC real,
                                        PURCHASE real,
                                        UNITS real,
                                        EXCHANGE real,
                                        PRED_LABEL text,
                                        STAT_LABEL text,
                                        ACC_BALANCE real,
                                        PROFIT real,
                                        SPOT_PRICE real,
                                        NATIVE_BALANCE real

                                    ); """
        file_path = Folder().create_folder_link("SQLDatabase", db_file)
        conn = self.create_connection(file_path)
        if conn is not None:
            conn.execute(sql_create_crypto_table)
            conn.commit()
            conn.close()

        else:
            print("Error! cannot create the database connection.")

    def create_entry_crypto(self, db_file, data):
        sql = """ INSERT INTO crypto (id,DATE,CRYPTO,TREND, ROC, PURCHASE,UNITS, EXCHANGE, PRED_LABEL, STAT_LABEL, ACC_BALANCE, PROFIT, SPOT_PRICE, NATIVE_BALANCE)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
        file_path = Folder().create_folder_link("SQLDatabase", db_file)
        conn = self.create_connection(file_path)
        if conn is not None:
            c = conn.execute(sql, data)
            conn.commit()
            conn.close()
            return c.lastrowid

        else:
            print("Error! cannot create the database connection.")

    def main(self):
        # Code for creating database connection and table
        print("Creating database connection and table...")

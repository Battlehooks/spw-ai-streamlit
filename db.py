import mysql.connector
from datetime import datetime
import streamlit as st


class InsertData:
    def __init__(self, question):
        self.mydb = mysql.connector.connect(
            host=st.secrets['db_host'],
            user=st.secrets['db_user'],
            password=st.secrets['db_pass'],
            database=st.secrets['db_data']
        )
        self.cursor = self.mydb.cursor()
        self.question = question

    def commit(self):
        timestamp = datetime.now()
        question = self.question
        year, month, day, hour, minute, second = timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second
        query = 'INSERT INTO pertanyaan (pertanyaan, timestamp) VALUES (%s, %s)'
        value = (question, f"{year}-{month}-{day}-{hour}-{minute}-{second}")
        self.cursor.execute(query, value)
        self.mydb.commit()
        print(f'{self.cursor.rowcount} record inserted.')

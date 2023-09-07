import mysql.connector
from datetime import datetime
import streamlit as st
mydb = mysql.connector.connect(
    host=st.secrets['db_host'],
    user=st.secrets['db_user'],
    password=st.secrets['db_pass'],
    database=st.secrets['db_data']
)


class InsertData:
    def __init__(self, question, total_answer, jawaban_ai):
        self.mydb = mysql.connector.connect(
            host=st.secrets['db_host'],
            user=st.secrets['db_user'],
            password=st.secrets['db_pass'],
            database=st.secrets['db_data']
        )
        self.cursor = self.mydb.cursor()
        self.question = question
        self.total_answer = total_answer
        self.jawaban_ai = jawaban_ai

    def commit(self):
        timestamp = datetime.now()
        question = self.question
        year, month, day, hour, minute, second = timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second
        token_pertanyaan = len(self.question.split(' ')) + 2
        token_jawaban = len(self.jawaban_ai.split(' ')) + 2
        duplicated = self.check_duplicate()
        if duplicated > 0:
            return
        query = 'INSERT INTO pertanyaan_jawaban (timestamp, pertanyaan, total_jawaban, jawaban_ai, token_pertanyaan, token_jawaban) VALUES (%s, %s, %s, %s, %s, %s)'
        value = (f"{year}-{month}-{day}-{hour}-{minute}-{second}",
                 question, self.total_answer, self.jawaban_ai, token_pertanyaan, token_jawaban)
        self.cursor.execute(query, value)
        self.mydb.commit()
        print(f'{self.cursor.rowcount} record inserted.')

    def check_duplicate(self):
        query = 'SELECT pertanyaan FROM pertanyaan_jawaban WHERE lower(pertanyaan) = %s'
        val = (self.question.lower(), )
        self.cursor.execute(query, val)
        result = self.cursor.fetchall()
        count = len(result)
        return count

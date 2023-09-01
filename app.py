import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from db import InsertData
import socket

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
print(f'Hostname : {hostname}')
print(f'IP Address : {ip_addr}')

api_key = st.secrets['OPENAI_API_KEY']
model_name = 'ft:gpt-3.5-turbo-0613:personal::7sLvXR18'

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
db = FAISS.load_local('retriever/FAISS_SPW', embeddings=embeddings)
model = ChatOpenAI(openai_api_key=api_key)
result = False

retriever = RetrievalQA.from_chain_type(
    llm=model,
    chain_type='stuff',
    retriever=db.as_retriever(
        search_kwargs={'score_threshold': .35}
    ),
    return_source_documents=True
)

st.title('AI SPW / PKK / KWU / Technopreneur')
st.write('<small>V1 - September 3rd 2023 Version</small>',
         unsafe_allow_html=True)
st.write('Disiapkan oleh https://www.gaeni.org dan SEAQIS')
prompt = st.text_input('Berikan Pertanyaan : ')
btn = st.button('Submit')
btn_status = False
if btn:
    btn_status = True
if prompt:
    result = retriever({
        'query': prompt
    })
    if result['result'].startswith('Maaf,'):
        result['result'] = 'Model general tidak mengetahui jawaban yang ditanyakan oleh pengguna, silahkan mencari jawaban di <b>Jawaban Lainnya</b>'
    result['result'] = result['result'].replace('\n', '<br />')
if result:
    # st.subheader('Jawaban Utama')
    # st.write(result['result'], unsafe_allow_html=True)
    # st.divider()
    st.subheader('Jawaban')
    for i, res in enumerate(result['source_documents']):
        st.write('\n\n')
        st.write(
            f'<b><u>Jawaban {i + 1}</b></u>', unsafe_allow_html=True)
        st.write(res.page_content)
    if len(result['source_documents']) < 1:
        st.write(
            'Tidak ada jawaban yang relevan dari pertanyaan tersebut terkait SPW.')
    answer = InsertData(prompt)
    answer.commit()

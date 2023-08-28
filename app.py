import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
import openai

api_key = st.secrets['OPENAI_API_KEY']
model_name = 'ft:gpt-3.5-turbo-0613:personal::7sLvXR18'

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
db = FAISS.load_local('retriever/FAISS_SPW', embeddings=embeddings)
model = ChatOpenAI(openai_api_key=api_key)
result = False

retriever = RetrievalQA.from_chain_type(
    llm=model,
    chain_type='stuff',
    retriever=db.as_retriever(),
    return_source_documents=True
)

st.title('SPW QnA')
prompt = st.text_input('Berikan Pertanyaan : ')
if prompt:
    result = retriever({
        'query': prompt
    })

if result:
    st.subheader('Jawaban Utama')
    st.write(result['result'])
    st.subheader('Jawaban Lainnya')
    for res in result['source_documents']:
        st.write(res.page_content)
        st.write('\n')
        st.divider()

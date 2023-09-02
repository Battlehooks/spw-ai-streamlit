import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from db import InsertData

api_key = st.secrets['OPENAI_API_KEY']
model_name = 'ft:gpt-3.5-turbo-0613:personal::7sLvXR18'

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
db = FAISS.load_local('retriever/FAISS_SPW', embeddings=embeddings)
model = ChatOpenAI(openai_api_key=api_key, model=model_name,
                   temperature=0.18)
result = False

retriever = RetrievalQA.from_chain_type(
    llm=model,
    chain_type='stuff',
    retriever=db.as_retriever(
        search_kwargs={'score_threshold': .32}
    ),
    return_source_documents=True
)

st.markdown('''
    <style>
            small {
            font-size: 13px !important;
            }
''', unsafe_allow_html=True)


def answer_question(result):
    st.subheader('Jawaban Utama')
    st.write(result['source_documents']
             [0].page_content, unsafe_allow_html=True)
    st.divider()
    st.subheader('Jawaban dari AI')
    st.write('''
        <small> Keterangan : Jawaban dari AI adalah jawaban yang diekstrapolasi oleh GPT 3.5 dari database kami.</small> <br />
             <small> Sehingga akurasi dalam ilmu pengetahuan mutlak akan sangat rendah dan kemungkinan tidak akurat. </small> 
    ''', unsafe_allow_html=True)
    st.write(result['result'], unsafe_allow_html=True)
    if len(result['source_documents']) > 1:
        st.divider()
        st.subheader('Jawaban Lainnya')
        for i, res in enumerate(result['source_documents']):
            st.write('\n\n')
            st.write(
                f'<b><u>Jawaban {i + 1}</b></u>', unsafe_allow_html=True)
            st.write(res.page_content)


st.title('AI SPW / PKK / KWU / Technopreneur / GCC 4')
st.write(
    '''
    <small>v1.01 - September 3rd 2023 Version</small> <br />
    <small>Disiapkan oleh https://www.gaeni.org dan SEAQIS</small>
    ''',
    unsafe_allow_html=True)
prompt = st.text_input('Berikan Pertanyaan : ')
btn = st.button('Submit')
btn_status = False
if btn:
    btn_status = True
if prompt:
    result = retriever({
        'query': prompt
    })
if result:
    if len(result['source_documents']) < 1:
        st.write(
            'Tidak ada jawaban yang relevan dari pertanyaan tersebut terkait SPW.')
    else:
        answer_question(result)
        answer = InsertData(prompt, len(
            result['source_documents']), result['result'])
        answer.commit()

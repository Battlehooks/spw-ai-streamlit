import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from db import InsertData
import os

api_key = st.secrets['OPENAI_API_KEY']
model_name = 'ft:gpt-3.5-turbo-0613:personal::7sLvXR18'

fs = LocalFileStore('retriever/cache_embed')
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
cache_embed = CacheBackedEmbeddings.from_bytes_store(embeddings, fs, namespace = embeddings.model)
db = FAISS.load_local('retriever/FAISS_SPW', embeddings=cache_embed)
model = ChatOpenAI(openai_api_key=api_key, temperature=0.06)

retriever = RetrievalQA.from_chain_type(
    llm=model,
    chain_type='stuff',
    retriever=db.as_retriever(
        search_kwargs={'k': 5, 'score_threshold': .32}
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
    primary = result['source_documents'][0].page_content
    primary = primary.split('[SEP]')[-1].strip()
    st.markdown(primary, unsafe_allow_html=True)
    st.divider()
    st.subheader('Jawaban dari AI')
    st.markdown('''
        <small> Keterangan : Jawaban dari AI adalah jawaban yang diekstrapolasi oleh GPT 3.5 dari database kami.</small> <br />
        <small> Sehingga akurasi dalam ilmu pengetahuan mutlak akan sangat rendah dan kemungkinan tidak akurat. </small> 
    ''', unsafe_allow_html=True)
    st.markdown(result['result'], unsafe_allow_html=True)
    if len(result['source_documents']) > 1:
        st.divider()
        st.subheader('Jawaban Lainnya')
        for i, res in enumerate(result['source_documents'][1:]):
            st.markdown('\n\n')
            st.markdown(
                f'<b><u>Jawaban {i + 1}</b></u>', unsafe_allow_html=True)
            text = res.page_content.split('[SEP]')[-1]
            text = text.strip()
            st.markdown(text)

def main() :
    st.title('GEMA-GPT')
    st.markdown('AI ini adalah versi beta dalam rangka melengkapi data set yang akan kita kompilasi dalam sistem yang dikembangkan sampai akhir Desember 2023')
    st.markdown('Technopreneur : Gatot Hari Priowirjanto, Tim Guru SPW, mahasiswa Golden Tiket PENS')
    st.markdown('Hukum : Enni Soerjati, Carolina')
    st.markdown('Perikanan : Siswoyo, Tim Mahasiswa SEAMEO QIS UNPAD - Eros, Aisyah, Rahma, Rafif, Mira, Abian, Bagus, Aidil, Rohmad dkk')
    st.markdown('Peternakan  : Achmad, Mahasiswa PENS - Anifa, Trifosha, dan Industri')
    st.markdown('STEM : Indrawati')
    st.markdown('Elektronika dan Otomotif : Eko Subiantoro, Wahyu Purnomo, BBPPMPV BoE Malang')
    st.markdown('Mesin CNC : Joko Suseno, BBPPMPV BMTI Bandung')
    st.markdown('Kakao : Dini, Halimah, Nur Fazila')
    st.markdown(
        '''
        <small>v1.42 - October 25th 2023 Version</small> <br />
        <small>Disiapkan oleh https://www.gaeni.org dan SEAQIS dan Tim Metaverse BMTI</small>
        ''',
        unsafe_allow_html=True)
    result = False
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
            st.markdown(
                'Tidak ada jawaban yang relevan dari pertanyaan tersebut.')
        elif 'tidak tahu' in result['result'][:20].lower():
            st.markdown(
                'Tidak ada jawaban yang relevan dari pertanyaan tersebut.')
        elif 'sorry' in result['result'].lower():
            st.markdown(
                'Berikan pertanyaan yang lebih spesifik.'
            )
        elif result['result'].lower() == prompt.lower():
            st.markdown(
                'Berikan pertanyaan yang lebih spesifik dan tepat.'
            )
        else:
            answer_question(result)
            answer = InsertData(prompt, len(
                result['source_documents']), result['result'])
            answer.commit()
main()
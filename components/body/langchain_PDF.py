from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import streamlit as st

def get_response_from_OpenAI_LangChain(uploaded_file, prompt):
    
    try:
        reader = PdfReader(uploaded_file)

        raw_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text

        text_splitter = CharacterTextSplitter(separator = "\n",
                                            chunk_size = 1000,
                                            chunk_overlap = 200,
                                            length_function = len)

        texts = text_splitter.split_text(raw_text)
        with st.spinner('Processing Embeddings...'):
            embeddings = OpenAIEmbeddings()
            doc_search = FAISS.from_texts(texts, embeddings)
            chain = load_qa_chain(OpenAI(), chain_type='map_reduce')

        query = prompt
        docs = doc_search.similarity_search(query)

        with st.spinner('Generating Answer...'):
            response = chain.run(input_documents=docs, question=query) # response
            from components.sidebar.Auth import upload_data

            data = {"prompt": prompt,
                    "response": response}
            
            st.session_state['response'] = response
            upload_data(st.session_state['uuid'], data, uploaded_file.name[:-4])
            return response

    except Exception as e:
        if "You exceeded your current quota" in str(e):
            st.error('Oops! You may have exceeded your API rate limit.\nPlease check you OpenAI API key usage at https://platform.openai.com/account/usage')
        else:
            st.error("Oops! Something went wrong. Please try again. Please check your OpenAI API key in the sidebar.")
        st.stop()
        return
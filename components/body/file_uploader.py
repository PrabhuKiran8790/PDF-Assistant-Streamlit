import streamlit as st
import os


def file_uploader():
    uploaded_file = st.file_uploader("Upload a PDF", type=['pdf'], accept_multiple_files=False)
    
    if st.session_state.get('generate_answer_button', None):
        if uploaded_file is None:
            st.caption(":red[Please upload a PDF]")

    if uploaded_file is None:
        st.session_state['uploaded_file'] = None
        
    else:
        st.session_state['uploaded_file'] = uploaded_file
        
    
import streamlit as st
import os

def set_openAi_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    os.environ['OPENAI_API_KEY'] = api_key


def openai_api_insert_component():
     with st.sidebar:
        st.markdown(
            "## Usage Instructions\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"
            "2. Upload a pdf file📄\n"
            "3. Ask a question about the document💬\n"
        )

        api_key_input = st.text_input("OpenAI API Key",
                                      type="password",
                                      placeholder="OpenAI API Key",
                                      help="You can get your API key from https://platform.openai.com/account/api-keys.")
        
        if st.session_state.get('generate_answer_button', None):
            if api_key_input == "" or api_key_input is None:
                st.sidebar.caption("👆 :red[Please set your OpenAI API Key here]")
        
        
        st.caption(":green[Your API is not stored anywhere. It is only used to generate answers to your questions.]")

        set_openAi_api_key(api_key_input)
        
        
if __name__ == "__main__":
    openai_api_insert_component()
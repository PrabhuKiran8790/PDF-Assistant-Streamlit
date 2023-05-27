import streamlit as st


def prompt_box():
    prompt = st.text_area("Enter your question here", height=100)
    if st.session_state.get('generate_answer_button', None):
        if prompt == "" or prompt is None:
            st.caption(":red[Please enter a prompt]")
    
    
    if prompt is not None: # If prompt is not empty
        st.session_state['prompt'] = prompt
    

if __name__ == "__main__":
    prompt_box()
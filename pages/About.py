import streamlit as st

def about():
    st.markdown("""
# PDF-Assistant : AI-Powered Q&A for PDFs

Welcome to PDF-Assistant, an AI-powered web app that helps you extract valuable information from PDF documents with ease! 📚🔍

## About the App

PDF-Assistant leverages the power of OpenAI GPT 3.0 to provide accurate and intelligent answers to your questions related to PDF content. Whether you're a student, researcher, or professional, our app aims to make your PDF reading experience more efficient and productive. 🚀💡

## Key Features

- AI-Powered Q&A: Simply upload your PDF document and enter your API key, and our advanced language model will be at your service! Ask any question related to the PDF content, and the AI will generate detailed and relevant answers for you. It's like having your own personal PDF expert! 💭💡🤖

- Firebase Integration: PDF-Assistant utilizes Firebase for authentication and database management. Your data and personal information are securely stored, ensuring a safe and reliable user experience. 🔒🔐🚀

- Past History: Never lose track of your previous queries and responses! PDF-Assistant keeps a history of all your prompts and the corresponding AI-generated answers, allowing you to review and revisit them whenever you need to. 📚🔍📝🕒

- Guest Mode: Don't want to go through the hassle of logging in? No worries! PDF-Assistant also offers a convenient guest mode. While prompts and responses aren't saved for guest users, it allows quick access to the powerful AI capabilities of the app. 🚀👥🔓

## How to Use

1. Log in using your credentials or simply use the guest mode.
2. Upload your PDF document by following the provided instructions.
3. Enter your API key to enable AI interaction.
4. Ask any question related to the PDF content using natural language prompts.
5. Wait for the AI to generate insightful and accurate answers for you.
6. Explore the past history section to review your previous prompts and responses.
7. Enjoy a seamless PDF reading experience with the help of AI intelligence!

## Start Exploring PDF-Assistant Today!

Don't let valuable information get lost in your PDF documents. Unlock the power of AI with PDF-Assistant and make the most out of your PDF reading and research endeavors. Start using PDF-Assistant today and experience a new level of productivity! 🎉🔍


""")
    

def main():
    about()
    
if __name__ == "__main__":
    main()
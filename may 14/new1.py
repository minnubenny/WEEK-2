# Import libraries
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import Chroma  # ✅ Updated import

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Set your actual environment variable as a named key
# Never hardcode API keys!
genai.configure(api_key=os.getenv("AIzaSyAyp-J9yb7k7SZMl5oQXSyHMhBOrEzo3HU"))

# Function to extract text from uploaded PDF documents
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split the extracted text into chunks 
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create and store embeddings in ChromaDB
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    vector_store = Chroma.from_texts(
        text_chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    vector_store.persist()

# Function to define a conversational chain for answering questions
def get_conversational_chain():
    prompt_template = """ 
    Answer the question as detailed as possible from the provided context. Make sure to provide all the details. 
    If the answer is not in the provided context, just say "answer is not available in the context". Do not provide the wrong answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to handle user input, search for relevant documents and answer the question
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    docs = vector_store.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    st.write("Reply:", response["output_text"])

# Main function
def main():
    st.set_page_config(page_title="Chat with Multiple PDF using ChromaDB and Gemini")
    st.header("Chat with Multiple PDF")

    user_question = st.text_input("Ask a question about your PDF:")
    if user_question:
        user_input(user_question)
    
    # Sidebar for uploading PDF files
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Extracting text from PDF..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done! You can now ask questions.")

# ✅ Fixing the __name__ typo
if __name__ == "__main__":
    main()

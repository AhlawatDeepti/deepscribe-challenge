# C:\Users\17329\Documents\deepscribe-challenge\backend\app.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Data Loading and Processing ---
# Load the transcript
loader = TextLoader('./transcript.txt')
documents = loader.load()

# Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Create embeddings and store in Chroma vector store
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma.from_documents(docs, embedding)

# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app)

# --- LLM and QA Chain Setup ---
# FINAL FIX: Using a model name that is confirmed to be available to your project.
llm = ChatGoogleGenerativeAI(model="models/gemini-pro-latest", temperature=0.3)
retriever = vector_store.as_retriever(search_kwargs={"k": 3}) 
qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever)

# In-memory store for chat histories
chat_histories = {} 

@app.route('/')
def index():
    return "Backend server is running!"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')
    session_id = data.get('session_id', 'default_session')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    chat_history = chat_histories.get(session_id, [])

    try:
        result = qa_chain.invoke({"question": question, "chat_history": chat_history}) 
        answer = result['answer']

        # Update chat history for this session
        chat_history.append((question, answer))
        chat_histories[session_id] = chat_history[-5:]

        return jsonify({'answer': answer})
    except Exception as e:
        print(f"An error occurred: {e}") 
        return jsonify({'error': 'Failed to process the request'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
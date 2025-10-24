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

# --- Flask App Initialization ---
app = Flask(__name__)

frontend_url = "https://deepscribe-challenge-frontend.onrender.com"

CORS(app, resources={r"/api/*": {"origins": frontend_url}})


# We will initialize this on the first request to avoid timeouts on startup.
qa_chain = None

def initialize_qa_chain():
    """
    This function will be called once on the first request to initialize
    the expensive components (models, vector store).
    """
    global qa_chain
    print("Initializing QA Chain...")
    
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Data Loading and Processing
    loader = TextLoader('./transcript.txt')
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma.from_documents(docs, embedding)
    
    # LLM and QA Chain Setup
    llm = ChatGoogleGenerativeAI(model="models/gemini-pro-latest", temperature=0.3)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3}) 
    
    # Assign the initialized chain to the global variable
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever)
    print("QA Chain Initialized Successfully.")


# --- Routes ---

# In-memory store for chat histories
chat_histories = {} 

@app.route('/')
def index():
    return "Backend server is running!"

@app.route('/api/chat', methods=['POST'])
def chat():
    # LAZY INITIALIZATION: Check if the chain has been loaded yet.
    if qa_chain is None:
        try:
            initialize_qa_chain()
        except Exception as e:
            print(f"CRITICAL: Failed to initialize QA Chain: {e}")
            return jsonify({'error': 'Server is not ready, initialization failed.'}), 503

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
        print(f"An error occurred during chat processing: {e}") 
        return jsonify({'error': 'Failed to process the request'}), 500

if __name__ == '__main__':
    # When running locally, we can initialize right away for easier debugging
    initialize_qa_chain()
    app.run(debug=True, port=5001)
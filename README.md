# DeepScribe Coding Challenge: AI Transcript Assistant

This project is a proof-of-concept web application designed to fulfill the DeepScribe Coding Challenge. It allows medical providers to interact with a patient transcript through an intuitive chat interface, asking follow-up questions and receiving context-aware answers powered by a Large Language Model (LLM).

**Live Demo Link:** [https://deepscribe-challenge-frontend.onrender.com](https://deepscribe-challenge-frontend.onrender.com) 

---

## Key Features

-   **Interactive Chat UI:** A clean, responsive web interface for providers to query the clinical transcript.
-   **Context-Aware Q&A:** Leverages the Google Gemini LLM to understand and answer questions based on the provided transcript content.
-   **Contextual Follow-ups:** Maintains a short-term memory of the conversation, allowing for natural follow-up questions (e.g., "Why was *it* prescribed?").
-   **Secure and Efficient Backend:** Built with Python and Flask, using a RAG (Retrieval-Augmented Generation) pipeline to process queries.

---

### Backend Setup
```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows: venv\\Scripts\\activate
# On Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file in the 'backend' directory
# and add your Google API key:
# GOOGLE_API_KEY="YOUR_API_KEY_HERE"

# Run the server
flask run --port=5001
```

### Frontend Setup
```bash
# (In a separate terminal) Navigate to the frontend folder
cd frontend

# Install dependencies
npm install

# Run the development server (make sure the backend is running)
npm run dev
```

The application will be available at http://localhost:5173.
-   **Cold Starts:** If the application has been inactive, the server will "sleep" to conserve resources. The first request after a period of inactivity may take 20-30 seconds as the server needs to wake up.
-   **Lazy Initialization:** To prevent the server from timing out or running out of memory on startup (a common issue on free tiers), the AI models and vector store are **"lazy loaded."** This means they are only initialized on the very first user query, not when the server boots. This adds a one-time delay to the first question, but ensures the application remains stable. Subsequent queries will be significantly faster.

---

## Local Development Setup

### Prerequisites
-   Python 3.8+
-   Node.js and npm
-   Git

### Backend Setup
```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file in the 'backend' directory
# and add your Google API key:
# GOOGLE_API_KEY="YOUR_API_KEY_HERE"

# Run the server
flask run --port=5001
```

### Frontend Setup
# (In a separate terminal) Navigate to the frontend folder
cd frontend

# Install dependencies
npm install

# Run the development server (make sure the backend is running)
npm run dev


The application will be available at http://localhost:5173.
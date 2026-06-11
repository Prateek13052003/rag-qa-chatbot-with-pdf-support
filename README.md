# 📄 Chat with Your PDF using RAG, OpenAI Embeddings & Groq LLM

## Overview of this 
This project is a Retrieval-Augmented Generation (RAG) application built with Streamlit, LangChain, OpenAI Embeddings, Chroma Vector Database, and Groq LLM. The application allows users to upload one or more PDF documents and interact with them through natural language conversations.

The system extracts text from uploaded PDFs, converts the content into vector embeddings, stores them in a Chroma vector database, retrieves relevant document chunks based on user queries, and generates context-aware answers using a Groq-powered Large Language Model.

The application also supports session-based chat history, enabling users to maintain conversational context throughout their interactions.

---

## Features

* Upload and analyze multiple PDF documents.
* Retrieval-Augmented Generation (RAG) architecture.
* OpenAI Embeddings (`text-embedding-3-small`) for semantic search.
* Chroma Vector Store for efficient document retrieval.
* Groq LLM integration using Llama 3.1 8B Instant.
* Session-based conversation memory.
* Context-aware question answering.
* Streamlit web interface.
* Supports follow-up questions using chat history.

---

## Architecture

```text
PDF Upload
     │
     ▼
PDF Loader (PyPDFLoader)
     │
     ▼
Text Splitting
(RecursiveCharacterTextSplitter)
     │
     ▼
OpenAI Embeddings
(text-embedding-3-small)
     │
     ▼
Chroma Vector Store
     │
     ▼
Retriever
     │
     ▼
Groq LLM (Llama 3.1)
     │
     ▼
Answer Generation
     │
     ▼
Streamlit Interface
```

---

## Technologies Used

| Technology        | Purpose                |
| ----------------- | ---------------------- |
| Python 3.9        | Programming Language   |
| Streamlit         | Web Interface          |
| LangChain         | RAG Framework          |
| OpenAI Embeddings | Text Vectorization     |
| ChromaDB          | Vector Database        |
| Groq              | LLM Inference          |
| PyPDFLoader       | PDF Processing         |
| dotenv            | Environment Management |

---

## Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── .env
├── README.md
└── uploaded_pdfs/
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/pdf-chatbot.git

cd pdf-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required Packages

```bash
streamlit
langchain
langchain-community
langchain-openai
langchain-groq
chromadb
pypdf
python-dotenv
openai
```

---

## API Keys Required

The application requires:

### OpenAI API Key

Used for:

* Generating text embeddings
* Semantic document search

### Groq API Key

Used for:

* Running the Llama 3.1 language model
* Generating final responses

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will launch in your browser:

```text
http://localhost:8501
```

---

## How It Works

### Step 1: Upload PDF Files

Users upload one or more PDF documents through the Streamlit interface.

### Step 2: Document Processing

The system loads PDFs using:

```python
PyPDFLoader
```

and extracts text content.

### Step 3: Text Chunking

Large documents are divided into smaller chunks using:

```python
RecursiveCharacterTextSplitter
```

Parameters:

```python
chunk_size = 1000
chunk_overlap = 200
```

### Step 4: Embedding Generation

Each chunk is converted into vector embeddings using:

```python
text-embedding-3-small
```

from OpenAI.

### Step 5: Vector Storage

Embeddings are stored in ChromaDB for efficient similarity search.

### Step 6: Retrieval

When a question is asked:

* User query is reformulated.
* Relevant document chunks are retrieved.
* Context is prepared for the LLM.

### Step 7: Response Generation

The Groq Llama 3.1 model generates an answer strictly based on retrieved document context.

If information is unavailable, the model responds:

```text
I don't know
```

---

## Session-Based Chat History

The application supports multiple conversation sessions.

Each session maintains:

* Previous user questions
* Previous AI responses
* Contextual conversation flow

This enables accurate follow-up question answering.

---

## Example Workflow

```text
Upload PDF
      ↓
Ask:
"What is the main objective of this paper?"

      ↓
Retriever finds relevant sections

      ↓
Groq LLM generates answer

      ↓
User asks:
"What methodology was used?"

      ↓
Chat history helps understand context

      ↓
Updated answer generated
```

---

## Advantages of RAG

* Reduces hallucinations.
* Answers are grounded in uploaded documents.
* Supports private document querying.
* Improves factual accuracy.
* Scales to large documents efficiently.

---

## Future Improvements

* PDF highlighting and source citations.
* Support for DOCX and TXT files.
* Persistent vector database storage.
* User authentication.
* Conversational streaming responses.
* Multi-modal document support.
* Local embedding models.
* Advanced document summarization.

---

## Use Cases

* Research Paper Analysis
* Academic Question Answering
* Legal Document Exploration
* Resume Analysis
* Technical Documentation Search
* Enterprise Knowledge Base Systems

---

## Author

Developed using:

* LangChain
* OpenAI Embeddings
* ChromaDB
* Groq LLM
* Streamlit

A Retrieval-Augmented Generation (RAG) chatbot designed for intelligent document-based question answering.

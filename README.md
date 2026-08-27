📚 RAG Document Assistant

A practical Retrieval-Augmented Generation (RAG) project built with Python, LangChain, LangGraph, Ollama, Chroma and Groq.

The project allows a user to upload a document, process its content, store embeddings in a vector database, retrieve relevant information and ask questions about the document.

🚀 Features

PDF document loading

PowerPoint (PPT/PPTX) document loading

Text chunking

Ollama embeddings

Chroma vector database

Similarity search

Top-K retrieval

Context-based question answering

Groq LLM integration

LangChain Agent

LangGraph memory

Environment variable support with .env

Planned / Advanced Features

LlamaParse

Multiple file support

Metadata filtering

Retriever abstraction

Similarity scores

MMR retrieval

Image and chart handling

Vision LLM

Multimodal RAG

Hybrid search

BM25

Reranking

Query transformation

Context compression

Source/page citations

RAG evaluation

🧠 What is RAG?

RAG (Retrieval-Augmented Generation) combines document retrieval with an LLM.

Instead of asking the LLM to answer only from its existing knowledge:

User Question
      ↓
Retrieve relevant document chunks
      ↓
Give chunks to LLM
      ↓
Generate answer

This helps the model answer questions using information from the user's documents.

🔄 RAG Architecture

              PDF / PPT
                  ↓
          Document Loader
                  ↓
              Documents
                  ↓
               Chunking
                  ↓
              Embeddings
                  ↓
             Chroma DB
                  ↓
            Similarity Search
                  ↓
          Relevant Documents
                  ↓
              Context
                  ↓
             Groq LLM
                  ↓
               Answer

🛠️ Tech Stack

Technology

Purpose

Python

Programming language

LangChain

RAG components and orchestration

LangGraph

Agent state and memory

PyPDFLoader

PDF loading

UnstructuredPowerPointLoader

PowerPoint loading

RecursiveCharacterTextSplitter

Text chunking

Ollama

Local model runtime

OllamaEmbeddings

Generate embeddings

Chroma

Vector database

Groq

LLM inference

LlamaParse

Advanced document parsing (planned)

python-dotenv

Environment variables

✅ Current RAG Pipeline

The current implementation follows:

File
 ↓
Loader
 ↓
Document
 ↓
Text Splitter
 ↓
Chunks
 ↓
Ollama Embeddings
 ↓
Chroma
 ↓
Similarity Search
 ↓
Context
 ↓
Prompt
 ↓
Groq LLM
 ↓
Answer

📂 Project Structure

RAG/
│
├── your_rag_file.py
├── .env
├── requirements.txt
├── README.md
│
└── sa_db/
    └── Chroma persistent database

Do not commit your .env file or API keys to GitHub.

⚙️ Installation

Clone the repository:

git clone <your-repository-url>
cd RAG

Install dependencies:

python -m pip install -r requirements.txt

If you do not have a requirements.txt yet, install the main packages:

python -m pip install langchain langchain-community langchain-text-splitters langchain-ollama langchain-chroma langchain-groq langgraph python-dotenv

For LlamaParse:

python -m pip install llama-parse

🔑 Environment Variables

Create a .env file in the project directory:

GROQ_API_KEY=your_groq_api_key
LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key

Load the variables in Python:

from dotenv import load_dotenv

load_dotenv()

Never upload API keys to GitHub.

Add this to .gitignore:

.env
__pycache__/
*.pyc
sa_db/

▶️ How to Run

Run the Python file:

python your_rag_file.py

The application will ask for:

Enter your name:
Enter name for your class assistant:
What do u want to upload?
1. PDF
2. PPT

Then provide the file path and start asking questions about the uploaded document.

To stop the conversation:

exit

or

terminate

📌 Current Implementation

The current implementation uses:

PyPDFLoader

for PDFs and:

UnstructuredPowerPointLoader

for PowerPoint files.

Documents are split using:

RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

Embeddings are generated using:

OllamaEmbeddings(
    model="nomic-embed-text:latest"
)

The vectors are stored in:

Chroma

Relevant chunks are retrieved using:

similarity_search(
    query=query,
    k=5
)

The retrieved context is then passed to a Groq model for generating the final answer.

📈 RAG Learning Roadmap

Completed

Python basics

OOP / Classes

LangChain basics

Document Loaders

PDF loading

PPT loading

Documents

Chunking

Chunk size

Chunk overlap

RecursiveCharacterTextSplitter

Embeddings

Ollama embeddings

Basic vectors

Chroma Vector Database

Similarity Search

Top-K retrieval

Context retrieval

RAG prompting

Groq LLM

Basic hallucination control

LangGraph MemorySaver

Conversation memory

LangChain Agent

Basic Ollama usage

.env / API key basics

To Learn

LlamaParse

Multiple PDF/PPT files

Different file types

Metadata

Retriever

Similarity search with score

MMR

Metadata filtering

Chroma persistence

Image handling

Vision LLM

Multimodal RAG

Hybrid search

BM25

Reranking

Query transformation

Query rewriting

Multi-query retrieval

Context compression

RAG prompt optimization

Grounded responses

Source/page citation

Chat history with RAG

RAG evaluation

RAG optimization

🎯 Project Goal

The final goal is to build a more advanced RAG system that can:

Multiple Documents
       ↓
Advanced Parsing
       ↓
Text + Tables + Images
       ↓
Chunking
       ↓
Embeddings
       ↓
Vector Database
       ↓
Advanced Retrieval
       ↓
Reranking
       ↓
Relevant Context
       ↓
LLM / Vision LLM
       ↓
Grounded Answer
       ↓
Source Citation

🔮 Future Improvements

Add LlamaParse for complex documents.

Support multiple files in one session.

Add metadata-based filtering.

Replace direct similarity search with a retriever.

Add MMR and hybrid search.

Add reranking.

Add support for images and charts.

Build multimodal RAG using a vision model.

Add source and page citations.

Add RAG evaluation.

Build a Streamlit interface.

Improve error handling and user experience.

👨‍💻 Learning Status

Basic RAG: ✅ Completed

Advanced RAG: 🚧 In Progress

Multimodal RAG: ⏳ To Learn

RAG Evaluation: ⏳ To Learn

📄 License

This project is created for learning and educational purposes.

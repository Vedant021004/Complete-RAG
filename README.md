# 📚 RAG Document Assistant

A practical **Retrieval-Augmented Generation (RAG)** project built with Python, LangChain, LangGraph, Ollama, Chroma and Groq.

This project allows users to upload documents, process their content, create embeddings, store them in a vector database, retrieve relevant information and ask questions about the uploaded documents.

---

## 🚀 Features

- PDF document loading
- PowerPoint (PPT/PPTX) document loading
- Text chunking
- Ollama embeddings
- Chroma vector database
- Similarity search
- Top-K retrieval
- Context-based question answering
- Groq LLM integration
- LangChain Agent
- LangGraph memory
- Environment variable support using `.env`

### Planned Features

- LlamaParse
- Multiple file support
- Metadata filtering
- Retriever
- Similarity scores
- MMR retrieval
- Image and chart handling
- Vision LLM
- Multimodal RAG
- Hybrid search
- BM25
- Reranking
- Query transformation
- Context compression
- Source/page citations
- RAG evaluation

---

## 🧠 What is RAG?

**RAG (Retrieval-Augmented Generation)** combines document retrieval with an LLM.

Instead of asking the LLM to answer only from its existing knowledge, RAG first retrieves relevant information from the user's documents and provides that information to the LLM.

### Basic Flow

User Question
↓
Retrieve Relevant Chunks
↓
Give Context to LLM
↓
Generate Answer

---

## 🔄 RAG Architecture

```text
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

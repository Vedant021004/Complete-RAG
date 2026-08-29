import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.document_loaders import (
    UnstructuredPowerPointLoader,
    PyPDFLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


class Assistant:

    def __init__(self, name, ai):
        self.name = name
        self.ai = ai

    def create_assistant(self):

        llm = ChatGroq(
            model="openai/gpt-oss-20b"
        )

        memory = MemorySaver()

        agent = create_agent(
            model=llm,
            checkpointer=memory
        )

        return agent

    def load_document(self, uploaded_file):

        file_name = uploaded_file.name.lower()

        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if file_name.endswith(".pdf"):

            data = PyPDFLoader(file_name)
            doc = data.load()

        elif file_name.endswith(".pptx"):

            data = UnstructuredPowerPointLoader(file_name)
            doc = data.load()

        else:

            st.error("Please upload a PDF or PPTX file.")
            return None

        return doc

    def create_vector_db(self, doc):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(doc)

        embedding = OllamaEmbeddings(
            model="nomic-embed-text:latest"
        )

        vdb = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory="./sa_db"
        )

        return vdb

    def ask_question(self, query, vdb, agent):

        # Search document
        result = vdb.similarity_search(
            query=query,
            k=5
        )

        # Create context
        context = "\n\n".join(
            doc.page_content
            for doc in result
        )

        prompt = f"""
You are {self.ai}, a helpful student assistant.

You answer questions about the uploaded document.

Use the document context below when it is relevant.

Document context:

{context}

Current question:

{query}

Rules:

1. If the answer is available in the document context,
   answer using the document.

2. If the exact answer is NOT available in the document,
   but the question is related to the same topic,
   you may answer using your general knowledge.

3. You can use previous conversation messages when
   the student asks about something discussed earlier.

4. If the question is completely unrelated to the
   document/topic and previous conversation, say:

"I could not find this information."

Give simple and clear answers suitable for a student.
"""

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": "student_1"
                }
            }
        )

        return response["messages"][-1].content


# =====================================================
# STREAMLIT UI
# =====================================================

st.title("🎓 Student Assistant")

st.write("Upload your study material and ask questions!")


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state["messages"] = []


# =====================================================
# STUDENT DETAILS
# =====================================================

name = st.text_input(
    "Enter your name:"
)

ai = st.text_input(
    "Enter name for your class assistant:",
    value="VK"
)


# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload your PDF or PowerPoint",
    type=["pdf", "pptx"]
)


# =====================================================
# PROCESS DOCUMENT
# =====================================================

if name and ai and uploaded_file:

    if st.button("Process Document"):

        with st.spinner("Reading your document..."):

            assistant = Assistant(name, ai)

            doc = assistant.load_document(
                uploaded_file
            )

            if doc:

                vdb = assistant.create_vector_db(
                    doc
                )

                agent = assistant.create_assistant()

                st.session_state["assistant"] = assistant
                st.session_state["vdb"] = vdb
                st.session_state["agent"] = agent

                # Clear old chat when new document is uploaded
                st.session_state["messages"] = []

                st.success(
                    "Document processed successfully! 🎉"
                )


# =====================================================
# CHAT HISTORY
# =====================================================

if "vdb" in st.session_state:

    st.divider()

    st.subheader(
        f"💬 Chat with {st.session_state['assistant'].ai}"
    )

    # Display previous messages
    for message in st.session_state["messages"]:

        with st.chat_message(message["role"]):

            st.write(message["content"])


    # =================================================
    # CHAT INPUT
    # =================================================

    query = st.chat_input(
        f"{name}, ask your question..."
    )


    if query:

        # -----------------------------
        # Show user message
        # -----------------------------

        st.session_state["messages"].append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.write(query)


        # -----------------------------
        # Get answer
        # -----------------------------

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = st.session_state[
                    "assistant"
                ].ask_question(
                    query,
                    st.session_state["vdb"],
                    st.session_state["agent"]
                )

            st.write(answer)


        # -----------------------------
        # Save assistant answer
        # -----------------------------

        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": answer
            }
        )
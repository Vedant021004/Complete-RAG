from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings 
from langchain_chroma import Chroma 
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(model="openai/gpt-oss-20b")

doc = PyPDFLoader("Roads_to_Mussoorie.pdf")
data = doc.load()

splitter =  RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100
)

chunk = splitter.split_documents(data)

embedding = OllamaEmbeddings( model="nomic-embed-text:latest")

vdb = Chroma.from_documents(
    documents=chunk,
    embedding=embedding,
    persist_directory="./rk_db"
)

while True:
    query = input("Ask: ")
    if query in ["exit", "terminate"]:
        print("Terminating... Thank youuu")
        break

    result = vdb.similarity_search(
        query= query,
        k=3
    )

    context = "\n\n".join(
    doc.page_content
    for doc in result
    )

    prompt = f"""
    You are an assistant that answers questions based on the provided PDF.

    Use ONLY the information from the PDF context below.

    PDF context:
    {context}

    Question:
    {query}

    Answer naturally and conversationally.
    Do not copy the PDF word-for-word.

    If the answer is not available in the PDF context, say:
    "I could not find this information in the PDF."
    """

    response = llm.invoke(prompt)

    print("\nAnswer:")
    print(response.content)

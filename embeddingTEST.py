from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)

result = embedding.embed_query("Hello world")

print("Embedding length:", len(result))
print("First 10 values:", result[:10])
from llama_cloud_services import LlamaParse
from dotenv import load_dotenv
import os

load_dotenv()

parser = LlamaParse(
    api_key=os.getenv("LLAMA_API_KEY"),
    result_type="markdown"
)

docs = parser.load_data("offbeat.pdf")

for doc in docs:
    print(doc.text)
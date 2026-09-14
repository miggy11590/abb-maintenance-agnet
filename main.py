#importing os
import os
#importing dotenv
from dotenv import load_dotenv
#importing the pdf reader
from pypdf import PdfReader
#imports sentence transformer
from sentence_transformers import SentenceTransformer
#imports chroma
import chromadb
#opens/extracts the pdf
manual = PdfReader("data/equipment_manual.pdf")
#importing
from google import genai

load_dotenv() #this reads .env and makes gemini api key readable

all_text = ""

for page_number,page in enumerate(manual.pages):
    text = page.extract_text()
    all_text += text + "\n"
#tells you how many characters are in the text
print("Characters extracted",len(all_text))
#chunnks the text
def chunk_text(text, chunk_size=1000,overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # move the start forward, but back up by 'overlap'
        # so consecutive chunks share a little context
        start = end - overlap
    return chunks

chunks = chunk_text(all_text)
#loads embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
#embeds every chunk
chunk_embeddings = model.encode(chunks)

#setting up chroma
client = chromadb.Client()
collection = client.create_collection(name="equipment_manual")

# add chunks and embeddings to the collection
chunk_ids = [f'chunk_{i}' for i in range(len(chunks))]

collection.add(
    ids = chunk_ids,
    documents = chunks,
    embeddings = chunk_embeddings.tolist()
)

print("Chunks stored in Chroma:", collection.count())

#trying a real search
while True:
    question = input("Ask a question about the manual. enter quit to exit: ")
    if question.strip().lower() == "quit":
        break
    question_embedding = model.encode([question])

    results = collection.query(
        query_embeddings = question_embedding.tolist(),
        n_results=3
    )
    retrieved_chunks = results["documents"][0]

    #building the prompt
    context = "\n\n---]\n\n".join(
        f'[Chunk {i+1}]\n{chunk}' for i, chunk in enumerate(retrieved_chunks)
    )

    system_prompt = (
        "You are a maintenace assistant. answer the technicians question"
        "using ONLY the provided maual excerpts below."
        "if the exceprts dont contain enough information to answer confidently,"
        "say so clearly instead of guessing."
        "when you use information from the exceprt, cite it like [Chunk 1]")

    user_message = f'Manual excerpts:\n\n{context}\n\nQuestion: {question}'

    #calling gemini

    gemini_client = genai.Client() #reads the key automatically

    response = gemini_client.models.generate_content(
        model = "gemini-flash-latest",
        config={"system_instruction": system_prompt},
        contents = user_message
    )

    print("\n---Answer---\n")
    print(response.text)
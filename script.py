import os
import time
import pdfplumber

from openai import OpenAI
from pinecone import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ===================================
# Configuration
# ===================================

# Ollama Embedding Client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# Pinecone Configuration
pinecone_api_key = "pcsk_4fqwU4_UeQomSBptyFoZqrhkw1jXgyW2a7rQKp7vvDP6EtNR4JL5yWYBCmgeS1wYqqpv9h"
index_name = "pharmaa-pdf"


# PDF Folder
pdf_folder = r"C:\Users\Afzal\OneDrive\Desktop\Newfolder"


# Upload Settings
batch_size = 50


# ===================================
# Initialize Pinecone
# ===================================

pc = Pinecone(
    api_key=pinecone_api_key
)

index = pc.Index(index_name)


# ===================================
# Extract PDF Text
# ===================================

def extract_text(file_path):

    text = ""

    try:

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"


        return text


    except Exception as e:

        print(f"Failed reading {file_path}")
        print(e)

        return None



# ===================================
# Create Chunks
# ===================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


all_chunks = []


print("\nReading PDFs...\n")


for filename in os.listdir(pdf_folder):

    if filename.lower().endswith(".pdf"):

        filepath = os.path.join(
            pdf_folder,
            filename
        )


        print("Processing:", filename)


        text = extract_text(filepath)


        if not text:
            continue


        chunks = splitter.split_text(text)


        for i, chunk in enumerate(chunks):

            all_chunks.append({

                "id": f"{filename}-{i}",

                "text": chunk,

                "metadata": {

                    "source": filename

                }

            })



print("\nTotal Chunks:", len(all_chunks))



# ===================================
# Generate Embeddings
# ===================================

def get_embedding(text, retries=3):


    for attempt in range(retries):

        try:

            response = client.embeddings.create(

                model="nomic-embed-text",

                input=text

            )


            return response.data[0].embedding



        except Exception as e:

            print(
                f"\nEmbedding Failed ({attempt+1}/{retries})"
            )

            print(e)


            if attempt < retries - 1:

                print("Retrying...")
                time.sleep(3)



    return None



# ===================================
# Upload to Pinecone
# ===================================

print("\nUploading to Pinecone...\n")


for start in range(
    0,
    len(all_chunks),
    batch_size
):


    batch = all_chunks[
        start:start + batch_size
    ]


    print(
        f"Batch {(start//batch_size)+1}"
    )


    vectors = []


    for item in batch:


        embedding = get_embedding(
            item["text"]
        )


        if embedding is None:

            print(
                "Skipping:",
                item["id"]
            )

            continue



        vectors.append({

            "id": item["id"],

            "values": embedding,

            "metadata": {

                "source": item["metadata"]["source"],

                "text": item["text"]

            }

        })



    if vectors:


        try:

            index.upsert(
                vectors=vectors
            )


            print(
                f"Uploaded {len(vectors)} vectors"
            )


        except Exception as e:

            print("Pinecone Upload Error:")
            print(e)



    time.sleep(1)



print("\n============================")
print("All PDFs uploaded successfully")
print("============================")
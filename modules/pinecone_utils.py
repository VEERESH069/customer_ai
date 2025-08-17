# modules/pinecone_utils.py

from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import streamlit as st

INDEX_NAME = "timeai-assignment"
EMBEDDING_DIMENSION = 384  # Based on 'all-MiniLM-L6-v2'

@st.cache_resource
def get_pinecone_and_embedding_model():
    """Initializes Pinecone connection and the embedding model."""
    try:
        # pinecone_api_key = st.secrets["PINECONE_API_KEY"]
        pinecone_api_key = st.secrets["PINECONE_API_KEY"]
        pc = Pinecone(api_key=pinecone_api_key)
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        return pc, embedding_model
    except Exception as e:
        st.error(f"Failed to initialize Pinecone or embedding model: {e}")
        st.stop()

def initialize_pinecone_index(pc):
    """Checks for the index and creates it if it doesn't exist."""
    if INDEX_NAME not in pc.list_indexes().names():
        st.info(f"Creating new Pinecone index: {INDEX_NAME}. This may take a minute...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(INDEX_NAME)

def upsert_chunks_to_pinecone(index, chunks):
    """Embeds and upserts text chunks into a defined namespace."""
    namespace = "timeai-doc"
    _, embedding_model = get_pinecone_and_embedding_model()
    
    vectors_to_upsert = []
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        vectors_to_upsert.append({
            "id": f"chunk_{i}",
            "values": embedding,
            "metadata": {"text": chunk}
        })
    
    try:
        index.upsert(vectors=vectors_to_upsert, namespace=namespace)
        return True
    except Exception as e:
        st.error(f"Failed to upsert data to Pinecone: {e}")
        return False

def query_pinecone(index, question):
    """Queries Pinecone to get relevant text chunks for a question."""
    namespace = "timeai-doc"
    _, embedding_model = get_pinecone_and_embedding_model()
    
    query_embedding = embedding_model.encode(question).tolist()
    results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True,
        namespace=namespace
    )
    context = "\n".join([match['metadata']['text'] for match in results['matches']])
    return context

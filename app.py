# app.py

import streamlit as st
from PIL import Image
import google.generativeai as genai

from modules.utils import process_pdf, process_video
from modules.pinecone_utils import get_pinecone_and_embedding_model, initialize_pinecone_index, upsert_chunks_to_pinecone, query_pinecone
from modules.gemini_utils import get_gemini_response, PERSONA_PROMPTS, FORMAT_PROMPTS

#  Page Configuration and Initialization 
st.set_page_config(page_title="Creative RAG Agent", layout="wide")

# Initialize connections (this is cached)
try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=google_api_key)
    pc, _ = get_pinecone_and_embedding_model()
    pinecone_index = initialize_pinecone_index(pc)
except Exception as e:
    st.error(f"Initialization failed. Please check your API keys in secrets.toml. Error: {e}")
    st.stop()

# --- UI Layout ---
st.title("🎨 Creative & Modular Multimedia RAG Agent")
st.markdown("An industry-standard application with selectable AI personas and output formats.")

# Initializing session state
if "doc_type" not in st.session_state:
    st.session_state.doc_type = None
if "doc_content" not in st.session_state:
    st.session_state.doc_content = None

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("PDF, Image, or Video", type=["pdf", "png", "jpg", "jpeg", "mp4", "mov"])
    
    if uploaded_file:
        if st.button(f"Process {uploaded_file.name}"):
            st.session_state.doc_type = None # Reset
            file_type = uploaded_file.type
            
            with st.spinner(f"Processing {file_type}..."):
                if "pdf" in file_type:
                    chunks = process_pdf(uploaded_file)
                    if chunks and upsert_chunks_to_pinecone(pinecone_index, chunks):
                        st.session_state.doc_type = "pdf"
                        st.success("PDF processed and indexed.")
                elif "image" in file_type:
                    st.session_state.doc_content = Image.open(uploaded_file)
                    st.session_state.doc_type = "image"
                    st.image(st.session_state.doc_content, caption="Uploaded Image")
                elif "video" in file_type:
                    st.session_state.doc_content = process_video(uploaded_file)
                    st.session_state.doc_type = "video"
                    st.success(f"Video processed. {len(st.session_state.doc_content)} frames ready.")

    # Add the new creative controls
    if st.session_state.doc_type:
        st.divider()
        st.header("2. AI Controls")
        
        # Persona Selector
        persona = st.selectbox(
            "Choose Agent Persona:",
            options=list(PERSONA_PROMPTS.keys())
        )
        
        # Output Format Selector
        output_format = st.selectbox(
            "Choose Output Format:",
            options=list(FORMAT_PROMPTS.keys())
        )

# --- Main Interaction Area ---
st.header("Ask a Question")
question = st.text_input("Enter your question here:", disabled=not st.session_state.doc_type)

if st.button("Get Answer", disabled=not question):
    doc_type = st.session_state.doc_type
    base_prompt = [f"Please answer the following question based on the provided context.\nUser's Question: {question}\n\nContext:\n"]
    
    with st.spinner(f"The {persona} is thinking in {output_format}..."):
        if doc_type == "pdf":
            retrieved_context = query_pinecone(pinecone_index, question)
            base_prompt.append(retrieved_context)
            st.info("Retrieved relevant context from Pinecone.")
        elif doc_type == "image":
            base_prompt.append(st.session_state.doc_content)
        elif doc_type == "video":
            base_prompt.extend(st.session_state.doc_content)
        
        # Call the updated Gemini function with the new parameters
        response = get_gemini_response(base_prompt, persona, output_format)
        
        st.subheader(f"🤖 Answer (from your {persona})")
        
        # Use st.code for JSON to get nice formatting and a copy button
        if output_format == "JSON":
            st.code(response, language="json")
        else:
            st.markdown(response)


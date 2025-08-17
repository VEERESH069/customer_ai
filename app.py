# # app.py

# import streamlit as st
# from PIL import Image
# import google.generativeai as genai

# # Import functions from our modules
# from modules.utils import process_pdf, process_video
# from modules.pinecone_utils import get_pinecone_and_embedding_model, initialize_pinecone_index, upsert_chunks_to_pinecone, query_pinecone
# from modules.gemini_utils import get_gemini_response, PERSONA_PROMPTS, FORMAT_PROMPTS

# # --- Page Configuration and Initialization ---
# st.set_page_config(page_title="Creative RAG Agent by Veeresh", layout="wide")

# # Initialize connections (this is cached)
# try:
#     # google_api_key = st.secrets["GOOGLE_API_KEY"]
#     google_api_key = "AIzaSyB7mY6VvjecZen74hllNIVH1IAvocrDCgw"
#     genai.configure(api_key=google_api_key)
#     pc, _ = get_pinecone_and_embedding_model()
#     pinecone_index = initialize_pinecone_index(pc)
# except Exception as e:
#     st.error(f"Initialization failed. Please check your API keys in secrets.toml. Error: {e}")
#     st.stop()

# # --- UI Layout ---
# st.title("🎨 Creative & Modular Multimedia RAG Agent")
# st.markdown("An industry-standard application with selectable AI personas and output formats.")

# # Initialize session state
# if "doc_type" not in st.session_state:
#     st.session_state.doc_type = None
# if "doc_content" not in st.session_state:
#     st.session_state.doc_content = None

# # --- Sidebar for Controls ---
# with st.sidebar:
#     st.header("1. Upload Document")
#     uploaded_file = st.file_uploader("PDF, Image, or Video", type=["pdf", "png", "jpg", "jpeg", "mp4", "mov"])
    
#     if uploaded_file:
#         if st.button(f"Process {uploaded_file.name}"):
#             st.session_state.doc_type = None # Reset
#             file_type = uploaded_file.type
            
#             with st.spinner(f"Processing {file_type}..."):
#                 if "pdf" in file_type:
#                     chunks = process_pdf(uploaded_file)
#                     if chunks and upsert_chunks_to_pinecone(pinecone_index, chunks):
#                         st.session_state.doc_type = "pdf"
#                         st.success("PDF processed and indexed.")
#                 elif "image" in file_type:
#                     st.session_state.doc_content = Image.open(uploaded_file)
#                     st.session_state.doc_type = "image"
#                     st.image(st.session_state.doc_content, caption="Uploaded Image")
#                 elif "video" in file_type:
#                     st.session_state.doc_content = process_video(uploaded_file)
#                     st.session_state.doc_type = "video"
#                     st.success(f"Video processed. {len(st.session_state.doc_content)} frames ready.")

#     # Add the new creative controls
#     if st.session_state.doc_type:
#         st.divider()
#         st.header("2. AI Controls")
        
#         # Persona Selector
#         persona = st.selectbox(
#             "Choose Agent Persona:",
#             options=list(PERSONA_PROMPTS.keys())
#         )
        
#         # Output Format Selector
#         output_format = st.selectbox(
#             "Choose Output Format:",
#             options=list(FORMAT_PROMPTS.keys())
#         )

# # --- Main Interaction Area ---
# st.header("Ask a Question")
# question = st.text_input("Enter your question here:", disabled=not st.session_state.doc_type)

# if st.button("Get Answer", disabled=not question):
#     doc_type = st.session_state.doc_type
#     base_prompt = [f"Please answer the following question based on the provided context.\nUser's Question: {question}\n\nContext:\n"]
    
#     with st.spinner(f"The {persona} is thinking in {output_format}..."):
#         if doc_type == "pdf":
#             retrieved_context = query_pinecone(pinecone_index, question)
#             base_prompt.append(retrieved_context)
#             st.info("Retrieved relevant context from Pinecone.")
#         elif doc_type == "image":
#             base_prompt.append(st.session_state.doc_content)
#         elif doc_type == "video":
#             base_prompt.extend(st.session_state.doc_content)
        
#         # Call the updated Gemini function with the new parameters
#         response = get_gemini_response(base_prompt, persona, output_format)
        
#         st.subheader(f"🤖 Answer (from your {persona})")
        
#         # Use st.code for JSON to get nice formatting and a copy button
#         if output_format == "JSON":
#             st.code(response, language="json")
#         else:
#             st.markdown(response)


# app.py (Stateful Chat Version)

# app.py (Final Corrected Version)

import streamlit as st
from PIL import Image
import google.generativeai as genai

# Import functions and dictionaries from our modules
from modules.utils import process_pdf, process_video
from modules.pinecone_utils import get_pinecone_and_embedding_model, initialize_pinecone_index, upsert_chunks_to_pinecone, query_pinecone
from modules.gemini_utils import start_chat_session, send_chat_message, PERSONA_PROMPTS, FORMAT_PROMPTS

# --- Page Configuration and Initialization ---
st.set_page_config(page_title="Final AI Agent", layout="wide")

# Initialize connections
try:
    # IMPORTANT: For security, use st.secrets. Hardcoding keys is risky.
    # I've left your hardcoded key here as per your code, but it's not recommended.
    google_api_key = st.secrets["GOOGLE_API_KEY"] # Replace with st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=google_api_key)
    pc, _ = get_pinecone_and_embedding_model()
    pinecone_index = initialize_pinecone_index(pc)
except Exception as e:
    st.error(f"Initialization failed. Please check your API keys. Error: {e}")
    st.stop()

# --- UI Layout ---
st.title("🧠🤖 Advanced Multimedia AI Agent")
st.markdown("This agent remembers your conversation, has selectable personas, and can process PDFs, images, and videos.")

# --- Session State Initialization ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = start_chat_session()
if "doc_processed" not in st.session_state:
    st.session_state.doc_processed = False
if "doc_type" not in st.session_state:
    st.session_state.doc_type = None
if "doc_content" not in st.session_state:
    st.session_state.doc_content = None

# --- A SINGLE, CORRECT SIDEBAR ---
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("PDF, Image, or Video", type=["pdf", "png", "jpg", "jpeg", "mp4", "mov"])
    
    if uploaded_file:
        if st.button(f"Process {uploaded_file.name}"):
            # When a new document is processed, reset the chat and state
            st.session_state.chat_session = start_chat_session()
            st.session_state.doc_processed = False
            st.session_state.doc_type = None
            st.session_state.doc_content = None
            
            file_type = uploaded_file.type
            
            with st.spinner(f"Processing {file_type}..."):
                if "pdf" in file_type:
                    st.session_state.doc_type = "pdf"
                    chunks = process_pdf(uploaded_file)
                    if chunks and upsert_chunks_to_pinecone(pinecone_index, chunks):
                        st.success("PDF processed and indexed.")
                        st.session_state.doc_processed = True
                elif "image" in file_type:
                    st.session_state.doc_type = "image"
                    st.session_state.doc_content = Image.open(uploaded_file)
                    st.success("Image processed.")
                    st.session_state.doc_processed = True
                elif "video" in file_type:
                    st.session_state.doc_type = "video"
                    st.session_state.doc_content = process_video(uploaded_file)
                    st.success(f"Video processed with {len(st.session_state.doc_content)} frames.")
                    st.session_state.doc_processed = True
    
    # Display the creative controls ONLY if a document has been processed
    if st.session_state.doc_processed:
        st.divider()
        st.header("2. AI Controls")
        st.session_state.persona = st.selectbox("Choose Agent Persona:", options=list(PERSONA_PROMPTS.keys()))
        st.session_state.output_format = st.selectbox("Choose Output Format:", options=list(FORMAT_PROMPTS.keys()))

# --- Main Chat Interface ---
st.header("Chat with your Document")

# Display previous messages from history
if hasattr(st.session_state.chat_session, 'history'):
    for message in st.session_state.chat_session.history:
        with st.chat_message(message.role):
            # For now, we assume content is text. A more robust solution would check parts.
            st.markdown(message.parts[0].text)

# Chat input
if prompt := st.chat_input("Ask a question...", disabled=not st.session_state.doc_processed):
    # Display user's new message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare the prompt for the model
    context_prompt = ""
    if st.session_state.doc_type == "pdf":
        retrieved_context = query_pinecone(pinecone_index, prompt)
        context_prompt = f"Based on this context:\n---\n{retrieved_context}\n---\n"
    
    # Get persona and format instructions
    persona_instruction = PERSONA_PROMPTS.get(st.session_state.get("persona", "Helpful Assistant"))
    format_instruction = FORMAT_PROMPTS.get(st.session_state.get("output_format", "Clear Paragraph"))

    # Construct the full prompt
    full_prompt = (
        f"**Instructions**\nPersona: {persona_instruction}\nFormat: {format_instruction}\n\n"
        f"**Context**\n{context_prompt}\n\n"
        f"**Question:**\n{prompt}"
    )
    
    # Add visual content if it exists
    if st.session_state.doc_type in ["image", "video"]:
        final_prompt_parts = [full_prompt]
        if isinstance(st.session_state.doc_content, list):
             final_prompt_parts.extend(st.session_state.doc_content)
        else:
             final_prompt_parts.append(st.session_state.doc_content)
    else:
        final_prompt_parts = full_prompt

    # Get model response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = send_chat_message(st.session_state.chat_session, final_prompt_parts)
            
            if st.session_state.get("output_format") == "JSON":
                st.code(response, language="json")
            else:
                st.markdown(response)

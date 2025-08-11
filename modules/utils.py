


# modules/utils.py

from PyPDF2 import PdfReader
from PIL import Image
import cv2
import tempfile
import os
import streamlit as st

def process_pdf(uploaded_file):
    """Extracts text from a PDF and splits it into chunks."""
    text = ""
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        return chunks
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        return None

def process_video(uploaded_file):
    """Extracts frames from a video file."""
    frames = []
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_file.read())
        temp_file_path = tfile.name
    try:
        video_capture = cv2.VideoCapture(temp_file_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS) or 30
        frame_interval = int(fps * 5)  # 1 frame every 5 seconds
        frame_count = 0
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret: break
            if frame_count % frame_interval == 0:
                frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            frame_count += 1
    finally:
        video_capture.release()
        os.remove(temp_file_path)
    return frames

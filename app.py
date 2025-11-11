import streamlit as st
import requests

# Define FastAPI backend URL
API_URL = "http://localhost:8000"


st.set_page_config(page_title="AI-Powered Presentation Generator", layout="centered")


st.title("AI-Powered Presentation Generator")
st.write("Generate a presentation with AI assistance.")

uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])


if uploaded_file is not None:
    # Upload file to FastAPI backend
    response = requests.post(f"{API_URL}/upload", files={"file": uploaded_file})
    if response.status_code == 200:
        st.success("File uploaded successfully.")
    else:
        st.error("File upload failed.")

if st.button("Generate Presentation"):
    response = requests.get(f"{API_URL}/generate/")
    if response.status_code == 200:
        st.success("Presentation generated successfully.")
        download_url = response.json().get("download_url")
        st.markdown(f"[Download Presentation]({download_url})")
    else:
        st.error("Failed to generate presentation.")
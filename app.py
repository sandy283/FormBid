import streamlit as st
import os
from PIL import Image

CERTIFICATES_DIR = 'uploads/certificates'
DEFECTS_DIR = 'uploads/defects'

os.makedirs(CERTIFICATES_DIR, exist_ok=True)
os.makedirs(DEFECTS_DIR, exist_ok=True)

st.title("Formbid Private Limited")

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

option = st.selectbox("Choose an option:", ["Defective Images", "Test Certificates"])

if option == "Test Certificates":
    uploaded_files = st.file_uploader("Choose files...", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
else:
    uploaded_files = st.file_uploader("Choose images...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.session_state.uploaded_files = [f for f in uploaded_files]

if st.session_state.uploaded_files:
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write("Delete")
    
    with col2:
        st.write("File Name")

    for idx, uploaded_file in enumerate(st.session_state.uploaded_files):
        file_type = uploaded_file.type

        if option == "Test Certificates":
            save_path = os.path.join(CERTIFICATES_DIR, uploaded_file.name)
        elif option == "Defective Images":
            save_path = os.path.join(DEFECTS_DIR, uploaded_file.name)
        
        if not os.path.isfile(save_path):
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        with st.container():
            cols = st.columns([3, 1])
            with cols[0]:
                delete_button_key = f"delete_{uploaded_file.name}_{idx}"
                if st.button("🗑", key=delete_button_key):
                    try:
                        os.remove(save_path)
                        st.session_state.uploaded_files.pop(idx)
                    except Exception as e:
                        st.error(f"Error deleting {uploaded_file.name}: {e}")

                st.write(uploaded_file.name)

            with cols[1]:
                if file_type in ["image/png", "image/jpeg"]:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f'Uploaded: {uploaded_file.name}', use_column_width=True)
                elif file_type == "application/pdf":
                    st.write("PDF files cannot be displayed here")

if st.button("Delete All Files"):
    try:
        for folder in [CERTIFICATES_DIR, DEFECTS_DIR]:
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                os.remove(file_path)
        st.session_state.uploaded_files = []
        st.success("All files deleted.")

    except Exception as e:
        st.error(f"Error deleting files: {e}")

# Proceed button to open page1.py
if st.button("Proceed"):
    if option == "Test Certificates":
        exec(open("page1.py").read())
    
    elif option == "Defective Images":
        exec(open("page2.py").read())
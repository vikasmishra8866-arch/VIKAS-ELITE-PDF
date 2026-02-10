import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import fitz  # PyMuPDF
from PIL import Image
import io

# --- Page Configuration ---
st.set_page_config(page_title="ELITE PDF EDITOR", page_icon="📑", layout="wide")

# --- Professional RGB & Cyberpunk CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #080a0f; color: #ffffff; }
    
    /* Main Title RGB Glow */
    .main-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #00f2ff, #ff00ff, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
        margin-bottom: 50px;
    }

    /* Professional Card Styling */
    .stButton>button {
        width: 100%;
        height: 150px;
        border-radius: 15px;
        border: 2px solid #00f2ff;
        background: rgba(0, 242, 255, 0.05);
        color: #00f2ff;
        font-size: 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton>button:hover {
        background: #00f2ff;
        color: #000;
        box-shadow: 0 0 30px #00f2ff;
        transform: translateY(-5px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #ff00ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="main-title">ELITE PDF EDITOR PRO</div>', unsafe_allow_html=True)

# --- Session State to manage navigation ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

def set_page(name):
    st.session_state.page = name

# --- HOME PAGE (Entry Options) ---
if st.session_state.page == 'Home':
    st.markdown("<h3 style='text-align: center; color: #aaa;'>Select Your Professional Tool</h3><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        if st.button("📝 PDF EDIT"): set_page('Edit')
    with col2:
        if st.button("🔓 PDF UNLOCK"): set_page('Unlock')
    with col3:
        if st.button("🔗 PDF MERGE"): set_page('Merge')
    with col4:
        if st.button("🔒 PDF LOCK"): set_page('Lock')

# --- PDF LOCK MODULE ---
elif st.session_state.page == 'Lock':
    st.subheader("🛡️ Secure Your PDF (Encryption)")
    uploaded_file = st.file_uploader("Upload PDF to Lock", type="pdf")
    password = st.text_input("Set Admin Password:", type="password")
    
    if st.button("Apply Security"):
        if uploaded_file and password:
            reader = PdfReader(uploaded_file)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)
            
            output = io.BytesIO()
            writer.write(output)
            st.success("✅ PDF Locked Successfully!")
            st.download_button("Download Encrypted PDF", data=output.getvalue(), file_name="ELITE_Locked.pdf")
    
    if st.button("Back to Dashboard"): set_page('Home')

# --- PDF MERGE MODULE ---
elif st.session_state.page == 'Merge':
    st.subheader("🔗 Combine Multiple PDFs")
    files = st.file_uploader("Select PDF Files", type="pdf", accept_multiple_files=True)
    
    if st.button("Merge Files"):
        if files:
            merger = PdfMerger()
            for f in files:
                merger.append(f)
            
            output = io.BytesIO()
            merger.write(output)
            st.success(f"✅ {len(files)} Files Merged!")
            st.download_button("Download Merged PDF", data=output.getvalue(), file_name="ELITE_Merged.pdf")
    
    if st.button("Back to Dashboard"): set_page('Home')

# --- PDF EDIT MODULE (Visual Editor Teaser) ---
elif st.session_state.page == 'Edit':
    st.subheader("🖋️ Elite Visual Editor")
    uploaded_file = st.file_uploader("Upload PDF to Modify", type="pdf")
    
    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = doc.load_page(0)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        st.image(img, caption="Page 1 Preview", use_container_width=True)
        st.info("Visual Overlay Tools (Text/Sign) loading in the next module...")

    if st.button("Back to Dashboard"): set_page('Home')

# --- PDF UNLOCK MODULE ---
elif st.session_state.page == 'Unlock':
    st.subheader("🔓 Remove PDF Restrictions")
    uploaded_file = st.file_uploader("Upload Locked PDF", type="pdf")
    pass_attempt = st.text_input("Enter Existing Password:", type="password")
    
    if st.button("Remove Password"):
        if uploaded_file and pass_attempt:
            reader = PdfReader(uploaded_file)
            if reader.decrypt(pass_attempt):
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                output = io.BytesIO()
                writer.write(output)
                st.success("✅ Password Removed!")
                st.download_button("Download Unlocked PDF", data=output.getvalue(), file_name="ELITE_Unlocked.pdf")
            else:
                st.error("❌ Wrong Password!")
                
    if st.button("Back to Dashboard"): set_page('Home')

st.sidebar.markdown("### 🛡️ ELITE STATUS")
st.sidebar.info("Enterprise Grade Encryption Active")
st.sidebar.caption("© 2026 Elite PDF Systems")

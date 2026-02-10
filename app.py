import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

# --- Page Config (Clean White Look) ---
st.set_page_config(page_title="ELITE PDF EDITOR", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #333; }
    .main-title { font-size: 40px; font-weight: bold; color: #2c3e50; text-align: center; margin-bottom: 30px; }
    .stButton>button { border-radius: 5px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'Home'

# --- Dashboard Home ---
if st.session_state.page == 'Home':
    st.markdown('<div class="main-title">ELITE PDF EDITOR</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📝 PDF EDIT"): st.session_state.page = 'Edit'
    with col2:
        if st.button("🔓 PDF UNLOCK"): st.session_state.page = 'Unlock'
    with col3:
        if st.button("🔗 PDF MERGE"): st.session_state.page = 'Merge'
    with col4:
        if st.button("🔒 PDF LOCK"): st.session_state.page = 'Lock'

# --- ACTUAL PDF EDIT MODULE (Visual Editor) ---
elif st.session_state.page == 'Edit':
    st.subheader("📝 Professional Visual Editor")
    uploaded_file = st.file_uploader("Upload PDF to Edit", type="pdf")
    
    if uploaded_file:
        # Load PDF page as image
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page_num = st.sidebar.number_input("Page Select", min_value=1, max_value=len(doc), step=1) - 1
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Toolbar
        drawing_mode = st.sidebar.selectbox("Tool:", ("transform", "rect", "freedraw"))
        text_content = st.sidebar.text_input("Text to Add:", "Bhai ka Editor")
        color = st.sidebar.color_picker("Color", "#000000")

        st.info("💡 Hint: 'transform' mode se aap text ya boxes ko move/resize kar sakte hain.")

        # Interactive Canvas (Real Editing)
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=2,
            stroke_color=color,
            background_image=img,
            update_streamlit=True,
            height=img.height,
            width=img.width,
            drawing_mode=drawing_mode,
            key="pdf_editor",
        )

        if st.button("Export Edited Page"):
            st.success("Page process ho rahi hai... Ye feature full conversion ke liye server-side Python ki demand karta hai.")

    if st.button("Back"): st.session_state.page = 'Home'

# --- PDF LOCK MODULE ---
elif st.session_state.page == 'Lock':
    st.subheader("🔒 Secure Your PDF")
    file = st.file_uploader("PDF Choose Karein", type="pdf")
    pw = st.text_input("Set Password", type="password")
    if st.button("Encrypt"):
        if file and pw:
            pdf_writer = PdfWriter()
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages: pdf_writer.add_page(page)
            pdf_writer.encrypt(pw)
            out = io.BytesIO()
            pdf_writer.write(out)
            st.download_button("Download Locked PDF", out.getvalue(), "locked.pdf")

    if st.button("Back"): st.session_state.page = 'Home'

# --- PDF MERGE MODULE ---
elif st.session_state.page == 'Merge':
    st.subheader("🔗 Merge PDFs")
    files = st.file_uploader("Files Select Karein", type="pdf", accept_multiple_files=True)
    if st.button("Merge Now"):
        merger = PdfMerger()
        for f in files: merger.append(f)
        out = io.BytesIO()
        merger.write(out)
        st.download_button("Download Merged PDF", out.getvalue(), "merged.pdf")
    
    if st.button("Back"): st.session_state.page = 'Home'

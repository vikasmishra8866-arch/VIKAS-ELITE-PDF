import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import tempfile

st.set_page_config(page_title="Professional PDF Editor", layout="wide")
st.title("✨ Professional PDF Editor")
st.markdown("Upload PDF, edit text, adjust size, add signature, aur download karen!")

# Sidebar for instructions
with st.sidebar:
    st.header("Features")
    st.markdown("- Text add/edit")
    st.markdown("- Font size change")
    st.markdown("- Signature image add")
    st.markdown("- Page preview")
    st.markdown("- Download edited PDF")

# File uploader
uploaded_pdf = st.file_uploader("PDF upload karen", type="pdf")
if uploaded_pdf is not None:
    # Save uploaded PDF to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_pdf.read())
        pdf_path = tmp_pdf.name

    doc = fitz.open(pdf_path)
    st.success(f"PDF loaded: {len(doc)} pages")

    # Page selector
    page_num = st.slider("Page select karen", 0, len(doc)-1, 0)

    page = doc[page_num]
    pix = page.get_pixmap()
    img_data = pix.tobytes("png")
    st.image(img_data, caption=f"Page {page_num+1} Preview")

    # Editing tabs
    tab1, tab2, tab3 = st.tabs(["➕ Text Add", "📝 Text Edit", "✍️ Signature Add"])

    with tab1:
        st.subheader("Naya text add karen")
        rect_x = st.slider("X position", 50, 500, 100)
        rect_y = st.slider("Y position", 50, 700, 100)
        rect_w = st.slider("Width", 100, 400, 200)
        rect_h = st.slider("Height", 20, 100, 40)
        new_text = st.text_area("Text enter karen")
        font_size = st.slider("Font size", 8, 36, 12)
        color = st.color_picker("Text color", "#000000")

        if st.button("Text Add", key="add_text"):
            rect = fitz.Rect(rect_x, rect_y, rect_x + rect_w, rect_y + rect_h)
            page.insert_textbox(
                rect, new_text,
                fontsize=font_size,
                color=(int(color[1:3],16)/255, int(color[3:5],16)/255, int(color[5:7],16)/255)
            )
            st.success("Text added!")

    with tab2:
        st.subheader("Existing text edit (search & replace)")
        search_text = st.text_input("Search text")
        replace_text = st.text_input("Replace with")
        new_font_size = st.slider("New font size", 8, 36, 12)

        if st.button("Replace Text", key="replace"):
            text_instances = page.search_for(search_text)
            for inst in text_instances:
                page.add_redact_annot(inst)
                page.apply_redactions()
                rect = inst
                page.insert_textbox(rect, replace_text, fontsize=new_font_size)
            st.success("Text replaced!")

    with tab3:
        st.subheader("Signature add karen")
        signature_img = st.file_uploader("Signature image upload (PNG/JPG)", type=["png", "jpg", "jpeg"])
        sig_x = st.slider("Signature X", 400, 550, 450)
        sig_y = st.slider("Signature Y", 700, 800, 750)
        sig_scale = st.slider("Scale", 0.5, 2.0, 1.0)

        if signature_img and st.button("Signature Add", key="signature"):
            sig_pil = Image.open(signature_img)
            sig_bytes = io.BytesIO()
            sig_pil.save(sig_bytes, format="PNG")
            sig_data = sig_bytes.getvalue()

            # Calculate rect based on scale
            sig_rect = fitz.Rect(sig_x, sig_y, sig_x + 150*sig_scale, sig_y + 50*sig_scale)
            page.insert_image(sig_rect, stream=sig_data)
            st.success("Signature added!")

    # Download button
    if st.button("✅ Edited PDF Download", type="primary"):
        output_bytes = io.BytesIO()
        doc.save(output_bytes)
        st.download_button(
            "Download",
            output_bytes.getvalue(),
            "edited_pdf.pdf",
            "application/pdf"
        )

    doc.close()

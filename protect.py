import streamlit as st
from pdf2image import convert_from_bytes
from fpdf import FPDF
import pikepdf
import os
import uuid

st.set_page_config(page_title="Proteksi PDF Anti Copas", layout="centered")
st.title("🔒 Proteksi PDF Anti Copas")

uploaded_file = st.file_uploader("Upload file PDF kamu", type="pdf")

if uploaded_file is not None:
    with st.spinner("Memproses file..."):
        unique_id = str(uuid.uuid4())
        image_files = []

        # Convert PDF to images
        pages = convert_from_bytes(uploaded_file.read(), dpi=300)
        for i, page in enumerate(pages):
            filename = f"{unique_id}_page_{i + 1}.jpg"
            page.save(filename, "JPEG")
            image_files.append(filename)

        # Create image-only PDF
        pdf = FPDF(unit="mm", format="A4")
        for image in image_files:
            pdf.add_page()
            pdf.image(image, x=0, y=0, w=210, h=297)
        image_pdf_path = f"{unique_id}_image_only.pdf"
        pdf.output(image_pdf_path)

        # Proteksi pakai pikepdf
        protected_pdf_path = f"{unique_id}_final_protected.pdf"
        with pikepdf.open(image_pdf_path) as pdf_file:
            pdf_file.save(
                protected_pdf_path,
                encryption=pikepdf.Encryption(
                    user="",
                    owner="galuh123",
                    allow=pikepdf.Permissions(
                        extract=False,
                        print_lowres=False,
                        print_highres=False
                    ),
                    R=4
                )
            )

        # Cleanup sementara image
        for img in image_files:
            os.remove(img)
        os.remove(image_pdf_path)

        # Download hasil
        with open(protected_pdf_path, "rb") as f:
            st.success("✅ File berhasil diproteksi!")
            st.download_button("📥 Download PDF Terproteksi", f, file_name="anti_copas.pdf")

        os.remove(protected_pdf_path)

import streamlit as st
import io
import tempfile
from pdf2docx import Converter

def convert_zip(zip_file):
    """
    Mengambil file ZIP dan mengembalikan byte data.
    Format .sb3 dan .aia keduanya berbasis struktur ZIP.
    """
    return zip_file.getvalue()

# Konfigurasi Halaman
st.set_page_config(page_title="Multi-Converter App", page_icon="🛠️")

st.title("🛠️ All-in-One Converter")
st.write("Pilih alat konversi yang ingin Anda gunakan melalui tab di bawah ini.")

# Membuat Tabs untuk memisahkan fitur
tab1, tab2 = st.tabs(["📦 ZIP to SB3/AIA", "📄 PDF to Word"])

# ==========================================
# TAB 1: ZIP TO SB3 / AIA CONVERTER
# ==========================================
with tab1:
    st.header("ZIP to SB3/AIA Converter")
    st.write("Unggah file **.zip** Anda untuk diubah menjadi format **.sb3** (Scratch) atau **.aia** (App Inventor).")

    # Pilihan Format Output
    output_format = st.radio(
        "Pilih format tujuan:",
        ('sb3', 'aia'),
        horizontal=True
    )

    # Widget Unggah File ZIP
    uploaded_zip = st.file_uploader("Pilih file ZIP", type="zip")

    if uploaded_zip is not None:
        # Ambil nama file asli tanpa ekstensi
        original_name = uploaded_zip.name.rsplit('.', 1)[0]
        new_filename = f"{original_name}.{output_format}"
        
        # Tentukan MIME type berdasarkan pilihan
        mime_type = "application/x-scratch3" if output_format == "sb3" else "application/zip"
        
        st.success(f"File '{uploaded_zip.name}' siap dikonversi ke {output_format.upper()}!")
        
        # Proses konversi
        converted_data = convert_zip(uploaded_zip)
        
        # Tombol Download
        st.download_button(
            label=f"📥 Download File .{output_format}",
            data=converted_data,
            file_name=new_filename,
            mime=mime_type
        )

    st.divider()

    # Informasi Teknis
    with st.expander("Persyaratan Struktur File"):
        if output_format == "sb3":
            st.info("Untuk **.sb3**: Pastikan di dalam ZIP terdapat file `project.json`.")
        else:
            st.info("Untuk **.aia**: Pastikan ZIP memiliki struktur folder `src`, `assets`, dan file `project.properties` agar bisa dibaca oleh MIT App Inventor.")


# ==========================================
# TAB 2: PDF TO WORD CONVERTER
# ==========================================
with tab2:
    st.header("PDF to Word Converter")
    st.write("Unggah file **.pdf** Anda untuk diubah menjadi dokumen **.docx** (Microsoft Word).")

    # Widget Unggah File PDF
    uploaded_pdf = st.file_uploader("Pilih file PDF", type="pdf")

    if uploaded_pdf is not None:
        original_name = uploaded_pdf.name.rsplit('.', 1)[0]
        new_filename_word = f"{original_name}.docx"

        # Menggunakan st.spinner agar user tahu proses sedang berjalan
        with st.spinner('Sedang mengonversi PDF ke Word... Mohon tunggu.'):
            
            # Membuat file temporary untuk menyimpan PDF sementara
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(uploaded_pdf.getvalue())
                pdf_path = tmp_pdf.name
                
            # Membuat file temporary untuk menampung hasil Word (DOCX)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
                docx_path = tmp_docx.name
                
            try:
                # Proses Konversi menggunakan pdf2docx
                cv = Converter(pdf_path)
                cv.convert(docx_path, start=0, end=None)
                cv.close()
                
                # Membaca kembali file .docx yang sudah jadi ke dalam bentuk byte
                with open(docx_path, "rb") as f:
                    docx_data = f.read()
                    
                st.success("Konversi berhasil! Silakan unduh file Anda di bawah.")
                
                # Tombol Download Word
                st.download_button(
                    label="📥 Download File .docx",
                    data=docx_data,
                    file_name=new_filename_word,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan saat konversi: {e}")

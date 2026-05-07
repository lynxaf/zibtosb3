import streamlit as st
import io

def convert_file(zip_file):
    """
    Mengambil file ZIP dan mengembalikan byte data.
    Format .sb3 dan .aia keduanya berbasis struktur ZIP.
    """
    return zip_file.getvalue()

# Konfigurasi Halaman
st.set_page_config(page_title="Project Converter", page_icon="🛠️")

st.title("📦 ZIP to SB3/AIA Converter")
st.write("Unggah file **.zip** Anda untuk diubah menjadi format **.sb3** (Scratch) atau **.aia** (App Inventor).")

# Pilihan Format Output
output_format = st.radio(
    "Pilih format tujuan:",
    ('sb3', 'aia'),
    horizontal=True
)

# Widget Unggah File
uploaded_file = st.file_uploader("Pilih file ZIP", type="zip")

if uploaded_file is not None:
    # Ambil nama file asli tanpa ekstensi
    original_name = uploaded_file.name.rsplit('.', 1)[0]
    new_filename = f"{original_name}.{output_format}"
    
    # Tentukan MIME type berdasarkan pilihan
    mime_type = "application/x-scratch3" if output_format == "sb3" else "application/zip"
    
    st.success(f"File '{uploaded_file.name}' siap dikonversi ke {output_format.upper()}!")
    
    # Proses konversi
    converted_data = convert_file(uploaded_file)
    
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
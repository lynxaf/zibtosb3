import streamlit as st
import io

def convert_zip_to_sb3(zip_file):
    """
    Mengambil file ZIP dan mengembalikan byte data untuk file SB3.
    Secara teknis hanya membaca ulang konten karena strukturnya identik.
    """
    # Membaca file yang diunggah ke dalam memory
    file_bytes = zip_file.getvalue()
    return file_bytes

# Konfigurasi Halaman
st.set_page_config(page_title="ZIP to SB3 Converter", page_icon="🐱")

st.title("📦 ZIP to SB3 Converter")
st.write("Unggah file **.zip** Anda untuk diubah menjadi format **.sb3** Scratch.")

# Widget Unggah File
uploaded_file = st.file_uploader("Pilih file ZIP", type="zip")

if uploaded_file is not None:
    # Ambil nama file asli tanpa ekstensi
    original_name = uploaded_file.name.rsplit('.', 1)[0]
    new_filename = f"{original_name}.sb3"
    
    st.success(f"File '{uploaded_file.name}' berhasil diunggah!")
    
    # Proses konversi (membaca byte)
    sb3_data = convert_zip_to_sb3(uploaded_file)
    
    # Tombol Download
    st.download_button(
        label="📥 Download File .sb3",
        data=sb3_data,
        file_name=new_filename,
        mime="application/x-scratch3"
    )

st.divider()
st.info("Catatan: Pastikan file ZIP Anda berisi struktur proyek Scratch yang valid (terdapat file project.json di dalamnya).")
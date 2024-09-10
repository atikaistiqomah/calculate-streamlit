import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Aplikasi Perhitungan dengan Tabel Hasil dan Visualisasi Grafik")

# Deskripsi aplikasi
st.write("Masukkan beberapa set angka untuk melakukan perhitungan, dan lihat hasilnya dalam bentuk tabel dan grafik.")

# Inisialisasi session_state untuk menyimpan data jika belum ada
if 'data' not in st.session_state:
    st.session_state.data = {'Nama Perhitungan': [], 'Hasil': [], 'Operasi': [], 'Kategori': []}

# Input dari user melalui form
with st.form(key='input_form'):
    # Input nama perhitungan
    nama_perhitungan = st.text_input("Masukkan nama perhitungan", value="Perhitungan 1")

    # Input angka pertama
    angka1 = st.number_input("Masukkan angka pertama", value=0)

    # Input angka kedua
    angka2 = st.number_input("Masukkan angka kedua", value=0)

    # Input radio button untuk memilih operasi matematika
    operasi = st.radio("Pilih operasi", ('Penjumlahan', 'Pengurangan', 'Perkalian', 'Pembagian'))

    # Input dropdown untuk memilih kategori
    kategori = st.selectbox("Pilih kategori perhitungan", ("Kategori A", "Kategori B", "Kategori C"))

    # Tombol untuk submit form
    submit_button = st.form_submit_button(label='Hitung')

# Logika perhitungan setelah form disubmit
if submit_button:
    # Melakukan perhitungan sesuai operasi yang dipilih
    if operasi == 'Penjumlahan':
        hasil = angka1 + angka2
    elif operasi == 'Pengurangan':
        hasil = angka1 - angka2
    elif operasi == 'Perkalian':
        hasil = angka1 * angka2
    elif operasi == 'Pembagian':
        hasil = angka1 / angka2 if angka2 != 0 else 0  # Menghindari pembagian dengan nol

    # Menyimpan hasil ke dalam session_state
    st.session_state.data['Nama Perhitungan'].append(nama_perhitungan)
    st.session_state.data['Hasil'].append(hasil)
    st.session_state.data['Operasi'].append(operasi)
    st.session_state.data['Kategori'].append(kategori)

    # Menampilkan hasil perhitungan
    st.write(f"Hasil {nama_perhitungan} ({kategori} - {operasi}): {hasil}")

# Jika sudah ada data, tampilkan tabel dan grafik
if st.session_state.data['Nama Perhitungan']:
    df = pd.DataFrame(st.session_state.data)

    # Tampilkan dataframe hasil perhitungan dalam bentuk tabel
    st.write("Tabel Hasil Perhitungan:")
    st.table(df)

    # Grafik rata-rata hasil per kategori
    df_mean = df.groupby(['Kategori', 'Nama Perhitungan'])['Hasil'].mean().reset_index()

    st.write("Rata-rata Hasil Perhitungan per Kategori dan Nama Perhitungan:")

    # Plotting grafik bar
    fig, ax = plt.subplots(figsize=(10, 6))
    for kategori in df_mean['Kategori'].unique():
        df_kategori = df_mean[df_mean['Kategori'] == kategori]
        ax.bar(df_kategori['Nama Perhitungan'] + ' (' + kategori + ')', df_kategori['Hasil'], label=kategori)

    ax.set_xlabel("Nama Perhitungan (Kategori)")
    ax.set_ylabel("Rata-rata Hasil")
    ax.set_title("Grafik Bar Rata-rata Hasil Perhitungan per Kategori")
    ax.legend(title="Kategori")
    plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)

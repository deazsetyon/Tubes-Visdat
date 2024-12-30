import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("TingkatKemiskinan.csv", sep=';')

# Rename Column dan Rubah Tipe Data
df = df.rename(columns={'Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota (Persen)': 'Persentasi Penduduk Miskin Tiap Kota', 
                        'Rata-rata Lama Sekolah Penduduk 15+ (Tahun)': 'Rata-rata Lama Sekolah', 
                        'Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun)': 'Pengeluaran per Kapita',
                        'Umur Harapan Hidup (Tahun)': 'Umur Harapan Hidup'
                        })
df['Persentasi Penduduk Miskin Tiap Kota'] = df['Persentasi Penduduk Miskin Tiap Kota'].str.replace(',', '.').astype(float)
df['Rata-rata Lama Sekolah'] = df['Rata-rata Lama Sekolah'].str.replace(',', '.').astype(float)
df['Indeks Pembangunan Manusia'] = df['Indeks Pembangunan Manusia'].str.replace(',', '.').astype(float)
df['Umur Harapan Hidup'] = df['Umur Harapan Hidup'].str.replace(',', '.').astype(float)
df['Persentase rumah tangga yang memiliki akses terhadap sanitasi layak'] = df['Persentase rumah tangga yang memiliki akses terhadap sanitasi layak'].str.replace(',', '.').astype(float)
df['Persentase rumah tangga yang memiliki akses terhadap air minum layak'] = df['Persentase rumah tangga yang memiliki akses terhadap air minum layak'].str.replace(',', '.').astype(float)
df['Tingkat Pengangguran Terbuka'] = df['Tingkat Pengangguran Terbuka'].str.replace(',', '.').astype(float)
df['Tingkat Partisipasi Angkatan Kerja'] = df['Tingkat Partisipasi Angkatan Kerja'].str.replace(',', '.').astype(float)


# SIDEBAR
st.sidebar.title("Kelompok 4")
st.sidebar.text("1. Deaz Setyo Nugroho (1301210248)\n2. Fadli Dwi Ramadhan (1301210062)\n3. M. Gazell Arafi Asmara (1301210317)")

# FILTERS
province_filter = st.sidebar.selectbox(
    "Pilih Provinsi:",
    options=["Seluruh Provinsi"] + list(df['Provinsi'].unique())
)


# MAIN PAGE
st.title("Tingkat Kemiskinan di Indonesia")
st.image("dataset_cover.jpeg", use_container_width=True)
st.markdown("[Dataset](https://www.kaggle.com/datasets/ermila/klasifikasi-tingkat-kemiskinan-di-indonesia)")
st.text("Sebagai upaya memahami kondisi sosial-ekonomi masyarakat, tingkat kemiskinan menjadi salah satu indikator penting yang diperhatikan. Berdasarkan data dari Badan Pusat Statistik (BPS), dashboard ini dirancang untuk memberikan gambaran mengenai tingkat kemiskinan di berbagai wilayah Indonesia. Relevansi tema ini sangat tinggi mengingat kemiskinan masih menjadi tantangan utama yang perlu diatasi untuk mewujudkan kesejahteraan dan keadilan sosial di Indonesia.")

st.title("Eksplorasi Dataset")



if province_filter != "Seluruh Provinsi":
    st.subheader("Ringkasan Statistik")
    filtered_df = df[df["Provinsi"] == province_filter]
    st.write(f"Total Baris: {filtered_df.shape[0]} | Total Kolom: {filtered_df.shape[1]}")
    st.table(filtered_df.describe())

    st.subheader(f"Dataset {province_filter.title()}")
    st.write(filtered_df)
    st.subheader("Visualisasi Data")

    
    bar_fig_PPMTP1 = px.bar(
        filtered_df,
        x="Kab/Kota",
        y="Persentasi Penduduk Miskin Tiap Kota",
        title=f"Persentasi Penduduk Miskin Tiap Kota di Provinsi {province_filter.title()}",
        labels={"Persentasi Penduduk Miskin Tiap Kota": "Persentase"}
    )
    st.plotly_chart(bar_fig_PPMTP1)

    bar_fig_PPK1 = px.bar(
        filtered_df,
        x="Kab/Kota",
        y="Pengeluaran per Kapita",
        title=f"Pengeluaran per Kapita Tiap Kota di Provinsi {province_filter.title()}",
        labels={"Pengeluaran per Kapita": "Pengeluaran"},
    )
    st.plotly_chart(bar_fig_PPK1)

    bar_fig_TPT1 = px.bar(
        filtered_df,
        x="Kab/Kota",
        y="Tingkat Pengangguran Terbuka",
        title=f"Tingkat Pengangguran Tiap Kota di Provinsi {province_filter.title()}",
        labels={"Tingkat Pengangguran Terbuka": "Tingkat Pengangguran"},
    )
    st.plotly_chart(bar_fig_TPT1)

    bar_fig_TPA1 = px.bar(
        filtered_df,
        x="Kab/Kota",
        y="Tingkat Partisipasi Angkatan Kerja",
        title=f"Tingkat Partisipasi Angkatan Kerja Tiap Kota di Provinsi {province_filter.title()}",
        labels={"Tingkat Partisipasi Angkatan Kerja": "Tingkat Partisipasi"},
    )
    st.plotly_chart(bar_fig_TPA1)

    # Klasifikasi Kemiskinan
    filtered_df2 = filtered_df.copy()
    filtered_df2['Klasifikasi Kemiskinan'] = filtered_df2['Klasifikasi Kemiskinan'].astype(object)
    filtered_df2['Klasifikasi Kemiskinan'] = filtered_df2['Klasifikasi Kemiskinan'].replace({0: 'Non-Miskin', 1: 'Miskin'})

    result = filtered_df2['Klasifikasi Kemiskinan'].value_counts().reset_index()
    result.columns = ['Klasifikasi Kemiskinan', 'Jumlah']

    # Visualisasi Pie Chart
    bar_fig_KK1 = px.pie(
        result,
        names='Klasifikasi Kemiskinan',
        values='Jumlah',
        title=f'Distribusi Klasifikasi Kemiskinan di {province_filter.title()}',
        color='Klasifikasi Kemiskinan',  # Warna berdasarkan kategori
        color_discrete_map={'Non-Miskin': 'blue', 'Miskin': 'red'}  # Warna: 0 = biru, 1 = merah
    )
    st.plotly_chart(bar_fig_KK1)

else: 
    st.write(f"Total Baris: {df.shape[0]} | Total Kolom: {df.shape[1]}")
    st.table(df.describe())

    st.subheader(f"Dataset {province_filter.title()}")
    st.write(df)
    st.subheader("Visualisasi Data")

    # Gruping Tiap Provinsi
    grouped = df.groupby('Provinsi').agg({
        'Persentasi Penduduk Miskin Tiap Kota': 'mean',  # Rata-rata pendapatan per provinsi
        'Rata-rata Lama Sekolah': 'mean',            # Total pengeluaran per provinsi
        'Pengeluaran per Kapita':'mean',
        'Indeks Pembangunan Manusia':'mean',
        'Umur Harapan Hidup':'mean',
        'Persentase rumah tangga yang memiliki akses terhadap sanitasi layak':'mean',
        'Persentase rumah tangga yang memiliki akses terhadap air minum layak':'mean',
        'Tingkat Pengangguran Terbuka':'mean',
        'Tingkat Partisipasi Angkatan Kerja':'mean',
        'PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)':'mean'
    }).reset_index()

    # Klasifikasi Kemiskinan
    klasifikasi_kemiskinan = df.groupby('Provinsi')['Klasifikasi Kemiskinan'].value_counts().unstack(fill_value=0)
    klasifikasi_kemiskinan.columns = ['Non-Miskin', 'Miskin']
    result = klasifikasi_kemiskinan.reset_index()
    
    # VISUALISASI
    bar_fig_PPMTP2 = px.bar(
        grouped,
        x="Provinsi",
        y="Persentasi Penduduk Miskin Tiap Kota",
        title="Rata-rata Persentasi Penduduk Miskin Tiap Provinsi di Indonesia",
        labels={"Persentasi Penduduk Miskin Tiap Kota": "Persentase"},
    )
    st.plotly_chart(bar_fig_PPMTP2)

    bar_fig_RLS2 = px.bar(
        grouped,
        x="Provinsi",
        y="Rata-rata Lama Sekolah",
        title="Rata-rata Lama Sekolah Tiap Provinsi di Indonesia",
        labels={"Rata-rata Lama Sekolah": "Rata-rata"},
    )
    st.plotly_chart(bar_fig_RLS2)

    bar_fig_PPK2 = px.bar(
        grouped,
        x="Provinsi",
        y="Pengeluaran per Kapita",
        title="Rata-rata Pengeluaran per Kapita Tiap Provinsi di Indonesia",
        labels={"Pengeluaran per Kapita": "Pengeluaran"},
    )
    st.plotly_chart(bar_fig_PPK2)

    bar_fig_IPM2 = px.bar(
        grouped,
        x="Provinsi",
        y="Indeks Pembangunan Manusia",
        title="Rata-rata Indeks Pembangunan Manusia Tiap Provinsi di Indonesia",
        # labels={"Indeks Pembangunan Manusia": "Pengeluaran"},
    )
    st.plotly_chart(bar_fig_IPM2)
    
    bar_fig_UHH2 = px.bar(
        grouped,
        x="Provinsi",
        y="Umur Harapan Hidup",
        title="Rata-rata Umur Harapan Hidup Tiap Provinsi di Indonesia",
        labels={"Umur Harapan Hidup": "Umur"},
    )
    st.plotly_chart(bar_fig_UHH2)
    
    bar_fig_PRT1 = px.bar(
        grouped,
        x="Provinsi",
        y="Persentase rumah tangga yang memiliki akses terhadap sanitasi layak",
        title="Rata-rata Persentase rumah tangga yang memiliki sanitasi layak Tiap Provinsi di Indonesia",
        labels={"Persentase rumah tangga yang memiliki akses terhadap sanitasi layak": "Persentase"},
    )
    st.plotly_chart(bar_fig_PRT1)
    
    bar_fig_PRT2 = px.bar(
        grouped,
        x="Provinsi",
        y="Persentase rumah tangga yang memiliki akses terhadap air minum layak",
        title="Rata-rata Persentase rumah tangga yang memiliki air minum layak Tiap Provinsi di Indonesia",
        labels={"Persentase rumah tangga yang memiliki akses terhadap air minum layak": "Persentase"},
    )
    st.plotly_chart(bar_fig_PRT2)
    
    bar_fig_TPT2 = px.bar(
        grouped,
        x="Provinsi",
        y="Tingkat Pengangguran Terbuka",
        title="Rata-rata Tingkat Pengangguran Tiap Provinsi di Indonesia",
        labels={"Tingkat Pengangguran Terbuka": "Tingkat Pengangguran"},
    )
    st.plotly_chart(bar_fig_TPT2)
    
    bar_fig_TPA2 = px.bar(
        grouped,
        x="Provinsi",
        y="Tingkat Partisipasi Angkatan Kerja",
        title="Rata-rata Tingkat Partisipasi Angkatan Kerja Tiap Provinsi di Indonesia",
        labels={"Tingkat Partisipasi Angkatan Kerja": "Tingkat Partisipasi"},
    )
    st.plotly_chart(bar_fig_TPA2)
    
    bar_fig_PDRB2 = px.bar(
        grouped,
        x="Provinsi",
        y="PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)",
        title="Rata-rata PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah) Tiap Provinsi di Indonesia",
        labels={"PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)": "PDRB"},
    )
    st.plotly_chart(bar_fig_PDRB2)


    # Ubah data menjadi bentuk long untuk visualisasi
    long_result = result.melt(id_vars='Provinsi', 
                            value_vars=['Non-Miskin', 'Miskin'], 
                            var_name='Klasifikasi', 
                            value_name='Jumlah')

    # Visualisasi bar chart
    bar_fig_KK2 = px.bar(
        long_result,
        x='Provinsi',
        y='Jumlah',
        color='Klasifikasi',
        barmode='group',
        title='Jumlah Klasifikasi Kemiskinan Tiap Provinsi di Indonesia',
        labels={'Jumlah': 'Jumlah', 'Provinsi': 'Provinsi'},
        color_discrete_map={'Non-Miskin': 'blue', 'Miskin': 'red'}
    )
    st.plotly_chart(bar_fig_KK2)

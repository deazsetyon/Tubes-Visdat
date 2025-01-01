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
st.markdown("""
        <div style="text-align: justify;">
            Sebagai upaya memahami kondisi sosial-ekonomi masyarakat, tingkat kemiskinan menjadi salah satu indikator penting yang diperhatikan. Berdasarkan data dari Badan Pusat Statistik (BPS), dashboard ini dirancang untuk memberikan gambaran mengenai tingkat kemiskinan di berbagai wilayah Indonesia. Relevansi tema ini sangat tinggi mengingat kemiskinan masih menjadi tantangan utama yang perlu diatasi untuk mewujudkan kesejahteraan dan keadilan sosial di Indonesia.
        </div>
        """, unsafe_allow_html=True)

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
        labels={"Persentasi Penduduk Miskin Tiap Kota": "Persentase (%)"}
    )
    st.plotly_chart(bar_fig_PPMTP1)

    bar_fig_PPK1 = px.bar(
        filtered_df,
        x="Kab/Kota",
        y="Pengeluaran per Kapita",
        title=f"Pengeluaran per Kapita Tiap Kota di Provinsi {province_filter.title()}",
        labels={"Pengeluaran per Kapita": "Pengeluaran per Kapita (k = Juta)"},
    )
    st.plotly_chart(bar_fig_PPK1)

    bar_fig_TPT1 = px.bar(
        filtered_df,
        x="Kab/Kota",
        y="Tingkat Pengangguran Terbuka",
        title=f"Tingkat Pengangguran Tiap Kota di Provinsi {province_filter.title()}",
        labels={"Tingkat Pengangguran Terbuka": "Tingkat Pengangguran (%)"},
    )
    st.plotly_chart(bar_fig_TPT1)

    bar_fig_TPA1 = px.bar(
        filtered_df,
        x="Kab/Kota",
        y="Tingkat Partisipasi Angkatan Kerja",
        title=f"Tingkat Partisipasi Angkatan Kerja Tiap Kota di Provinsi {province_filter.title()}",
        labels={"Tingkat Partisipasi Angkatan Kerja": "Tingkat Partisipasi (%)"},
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
        labels={"Persentasi Penduduk Miskin Tiap Kota": "Persentase (%)"},
    )
    st.plotly_chart(bar_fig_PPMTP2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang diatas menunjukkan rata-rata persentase penduduk miskin di setiap provinsi di Indonesia. Mayoritas provinsi memiliki persentase kemiskinan yang berkisar antara 5% hingga 15%. Namun, terdapat beberapa provinsi yang menonjol dengan angka kemiskinan lebih tinggi, seperti Papua dan Papua Barat, yang masing-masing mencatatkan angka di atas 20%. Hal ini mengindikasikan adanya tantangan besar dalam pemerataan pembangunan dan kesejahteraan di wilayah tersebut.
        </div>
        """, unsafe_allow_html=True)

    bar_fig_RLS2 = px.bar(
        grouped,
        x="Provinsi",
        y="Rata-rata Lama Sekolah",
        title="Rata-rata Lama Sekolah Tiap Provinsi di Indonesia",
        labels={"Rata-rata Lama Sekolah": "Rata-rata (Tahun)"},
    )
    st.plotly_chart(bar_fig_RLS2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata lama sekolah tiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan rata-rata lama sekolah antara 8 hingga 9 tahun, yang setara dengan tingkat pendidikan SMP/sederajat. Provinsi seperti DKI Jakarta memiliki rata-rata lama sekolah yang lebih tinggi. Rata-rata lama sekolah ini menunjukkan tingkat pendidikan formal yang ditempuh oleh penduduk di masing-masing provinsi, yang dapat menjadi indikator kualitas sumber daya manusia di wilayah tersebut.
        </div>
        """, unsafe_allow_html=True)

    bar_fig_PPK2 = px.bar(
        grouped,
        x="Provinsi",
        y="Pengeluaran per Kapita",
        title="Rata-rata Pengeluaran per Kapita Tiap Provinsi di Indonesia",
        labels={"Pengeluaran per Kapita": "Pengeluaran",'Pengeluaran per Kapita':'Pengeluaran per Kapita (k = Juta)'},
    )
    st.plotly_chart(bar_fig_PPK2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata pengeluaran per kapita di setiap provinsi di Indonesia. Secara umum, mayoritas provinsi memiliki rata-rata pengeluaran yang berada di kisaran menengah, yaitu sekitar 7.000.000 hingga 12.000.000. Namun, terdapat beberapa provinsi yang menonjol dengan pengeluaran yang lebih tinggi, seperti DKI Jakarta, yang mencatatkan angka di atas 15.000.000. Hal ini mencerminkan adanya disparitas ekonomi antar wilayah, yang dapat diakibatkan oleh perbedaan tingkat pembangunan, pendapatan per kapita, dan akses terhadap layanan publik.
        </div>
        """, unsafe_allow_html=True)

    bar_fig_IPM2 = px.bar(
        grouped,
        x="Provinsi",
        y="Indeks Pembangunan Manusia",
        title="Rata-rata Indeks Pembangunan Manusia Tiap Provinsi di Indonesia",
        labels={"Indeks Pembangunan Manusia": "Indeks Pembangunan Manusia (%)"},
    )
    st.plotly_chart(bar_fig_IPM2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata Indeks Pembangunan Manusia (IPM) di setiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan nilai IPM pada rentang 65% hingga 75%. Beberapa provinsi, seperti DKI Jakarta dan DI Yogyakarta, memiliki IPM yang lebih tinggi mencapai sekitar 80%. Nilai IPM ini mencerminkan tingkat kesejahteraan dan kualitas hidup masyarakat di masing-masing provinsi, yang diukur dari aspek kesehatan, pendidikan, dan standar hidup layak. Sementara itu, beberapa provinsi seperti Papua Barat menunjukkan IPM yang relatif lebih rendah, mengindikasikan masih perlunya upaya peningkatan pembangunan manusia di wilayah tersebut.
        </div>
        """, unsafe_allow_html=True)
    
    bar_fig_UHH2 = px.bar(
        grouped,
        x="Provinsi",
        y="Umur Harapan Hidup",
        title="Rata-rata Umur Harapan Hidup Tiap Provinsi di Indonesia",
        labels={"Umur Harapan Hidup": "Umur (Tahun)"},
    )
    st.plotly_chart(bar_fig_UHH2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata umur harapan hidup di setiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan umur harapan hidup pada rentang 60 hingga 65 tahun. Beberapa provinsi, seperti DKI Jakarta, DI Yogyakarta, dan Jawa Tengah, memiliki umur harapan hidup yang lebih tinggi mendekati 75 tahun. Angka harapan hidup ini mencerminkan perkiraan rata-rata lamanya hidup yang akan dicapai oleh penduduk di masing-masing provinsi, yang dipengaruhi oleh berbagai faktor seperti kualitas kesehatan, gizi, dan lingkungan.
        </div>
        """, unsafe_allow_html=True)
    
    bar_fig_PRT1 = px.bar(
        grouped,
        x="Provinsi",
        y="Persentase rumah tangga yang memiliki akses terhadap sanitasi layak",
        title="Rata-rata Persentase rumah tangga yang memiliki sanitasi layak Tiap Provinsi di Indonesia",
        labels={"Persentase rumah tangga yang memiliki akses terhadap sanitasi layak": "Persentase (%)"},
    )
    st.plotly_chart(bar_fig_PRT1)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata persentase rumah tangga yang memiliki sanitasi layak di setiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan persentase sanitasi layak pada rentang 70% hingga 80%. Beberapa provinsi, seperti Bali, DI Yogyakarya dan DKI Jakarta, memiliki persentase yang sangat baik mencapai lebih dari 90%. Namun, terdapat kesenjangan yang cukup signifikan dimana beberapa provinsi seperti Papua memiliki persentase yang relatif rendah, hanya sekitar 40%. Data ini mencerminkan tingkat akses masyarakat terhadap fasilitas sanitasi yang memenuhi standar kesehatan di masing-masing provinsi, yang merupakan salah satu indikator penting dalam kesejahteraan dan kesehatan masyarakat.
        </div>
        """, unsafe_allow_html=True)
    
    bar_fig_PRT2 = px.bar(
        grouped,
        x="Provinsi",
        y="Persentase rumah tangga yang memiliki akses terhadap air minum layak",
        title="Rata-rata Persentase rumah tangga yang memiliki air minum layak Tiap Provinsi di Indonesia",
        labels={"Persentase rumah tangga yang memiliki akses terhadap air minum layak": "Persentase (%)"},
    )
    st.plotly_chart(bar_fig_PRT2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata persentase rumah tangga yang memiliki akses air minum layak di setiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan persentase akses air minum layak pada rentang 75% hingga 90%. Beberapa provinsi, seperti Bali, DI Yogyakarta, dan DKI Jakarta, memiliki persentase yang sangat baik mencapai lebih dari 95%. Namun, terdapat beberapa provinsi seperti Bengkulu, dan Papua yang memiliki persentase relatif lebih rendah, sekitar 65%. Data ini mencerminkan tingkat akses masyarakat terhadap sumber air minum yang memenuhi standar kesehatan di masing-masing provinsi, yang merupakan salah satu kebutuhan dasar dan indikator penting dalam kualitas hidup masyarakat.
        </div>
        """, unsafe_allow_html=True)
    
    bar_fig_TPT2 = px.bar(
        grouped,
        x="Provinsi",
        y="Tingkat Pengangguran Terbuka",
        title="Rata-rata Tingkat Pengangguran Tiap Provinsi di Indonesia",
        labels={"Tingkat Pengangguran Terbuka": "Tingkat Pengangguran (%)"},
    )
    st.plotly_chart(bar_fig_TPT2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata tingkat pengangguran di setiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan tingkat pengangguran yang berada pada kisaran 4% hingga 6%. Namun, ada beberapa provinsi yang menonjol dengan tingkat pengangguran yang lebih tinggi, seperti Banten, DKI Jakarta, dan Jawa Barat, yang mencatatkan angka di atas 8%. Hal ini menunjukkan adanya tantangan dalam penyediaan lapangan kerja yang merata di seluruh wilayah Indonesia. Provinsi dengan tingkat pengangguran tinggi mungkin menghadapi kendala seperti kepadatan penduduk, urbanisasi yang pesat, atau kurangnya investasi di sektor-sektor yang menciptakan banyak lapangan kerja.
        </div>
        """, unsafe_allow_html=True)
    
    bar_fig_TPA2 = px.bar(
        grouped,
        x="Provinsi",
        y="Tingkat Partisipasi Angkatan Kerja",
        title="Rata-rata Tingkat Partisipasi Angkatan Kerja Tiap Provinsi di Indonesia",
        labels={"Tingkat Partisipasi Angkatan Kerja": "Tingkat Partisipasi (%)"},
    )
    st.plotly_chart(bar_fig_TPA2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata tingkat partisipasi angkatan kerja (TPAK) di setiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan tingkat partisipasi angkatan kerja pada rentang 60% hingga 70%. Beberapa provinsi, seperti Papua, Bali, dan Nusa Tenggara Timur, memiliki TPAK yang lebih tinggi, mendekati atau bahkan melebihi 75%. Tingkat partisipasi angkatan kerja yang tinggi menunjukkan banyaknya penduduk usia kerja yang aktif secara ekonomi, baik bekerja maupun mencari kerja.
        </div>
        """, unsafe_allow_html=True)
    
    bar_fig_PDRB2 = px.bar(
        grouped,
        x="Provinsi",
        y="PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)",
        title="Rata-rata PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah) Tiap Provinsi di Indonesia",
        labels={"PDRB atas Dasar Harga Konstan menurut Pengeluaran (Rupiah)": "PDRB"},
    )
    st.plotly_chart(bar_fig_PDRB2)
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan rata-rata PDRB (Produk Domestik Regional Bruto) atas dasar harga konstan menurut pengeluaran di setiap provinsi di Indonesia. Sebagian besar provinsi mencatatkan PDRB di bawah 50M Rupiah, namun terdapat provinsi yang menunjukkan nilai yang jauh lebih tinggi. DKI Jakarta mencatatkan PDRB tertinggi mencapai sekitar 300M Rupiah, diikuti oleh beberapa provinsi seperti Banten dan Jawa Barat yang memiliki PDRB di kisaran 50M Rupiah. Data ini mencerminkan tingkat aktivitas ekonomi dan nilai tambah yang dihasilkan oleh masing-masing provinsi, yang menunjukkan adanya kesenjangan ekonomi yang cukup signifikan antar wilayah di Indonesia.
        </div>
        """, unsafe_allow_html=True)


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
    st.markdown("""
        <div style="text-align: justify;">
            Diagram batang di atas menunjukkan jumlah klasifikasi kemiskinan di setiap provinsi di Indonesia yang terbagi menjadi kategori miskin dan non-miskin. Sebagian besar provinsi mencatatkan jumlah klasifikasi non-miskin yang lebih dominan dibandingkan klasifikasi miskin. Beberapa provinsi, seperti Jawa Tengah dan Jawa Timur, memiliki jumlah klasifikasi non-miskin tertinggi yang mencapai sekitar 35. Sementara itu, provinsi-provinsi di wilayah timur Indonesia cenderung memiliki jumlah klasifikasi yang lebih rendah. Tingginya jumlah klasifikasi non-miskin di beberapa provinsi menunjukkan adanya perkembangan positif dalam upaya pengentasan kemiskinan, meskipun masih terdapat beberapa provinsi yang memiliki jumlah klasifikasi miskin yang cukup signifikan.
        </div>
        """, unsafe_allow_html=True)

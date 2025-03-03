import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Pengaturan halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

@st.cache_data
def load_data():
    """Load dataset utama dari main_data.csv."""
    df = pd.read_csv("main_data.csv")
    
    # Jika kolom 'dteday' ada, konversi ke datetime
    if 'dteday' in df.columns:
        df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Buat kategori Rush Hour vs Non-Rush Hour jika belum ada
    if 'hr' in df.columns and 'time_category' not in df.columns:
        df['time_category'] = df['hr'].apply(
            lambda x: "Rush Hour" if x in range(6,10) or x in range(16,20) 
            else "Non-Rush Hour"
        )
    return df

# Load data
df = load_data()

# ================== SIDEBAR UNTUK FILTER ===================
st.sidebar.title("Bike Sharing Filters")

# Filter Tahun (jika kolom 'yr' ada)
if 'yr' in df.columns:
    unique_years = sorted(df['yr'].unique())
    selected_years = st.sidebar.multiselect(
        "Pilih Tahun (0 = 2011, 1 = 2012):",
        options=unique_years,
        default=unique_years
    )
    df = df[df['yr'].isin(selected_years)]

# Filter Kondisi Cuaca (weathersit)
if 'weathersit' in df.columns:
    unique_weather = sorted(df['weathersit'].unique())
    selected_weather = st.sidebar.multiselect(
        "Pilih Kondisi Cuaca (1=cerah, 2=berawan, dst.):",
        options=unique_weather,
        default=unique_weather
    )
    df = df[df['weathersit'].isin(selected_weather)]

# Filter Musim (season)
if 'season' in df.columns:
     unique_season = sorted(df['season'].unique())
     selected_season = st.sidebar.multiselect(
         "Pilih Musim:",
         options=unique_season,
         default=unique_season
     )
     df = df[df['season'].isin(selected_season)]

st.sidebar.write("---")
st.sidebar.write("Gunakan filter di atas untuk menyesuaikan tampilan data.")

# ================== LAYOUT: TABS UNTUK BEBERAPA ANALISIS ===================
tab1, tab2, tab3, tab4 = st.tabs([
    "Data Overview", 
    "Time Analysis", 
    "Weather Analysis", 
    "User Type Analysis"
])

# ============ TAB 1: DATA OVERVIEW ============
with tab1:
    st.title("🚴‍♂️ Bike Sharing Dashboard")
    st.markdown("### 1. Data Overview")
    st.write("Di sini kita melihat gambaran umum data yang sudah difilter.")

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(10))

    st.subheader("Descriptive Statistics")
    st.write(df.describe())

# ============ TAB 2: TIME ANALYSIS ============
with tab2:
    st.markdown("### 2. Time-based Analysis")
    st.write("Analisis tren penggunaan sepeda berdasarkan waktu.")

    # A. Tren Harian (jika ada kolom 'dteday')
    if 'dteday' in df.columns:
        st.subheader("Tren Harian")
        daily_usage = df.groupby('dteday')['cnt'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(daily_usage['dteday'], daily_usage['cnt'], marker='o', color='blue')
        ax.set_title("Tren Total Peminjaman Sepeda per Hari")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Total Peminjaman")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # B. Rata-rata Peminjaman per Bulan (mnth)
    if 'mnth' in df.columns:
        st.subheader("Peminjaman per Bulan")
        monthly_usage = df.groupby('mnth')['cnt'].mean().reset_index()

        fig2, ax2 = plt.subplots(figsize=(8,5))
        sns.barplot(x='mnth', y='cnt', data=monthly_usage, ax=ax2, palette="viridis", errorbar=None)
        ax2.set_title("Rata-rata Peminjaman per Bulan")
        ax2.set_xlabel("Bulan")
        ax2.set_ylabel("Rata-rata Peminjaman")
        st.pyplot(fig2)

    # C. Rata-rata Peminjaman per Jam (hr)
    if 'hr' in df.columns:
        st.subheader("Peminjaman per Jam")
        hour_usage = df.groupby('hr')['cnt'].mean().reset_index()

        fig3, ax3 = plt.subplots(figsize=(8,5))
        sns.barplot(x='hr', y='cnt', data=hour_usage, ax=ax3, palette="magma", errorbar=None)
        ax3.set_title("Rata-rata Peminjaman per Jam")
        ax3.set_xlabel("Jam")
        ax3.set_ylabel("Rata-rata Peminjaman")
        st.pyplot(fig3)

    # D. Rush Hour vs Non-Rush Hour
    if 'time_category' in df.columns:
        st.subheader("Rush Hour vs Non-Rush Hour")
        rush_df = df.groupby('time_category')['cnt'].mean().reset_index()

        fig4, ax4 = plt.subplots()
        sns.barplot(x='time_category', y='cnt', data=rush_df, ax=ax4, palette=["blue", "red"], errorbar=None)
        ax4.set_xlabel("Kategori Waktu")
        ax4.set_ylabel("Rata-rata Peminjaman")
        ax4.set_title("Perbandingan Peminjaman: Rush Hour vs Non-Rush Hour")
        st.pyplot(fig4)

# ============ TAB 3: WEATHER ANALYSIS ============
with tab3:
    st.markdown("### 3. Weather-based Analysis")
    st.write("Analisis pengaruh cuaca, suhu, kelembapan, dsb.")

    # A. Kondisi Cuaca vs Peminjaman
    if 'weathersit' in df.columns:
        st.subheader("Distribusi Peminjaman Berdasarkan Kondisi Cuaca")
        fig5, ax5 = plt.subplots(figsize=(8,5))
        sns.boxplot(x='weathersit', y='cnt', data=df, ax=ax5, palette="coolwarm")
        ax5.set_title("Boxplot: Kondisi Cuaca vs Peminjaman")
        ax5.set_xlabel("Kondisi Cuaca (1=cerah, 2=berawan, dsb.)")
        ax5.set_ylabel("Jumlah Peminjaman")
        st.pyplot(fig5)

    # B. Suhu (temp) vs Peminjaman
    if 'temp' in df.columns:
        st.subheader("Hubungan Suhu dan Peminjaman")
        fig6, ax6 = plt.subplots(figsize=(8,5))
        sns.scatterplot(x='temp', y='cnt', data=df, ax=ax6, hue='weathersit')
        ax6.set_title("Scatter Plot: Temp vs. Cnt")
        ax6.set_xlabel("Suhu (Normalized)")
        ax6.set_ylabel("Jumlah Peminjaman")
        st.pyplot(fig6)

    # C. Kelembapan (hum) vs Peminjaman (opsional)
    if 'hum' in df.columns:
        st.subheader("Kelembapan vs Peminjaman")
        fig7, ax7 = plt.subplots(figsize=(8,5))
        sns.scatterplot(x='hum', y='cnt', data=df, ax=ax7, hue='weathersit')
        ax7.set_title("Scatter Plot: Humidity vs. Cnt")
        ax7.set_xlabel("Kelembapan (Normalized)")
        ax7.set_ylabel("Jumlah Peminjaman")
        st.pyplot(fig7)

# ============ TAB 4: USER TYPE ANALYSIS ============
with tab4:
    st.markdown("### 4. User Type Analysis")
    st.write("Perbandingan penggunaan oleh **casual** vs. **registered** users.")

    if 'casual' in df.columns and 'registered' in df.columns:
        # A. Total Casual vs. Registered
        user_sum = df[['casual','registered']].sum()
        fig8, ax8 = plt.subplots(figsize=(6,5))
        user_sum.plot(kind='bar', ax=ax8, color=['orange','green'])
        ax8.set_title("Total Casual vs Registered Usage")
        ax8.set_ylabel("Total Peminjaman")
        ax8.set_xticklabels(["Casual","Registered"], rotation=0)
        st.pyplot(fig8)

        # B. Boxplot per jam (opsional)
        st.subheader("Distribusi Casual vs Registered per Jam")
        if 'hr' in df.columns:
            # Buat data panjang
            df_long = df.melt(
                id_vars='hr', 
                value_vars=['casual','registered'], 
                var_name='user_type', 
                value_name='count'
            )
            fig9, ax9 = plt.subplots(figsize=(8,5))
            sns.boxplot(x='hr', y='count', hue='user_type', data=df_long, ax=ax9)
            ax9.set_title("Casual vs Registered by Hour")
            ax9.set_xlabel("Jam")
            ax9.set_ylabel("Jumlah Pengguna")
            st.pyplot(fig9)

st.write("---")
st.markdown("""
**Catatan**:  
1. Gunakan _sidebar_ untuk memfilter data berdasarkan tahun atau kondisi cuaca.  
2. Lihat _tab_ Time Analysis untuk pola waktu (harian, bulanan, jam).  
3. Lihat _tab_ Weather Analysis untuk pengaruh cuaca, suhu, dan kelembapan.  
4. Lihat _tab_ User Type Analysis untuk membandingkan penggunaan _casual_ vs. _registered_.
""")

st.caption("Dibuat dengan ❤️ menggunakan Streamlit. Dari Yandiyan, semoga bintang 5") 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.dates as mdates

# Pengaturan dasar halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Supaya tampilan seaborn lebih enak dibaca
sns.set(style="whitegrid")

# ------------------------------------
# 1. LOAD DATA
# ------------------------------------
@st.cache_data
def load_day_data():
    """Load dataset harian dari main_data_day.csv."""
    df_day = pd.read_csv(os.path.join(os.path.dirname(__file__), "main_data_day.csv"))
    
    # Pastikan konversi 'dteday' ke datetime jika ada
    if 'dteday' in df_day.columns:
        df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    
    return df_day

@st.cache_data
def load_hour_data():
    """Load dataset per jam dari main_data_hour.csv."""
    df_hour = pd.read_csv(os.path.join(os.path.dirname(__file__), "main_data_hour.csv"))
    
    # Pastikan konversi 'dteday' ke datetime jika ada
    if 'dteday' in df_hour.columns:
        df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
        
    return df_hour

# Memuat kedua data
df_day = load_day_data()
df_hour = load_hour_data()

# ------------------------------------
# 2. SIDEBAR: FILTER-FILTER
# ------------------------------------
st.sidebar.title("Bike Sharing Filters")

# Filter Tahun (yr) -> 0 = 2011, 1 = 2012
if 'yr' in df_day.columns or 'yr' in df_hour.columns:
    all_years_day = df_day['yr'].unique() if 'yr' in df_day.columns else []
    all_years_hour = df_hour['yr'].unique() if 'yr' in df_hour.columns else []
    all_years = sorted(list(set(all_years_day) | set(all_years_hour)))  # gabung unique di day & hour

    selected_years = st.sidebar.multiselect(
        "Pilih Tahun (0 = 2011, 1 = 2012):",
        options=all_years,
        default=all_years
    )
    # Terapkan filter ke df_day
    if 'yr' in df_day.columns:
        df_day = df_day[df_day['yr'].isin(selected_years)]
    # Terapkan filter ke df_hour
    if 'yr' in df_hour.columns:
        df_hour = df_hour[df_hour['yr'].isin(selected_years)]

# Filter Kondisi Cuaca (weathersit)
if 'weathersit' in df_day.columns or 'weathersit' in df_hour.columns:
    all_weather_day = df_day['weathersit'].unique() if 'weathersit' in df_day.columns else []
    all_weather_hour = df_hour['weathersit'].unique() if 'weathersit' in df_hour.columns else []
    all_weather = sorted(list(set(all_weather_day) | set(all_weather_hour)))

    selected_weather = st.sidebar.multiselect(
        "Pilih Kondisi Cuaca (1=cerah, 2=berawan, dsb.):",
        options=all_weather,
        default=all_weather
    )
    # Terapkan filter
    if 'weathersit' in df_day.columns:
        df_day = df_day[df_day['weathersit'].isin(selected_weather)]
    if 'weathersit' in df_hour.columns:
        df_hour = df_hour[df_hour['weathersit'].isin(selected_weather)]

# Filter Musim (season)
if 'season' in df_day.columns or 'season' in df_hour.columns:
    all_season_day = df_day['season'].unique() if 'season' in df_day.columns else []
    all_season_hour = df_hour['season'].unique() if 'season' in df_hour.columns else []
    all_season = sorted(list(set(all_season_day) | set(all_season_hour)))

    selected_season = st.sidebar.multiselect(
        "Pilih Musim (1=Musim Semi, 2=Musim Panas, dst.):",
        options=all_season,
        default=all_season
    )
    # Terapkan filter
    if 'season' in df_day.columns:
        df_day = df_day[df_day['season'].isin(selected_season)]
    if 'season' in df_hour.columns:
        df_hour = df_hour[df_hour['season'].isin(selected_season)]

st.sidebar.write("---")
st.sidebar.write("Gunakan filter di atas untuk menyesuaikan tampilan data.")


# ------------------------------------
# 3. LAYOUT: TABS
# ------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Data Overview",
    "Time Analysis",
    "Weather Analysis",
    "User Type Analysis"
])

# ------------------------------------
# TAB 1: DATA OVERVIEW
# ------------------------------------
with tab1:
    st.title("🚴‍♂️ Bike Sharing Dashboard")
    st.markdown("### 1. Data Overview")
    st.write("Menampilkan gambaran umum data harian dan data per jam yang sudah terfilter.")

    st.subheader("Data Harian (df_day) - Preview")
    st.dataframe(df_day.head(10))

    st.subheader("Descriptive Statistics (Day)")
    st.write(df_day.describe())

    st.subheader("Data Per Jam (df_hour) - Preview")
    st.dataframe(df_hour.head(10))

    st.subheader("Descriptive Statistics (Hour)")
    st.write(df_hour.describe())

# ------------------------------------
# TAB 2: TIME ANALYSIS
# (Menyesuaikan kode Colab: tren harian, tren jam, pola bulanan, jam rush vs non-rush, dll.)
# ------------------------------------
with tab2:
    st.markdown("### 2. Time-based Analysis")
    st.write("Analisis tren penggunaan sepeda berdasarkan waktu (harian & per jam).")

    # --------------------------------
    # 2a. Tren Peminjaman Sepeda per Hari
    # --------------------------------
    st.subheader("Tren Peminjaman Sepeda per Hari")
    if 'dteday' in df_day.columns and 'cnt' in df_day.columns:
        fig, ax = plt.subplots(figsize=(12,5), dpi=100)
        ax.plot(df_day['dteday'], df_day['cnt'], label="Total Peminjaman", marker='o', linestyle='-')
        ax.set_xlabel("Tanggal", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Tren Peminjaman Sepeda per Hari", fontsize=12)
        ax.legend()

        # Format tanggal di sumbu X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig)
    else:
        st.warning("Kolom 'dteday' atau 'cnt' tidak ditemukan di df_day.")

    # --------------------------------
    # 2b. Tren Peminjaman Sepeda per Jam
    # --------------------------------
    st.subheader("Tren Peminjaman Sepeda per Jam")
    if 'hr' in df_hour.columns and 'cnt' in df_hour.columns:
        fig, ax = plt.subplots(figsize=(12,5), dpi=100)
        sns.lineplot(x=df_hour['hr'], y=df_hour['cnt'], marker='o', linestyle='-', label="Total Peminjaman", ax=ax)
        ax.set_xlabel("Jam", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Tren Peminjaman Sepeda per Jam", fontsize=12)
        ax.legend()
        ax.set_xticks(range(0,24,1))
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig)
    else:
        st.warning("Kolom 'hr' atau 'cnt' tidak ditemukan di df_hour.")

    # --------------------------------
    # 2c. Pola Peminjaman Berdasarkan Bulan (Day)
    # --------------------------------
    st.subheader("Pola Peminjaman Berdasarkan Bulan (Day)")
    if 'mnth' in df_day.columns and 'cnt' in df_day.columns:
        fig, ax = plt.subplots(figsize=(10,5), dpi=100)
        sns.barplot(x='mnth', y='cnt', data=df_day, palette="viridis", errorbar=None, ax=ax)
        ax.set_xlabel("Bulan", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Jumlah Peminjaman Sepeda Berdasarkan Bulan (Day)", fontsize=12)
        ax.set_xticks(range(0,12))
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], fontsize=9)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig)
    else:
        st.warning("Kolom 'mnth' atau 'cnt' tidak ditemukan di df_day.")

    # --------------------------------
    # 2d. Pola Peminjaman Berdasarkan Jam (Rush Hour vs Non-Rush Hour) - Hour
    # --------------------------------
    st.subheader("Pola Peminjaman Berdasarkan Rush Hour vs Non-Rush Hour (Hour)")
    if 'rush_hour' in df_hour.columns and 'cnt' in df_hour.columns:
        fig, ax = plt.subplots(figsize=(10,5), dpi=100)
        plot_data = df_hour[['rush_hour','cnt']].copy()

        # Pastikan tipenya string untuk memudahkan sorting/label
        plot_data['rush_hour'] = plot_data['rush_hour'].astype(str)

        ax2 = sns.barplot(x='rush_hour', y='cnt', data=plot_data, palette="coolwarm")
        ax2.set_xlabel("Kategori Waktu", fontsize=10)
        ax2.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax2.set_title("Distribusi Peminjaman Sepeda pada Rush Hour vs Non-Rush Hour (Hour)", fontsize=12)

        # Anotasi
        for p in ax2.patches:
            ax2.annotate(f'{int(p.get_height())}', 
                         (p.get_x() + p.get_width() / 2, p.get_height()),
                         ha='center', va='bottom', fontsize=9, color='black')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig)
    else:
        st.warning("Kolom 'rush_hour' atau 'cnt' tidak ditemukan di df_hour.")

    # --------------------------------
    # 2e. Tren Penggunaan Sepeda Selama 2 Tahun (Day)
    # --------------------------------
    st.subheader("Tren Penggunaan Sepeda Harian selama 2 Tahun")
    if 'dteday' in df_day.columns and 'cnt' in df_day.columns:
        # Tambahkan kolom rolling_mean(30 hari) jika belum ada
        if 'rolling_mean' not in df_day.columns:
            df_day['rolling_mean'] = df_day['cnt'].rolling(window=30).mean()

        fig, ax = plt.subplots(figsize=(12,5), dpi=100)

        sns.lineplot(x=df_day['dteday'], y=df_day['cnt'], marker='o', label="Total Peminjaman", ax=ax, color='blue')
        sns.lineplot(x=df_day['dteday'], y=df_day['rolling_mean'], label="Rata-rata Bergerak (30 hari)", ax=ax, color='red')

        ax.set_xlabel("Tanggal", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Tren Peminjaman Sepeda Harian dalam 2 Tahun", fontsize=12)
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        st.pyplot(fig)
    else:
        st.warning("Kolom 'dteday' atau 'cnt' tidak ditemukan di df_day.")

# ------------------------------------
# TAB 3: WEATHER ANALYSIS
# (Pengaruh Musim, Kondisi Cuaca, Suhu, dsb. untuk Day & Hour)
# ------------------------------------
with tab3:
    st.markdown("### 3. Weather-based Analysis")
    st.write("Analisis pengaruh musim, kondisi cuaca, dan suhu terhadap peminjaman sepeda (Day & Hour).")

    # ------------------------------
    # 3a. Pengaruh Musim terhadap Peminjaman (Day)
    # ------------------------------
    st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda (Day)")
    if 'season' in df_day.columns and 'cnt' in df_day.columns:
        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.boxplot(x=df_day['season'], y=df_day['cnt'], palette="coolwarm", ax=ax)
        ax.set_xlabel("Musim", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Pengaruh Musim terhadap Peminjaman Sepeda (Day)", fontsize=12)

        # Anotasi rata-rata
        mean_values = df_day.groupby("season")["cnt"].mean()
        for i, mean_val in enumerate(mean_values):
            ax.text(i, mean_val + 500, f'{int(mean_val):,}', ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'season' atau 'cnt' tidak ditemukan di df_day.")

    # ------------------------------
    # 3b. Pengaruh Musim terhadap Peminjaman (Hour)
    # ------------------------------
    st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda (Hour)")
    if 'season' in df_hour.columns and 'cnt' in df_hour.columns:
        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.boxplot(x=df_hour['season'], y=df_hour['cnt'], palette="coolwarm", ax=ax)
        ax.set_xlabel("Musim", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Pengaruh Musim terhadap Peminjaman Sepeda (Hour)", fontsize=12)

        # Anotasi rata-rata
        mean_values = df_hour.groupby("season")["cnt"].mean()
        for i, mean_val in enumerate(mean_values):
            ax.text(i, mean_val + 100, f'{int(mean_val):,}', ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'season' atau 'cnt' tidak ditemukan di df_hour.")

    # ------------------------------
    # 3c. Pengaruh Kondisi Cuaca (weathersit) terhadap Peminjaman (Day)
    # ------------------------------
    st.subheader("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda (Day)")
    if 'weathersit' in df_day.columns and 'cnt' in df_day.columns:
        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.boxplot(x=df_day['weathersit'], y=df_day['cnt'], palette="coolwarm", ax=ax)
        ax.set_xlabel("Kondisi Cuaca", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda (Day)", fontsize=12)

        # Anotasi rata-rata
        mean_values = df_day.groupby("weathersit")["cnt"].mean()
        for i, mean_val in enumerate(mean_values):
            ax.text(i, mean_val + 100, f'{int(mean_val):,}', ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'weathersit' atau 'cnt' tidak ditemukan di df_day.")

    # ------------------------------
    # 3d. Pengaruh Kondisi Cuaca (weathersit) terhadap Peminjaman (Hour)
    # ------------------------------
    st.subheader("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda (Hour)")
    if 'weathersit' in df_hour.columns and 'cnt' in df_hour.columns:
        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.boxplot(x=df_hour['weathersit'], y=df_hour['cnt'], palette="coolwarm", ax=ax)
        ax.set_xlabel("Kondisi Cuaca", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda (Hour)", fontsize=12)

        # Anotasi rata-rata
        mean_values = df_hour.groupby("weathersit")["cnt"].mean()
        for i, mean_val in enumerate(mean_values):
            ax.text(i, mean_val + 100, f'{int(mean_val):,}', ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'weathersit' atau 'cnt' tidak ditemukan di df_hour.")

    # ------------------------------
    # 3e. Pengaruh Suhu (temp_category) terhadap Peminjaman (Hour)
    # ------------------------------
    st.subheader("Pengaruh Suhu terhadap Peminjaman Sepeda (Hour)")
    if 'temp_category' in df_hour.columns and 'cnt' in df_hour.columns:
        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        # Pastikan urutan kategori suhu: Cold, Mild, Warm, Hot
        order_cats = ["Cold", "Mild", "Warm", "Hot"]
        sns.boxplot(x=df_hour['temp_category'], y=df_hour['cnt'], palette="magma", order=order_cats, ax=ax)
        ax.set_xlabel("Kategori Suhu", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Pengaruh Suhu terhadap Peminjaman Sepeda (Hour)", fontsize=12)

        # Anotasi median
        median_values = df_hour.groupby("temp_category")["cnt"].median()
        for i, median_val in enumerate(median_values):
            ax.text(i, median_val + 50, f'{int(median_val):,}', ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'temp_category' atau 'cnt' tidak ditemukan di df_hour.")

# ------------------------------------
# TAB 4: USER TYPE ANALYSIS
# (Perbandingan casual vs registered, jam sibuk vs non-sibuk, weekday vs weekend, dsb.)
# ------------------------------------
with tab4:
    st.markdown("### 4. User Type Analysis")
    st.write("Perbandingan penggunaan oleh **casual** vs. **registered**, serta analisis jam sibuk vs non-sibuk, hari kerja vs akhir pekan.")

    # ------------------------------------------------------
    # 4a. Perbandingan Pengguna Casual vs Registered (Day)
    # ------------------------------------------------------
    st.subheader("Perbandingan Pengguna Casual vs Registered (Day)")
    if 'casual' in df_day.columns and 'registered' in df_day.columns:
        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.boxplot(data=df_day[['casual', 'registered']], palette=["skyblue", "salmon"], ax=ax)
        ax.set_xlabel("Tipe Pengguna", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Perbandingan Pengguna Casual vs Registered (Day)", fontsize=12)

        # Anotasi median
        median_values = df_day[['casual', 'registered']].median()
        for i, median_val in enumerate(median_values):
            ax.text(i, median_val + 100, f'{int(median_val):,}', ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'casual' atau 'registered' tidak ditemukan di df_day.")

    # ------------------------------------------------------
    # 4b. Perbandingan Pengguna Casual vs Registered (Hour)
    # ------------------------------------------------------
    st.subheader("Perbandingan Pengguna Casual vs Registered (Hour)")
    if 'casual' in df_hour.columns and 'registered' in df_hour.columns:
        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.boxplot(data=df_hour[['casual', 'registered']], palette=["skyblue", "salmon"], ax=ax)
        ax.set_xlabel("Tipe Pengguna", fontsize=10)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=10)
        ax.set_title("Perbandingan Pengguna Casual vs Registered (Hour)", fontsize=12)

        # Anotasi median
        median_values = df_hour[['casual', 'registered']].median()
        for i, median_val in enumerate(median_values):
            ax.text(i, median_val + 100, f'{int(median_val):,}', ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'casual' atau 'registered' tidak ditemukan di df_hour.")

    # ------------------------------------------------------
    # 4c. Analisis Jam Sibuk (Rush Hour) vs Non-Sibuk (Hour)
    # ------------------------------------------------------
    st.subheader("Analisis Jam Sibuk vs Non-Sibuk (Hour)")
    if 'hr' in df_hour.columns and 'cnt' in df_hour.columns:
        # Definisi jam sibuk
        rush_hours = list(range(6, 10)) + list(range(16, 20))
        
        # Buat kolom time_category jika belum ada
        if 'time_category' not in df_hour.columns:
            df_hour['time_category'] = df_hour['hr'].apply(
                lambda x: 'Rush Hour' if x in rush_hours else 'Non-Rush Hour'
            )
        
        # Agregasi jumlah peminjaman
        rush_hour_comparison = df_hour.groupby('time_category').agg(
            avg_peminjaman=('cnt','mean'),
            total_peminjaman=('cnt','sum')
        ).reset_index()

        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.barplot(x='time_category', y='avg_peminjaman', data=rush_hour_comparison, palette='coolwarm', ax=ax)
        ax.set_xlabel("Kategori Waktu", fontsize=10)
        ax.set_ylabel("Rata-rata Peminjaman", fontsize=10)
        ax.set_title("Perbandingan Peminjaman Sepeda pada Rush Hour vs Non-Rush Hour", fontsize=12)

        # Anotasi
        for i, row in rush_hour_comparison.iterrows():
            ax.text(i, row.avg_peminjaman + 10, f'{int(row.avg_peminjaman):,}', 
                    ha='center', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'hr' atau 'cnt' tidak ditemukan di df_hour.")

    # ------------------------------------------------------
    # 4d. Analisis Hari Kerja (Weekday) vs Akhir Pekan (Weekend)
    #     + Pengaruh Rush Hour vs Non-Rush Hour
    # ------------------------------------------------------
    st.subheader("Pengaruh Hari Kerja vs Akhir Pekan terhadap Peminjaman (Hour)")
    if 'time_category' in df_hour.columns and 'day_type' in df_hour.columns and 'cnt' in df_hour.columns:
        rush_hour_weekday = df_hour.groupby(['time_category', 'day_type']).agg(
            avg_peminjaman=('cnt','mean'),
            total_peminjaman=('cnt','sum')
        ).reset_index()

        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.barplot(x='time_category', y='avg_peminjaman', hue='day_type', data=rush_hour_weekday, 
                    palette=['blue','red'], ax=ax)
        ax.set_xlabel("Kategori Waktu", fontsize=10)
        ax.set_ylabel("Rata-rata Peminjaman", fontsize=10)
        ax.set_title("Pengaruh Hari Kerja dan Akhir Pekan terhadap Peminjaman Sepeda", fontsize=12)
        
        # Legenda
        plt.legend(title="Tipe Hari", labels=["Weekday","Weekend"])

        # Anotasi
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height()):,}',
                        (p.get_x() + p.get_width()/2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'time_category' atau 'day_type' atau 'cnt' tidak ditemukan di df_hour.")

    # ------------------------------------------------------
    # 4e. Analisis Weekday vs Weekend (rata-rata peminjaman)
    # ------------------------------------------------------
    st.subheader("Perbandingan Peminjaman Sepeda: Weekday vs Weekend (Hour)")
    if 'day_type' in df_hour.columns and 'cnt' in df_hour.columns:
        weekday_weekend_comparison = df_hour.groupby('day_type').agg(
            avg_peminjaman=('cnt','mean'),
            total_peminjaman=('cnt','sum')
        ).reset_index()

        fig, ax = plt.subplots(figsize=(8,5), dpi=100)
        sns.barplot(x='day_type', y='avg_peminjaman', data=weekday_weekend_comparison, 
                    palette=['blue','red'], ax=ax)
        ax.set_xlabel("Tipe Hari", fontsize=10)
        ax.set_ylabel("Rata-rata Peminjaman", fontsize=10)
        ax.set_title("Perbandingan Peminjaman Sepeda: Weekday vs Weekend", fontsize=12)

        for i, row in weekday_weekend_comparison.iterrows():
            ax.text(i, row.avg_peminjaman + 10, f'{int(row.avg_peminjaman):,}', 
                    ha='center', fontsize=9, color='black')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'day_type' atau 'cnt' tidak ditemukan di df_hour.")

# ------------------------------------
# Bagian Bawah Halaman
# ------------------------------------
st.write("---")
st.markdown("""
**Catatan**:  
1. Gunakan _sidebar_ di sebelah kiri untuk memfilter data berdasarkan tahun, kondisi cuaca, maupun musim.  
2. Cek *Data Overview* untuk melihat rangkuman data.  
3. Buka *Time Analysis* untuk analisis tren peminjaman berdasarkan hari, jam, bulan, jam sibuk, dll.  
4. Buka *Weather Analysis* untuk melihat pengaruh musim, cuaca, dan suhu.  
5. Buka *User Type Analysis* untuk melihat perbedaan pengguna casual vs registered, serta analisis weekday vs weekend dan jam sibuk.  
""")

st.caption("Dibuat dengan ❤️ menggunakan Streamlit. Dari Yandiyan, semoga bintang 5.")
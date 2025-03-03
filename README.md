# 🚴‍♂️ Bike Sharing Dashboard

## 📊 Dashboard Interaktif untuk Analisis Peminjaman Sepeda

Bike Sharing Dashboard adalah aplikasi visualisasi data interaktif yang dibangun dengan Streamlit untuk mengeksplorasi tren peminjaman sepeda berdasarkan waktu, cuaca, dan jenis pengguna.

## 📦 Struktur Proyek
```
submission
├───dashboard
│    ├── main_data.csv     # Dataset utama yang digunakan di dashboard
│    ├── dashboard.py      # File utama Streamlit untuk menjalankan dashboard
├───data
│    ├── day.csv           # Data mentah (harian)
│    ├── hour.csv          # Data mentah (per jam)
│    ├── day_clean.csv     # Data hasil cleaning
│    ├── hour_clean.csv    # Data hasil cleaning
│    ├── day_featured.csv  # Data hasil feature engineering (harian)
│    ├── hour_featured.csv # Data hasil feature engineering (per jam)
├───notebook.ipynb         # Notebook eksplorasi dan analisis
├───README.md              # Panduan menjalankan proyek
├───requirements.txt       # Daftar library yang digunakan
└───url.txt                # URL jika dashboard dideploy
```
## 🛠️ Setup Environment & Instalasi Library

Terdapat dua cara untuk menjalankan proyek ini: menggunakan Anaconda atau virtual environment (venv/pipenv).

### 1️⃣ Menggunakan Anaconda
```
conda create --name bike_dashboard python=3.9
conda activate bike_dashboard
pip install -r requirements.txt
```
### 2️⃣ Menggunakan Virtual Environment (Pip)
```
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard
python -m venv env
source env/bin/activate  # (Mac/Linux)
env\Scripts\activate  # (Windows)
pip install -r requirements.txt
```
### 3️⃣ Menggunakan Pipenv
```
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```
## 🚀 Menjalankan Dashboard

Setelah environment terinstal, jalankan Streamlit dengan perintah berikut:
```
cd submission/dashboard
streamlit run dashboard.py
Kemudian, buka browser dan akses dashboard di:
<http://localhost:8501>
```
## 📝 Fitur dalam Dashboard

✅ Data Overview → Menampilkan gambaran umum dataset.

✅ Time Analysis → Tren peminjaman berdasarkan hari, bulan, dan jam.

✅ Weather Analysis → Pengaruh cuaca, suhu, dan kelembapan terhadap peminjaman.

✅ User Type Analysis → Perbandingan pengguna casual dan registered.

✅ Filter Interaktif → Memilih tahun, kondisi cuaca, dan faktor lainnya.

## 📌 Catatan Tambahan

Pastikan struktur folder sesuai dan menjalankan sesuai instruksi

## 🎯 Kesimpulan

Dashboard ini dirancang untuk membantu memahami tren peminjaman sepeda dan bagaimana berbagai faktor seperti waktu, cuaca, dan jenis pengguna memengaruhi pola peminjaman. 🚴‍♂️

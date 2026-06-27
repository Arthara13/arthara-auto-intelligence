# 🚗 AutoPrice Intelligence Dashboard

Dashboard prediksi harga kendaraan bekas menggunakan Machine Learning (Random Forest + Ridge Regression).

## Cara Menjalankan

### 1. Install dependencies
```bash
pip install streamlit scikit-learn pandas numpy plotly
```

### 2. Letakkan file dataset
Pastikan file `vehicle_price_prediction.csv` ada di folder yang sama dengan `app.py`.

```
dashboard/
├── app.py
└── vehicle_price_prediction.csv
```

### 3. Jalankan dashboard
```bash
streamlit run app.py
```

Dashboard akan terbuka otomatis di browser: `http://localhost:8501`

---

## Fitur Dashboard

| Halaman | Konten |
|---|---|
| 🏠 Overview & EDA | KPI cards, distribusi harga, heatmap korelasi |
| 📊 Analisis Mendalam | Filter interaktif, scatter plots, box plots |
| 🔮 Prediksi Harga | Form input spesifikasi → estimasi harga + feature importance |
| 📈 Evaluasi Model | Actual vs Predicted, residuals, perbandingan RF vs Ridge |

## Model yang Digunakan
- **Random Forest Regressor** — model utama
- **Ridge Regression** — model baseline perbandingan

## Deploy ke Streamlit Cloud
1. Upload ke GitHub repository
2. Buka https://share.streamlit.io
3. Connect repo → pilih `app.py`
4. Upload dataset sebagai file statis atau gunakan st.file_uploader

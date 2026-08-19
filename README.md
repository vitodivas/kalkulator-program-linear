# 📈 Kalkulator Program Linear — Metode Grafik & Simpleks

Aplikasi Python untuk menyelesaikan soal **Program Linear (Linear Programming) 2 variabel** menggunakan dua metode sekaligus:

1. **Metode Simpleks** — menampilkan tabel iterasi (tabel simpleks) langkah demi langkah hingga solusi optimal ditemukan.
2. **Metode Grafik** — menampilkan visualisasi daerah penyelesaian (*feasible region*) beserta titik optimalnya.

Tersedia dalam dua versi:
- 🖥️ **CLI (Command Line)** — `Aplikasi_Kalkulator_Program_Linear.py`
- 🌐 **Web App (Streamlit)** — `app_streamlit.py`

---

## 📌 Latar Belakang Soal

Program ini menyelesaikan bentuk umum soal Program Linear:

```
Maksimumkan   Z = c1.x + c2.y
Kendala       a1.x + b1.y ≤ r1
              a2.x + b2.y ≤ r2
              ...
              x ≥ 0, y ≥ 0
```

Contoh soal bawaan (default):

```
Maksimumkan Z = 5x + 4y
Kendala:
  x + 2y ≤ 14
  3x + y ≤ 21
```

Solusi optimal untuk contoh di atas: **x = 5.6, y = 4.2, Z = 44.8**

---

## 🚀 Demo

### Versi Web (Streamlit)
Input soal lewat sidebar, hasil ditampilkan dalam bentuk grafik interaktif, tabel iterasi simpleks, dan perbandingan hasil kedua metode.

### Versi CLI
Menampilkan tabel iterasi simpleks di terminal, lalu membuka jendela grafik matplotlib berisi daerah penyelesaian.

---

## 🛠️ Instalasi

Pastikan Python 3.8+ sudah terpasang, lalu install dependensi:

```bash
pip install numpy matplotlib streamlit pandas
```

---

## ▶️ Cara Menjalankan

### 1. Versi CLI

```bash
python Aplikasi_Kalkulator_Program_Linear.py
```

- Program akan meminta input koefisien fungsi tujuan dan kendala.
- Tekan **ENTER** tanpa mengisi apa pun untuk memakai contoh soal default.
- Hasil tabel simpleks akan tercetak di terminal, lalu grafik akan muncul di jendela baru dan otomatis tersimpan sebagai `grafik_program_linear.png`.

### 2. Versi Web (Streamlit)

```bash
streamlit run app_streamlit.py
```

- Browser akan terbuka otomatis (biasanya di `http://localhost:8501`).
- Atur fungsi tujuan dan kendala di sidebar kiri, lalu klik **Hitung Solusi**.
- Hasil ditampilkan dalam 3 tab: Metode Grafik, Metode Simpleks, dan Perbandingan Hasil.

> 💡 Jika ingin membagikan versi web ini sebagai link portofolio, deploy secara gratis ke [Streamlit Community Cloud](https://streamlit.io/cloud) dengan menghubungkan repo GitHub ini.

---

## 📂 Struktur File

```
├── Aplikasi_Kalkulator_Program_Linear.py   # Versi CLI (terminal)
├── app_streamlit.py                        # Versi web (Streamlit)
└── README.md                               # Dokumentasi proyek ini
```

---

## 🧠 Konsep yang Digunakan

- **Metode Simpleks**: implementasi tabel simpleks dari nol (tanpa library solver eksternal seperti `scipy.optimize.linprog`), termasuk uji optimalitas, pemilihan kolom pivot, uji rasio minimum, dan operasi baris eliminasi Gauss-Jordan.
- **Metode Grafik**: mencari semua titik sudut kandidat (perpotongan antar garis kendala dan sumbu), menyaring titik yang *feasible*, lalu mengevaluasi nilai fungsi tujuan di tiap titik sudut untuk menemukan solusi optimal — sesuai Teorema Titik Sudut (*Corner Point Theorem*) dalam Program Linear.
- **Visualisasi**: `matplotlib` untuk versi CLI, terintegrasi dengan `streamlit` untuk versi web interaktif.

---

## ✍️ Pengembangan Lebih Lanjut (Ide)

- Mendukung Program Linear dengan lebih dari 2 variabel keputusan.
- Menambahkan mode Minimumkan (selain Maksimumkan).
- Menambahkan unit test untuk fungsi `metode_simpleks` dan `metode_grafik`.
- Ekspor hasil ke PDF/Excel.

---

## 👤 Author

Dibuat sebagai proyek pembelajaran Riset Operasi / Program Linear.

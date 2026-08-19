"""
=====================================================================
 KALKULATOR PROGRAM LINEAR - VERSI WEB (STREAMLIT)
 Metode Grafik dan Metode Simpleks
=====================================================================
 Versi interaktif berbasis web dari kalkulator program linear 2
 variabel. Logika perhitungan (Simpleks & Grafik) mengikuti versi
 CLI asli (Aplikasi_Kalkulator_Program_Linear.py), hanya antarmukanya
 yang diubah dari input() menjadi widget Streamlit.

 Cara menjalankan secara lokal:
   pip install streamlit numpy matplotlib
   streamlit run app_streamlit.py
=====================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulator Program Linear", page_icon="📈", layout="wide")


# =====================================================================
# METODE SIMPLEKS
# =====================================================================
def metode_simpleks(c1, c2, kendala):
    n_var = 2
    n_slack = len(kendala)
    n_kolom = n_var + n_slack + 1

    tabel = np.zeros((len(kendala) + 1, n_kolom))
    for i, (a, b, r) in enumerate(kendala):
        tabel[i, 0] = a
        tabel[i, 1] = b
        tabel[i, n_var + i] = 1
        tabel[i, -1] = r

    tabel[-1, 0] = -c1
    tabel[-1, 1] = -c2

    nama_kolom = ["x", "y"] + [f"s{i+1}" for i in range(n_slack)] + ["RHS"]
    basis = [f"s{i+1}" for i in range(n_slack)]

    riwayat_tabel = []
    iterasi = 0
    while True:
        baris_z = tabel[-1, :-1]
        riwayat_tabel.append((iterasi, tabel.copy(), basis.copy()))

        if np.all(baris_z >= -1e-9):
            break

        kolom_pivot = int(np.argmin(baris_z))

        rasio = []
        for i in range(len(kendala)):
            elemen = tabel[i, kolom_pivot]
            if elemen > 1e-9:
                rasio.append(tabel[i, -1] / elemen)
            else:
                rasio.append(np.inf)

        if all(r == np.inf for r in rasio):
            return None, None, nama_kolom, riwayat_tabel

        baris_pivot = int(np.argmin(rasio))
        elemen_pivot = tabel[baris_pivot, kolom_pivot]

        tabel[baris_pivot, :] = tabel[baris_pivot, :] / elemen_pivot
        for i in range(tabel.shape[0]):
            if i != baris_pivot:
                tabel[i, :] -= tabel[i, kolom_pivot] * tabel[baris_pivot, :]

        basis[baris_pivot] = nama_kolom[kolom_pivot]
        iterasi += 1
        if iterasi > 50:
            break

    hasil = {"x": 0.0, "y": 0.0}
    for i, var in enumerate(basis):
        if var in hasil:
            hasil[var] = tabel[i, -1]
    z_optimal = tabel[-1, -1]

    return (hasil["x"], hasil["y"], z_optimal), riwayat_tabel, nama_kolom, None


# =====================================================================
# METODE GRAFIK
# =====================================================================
def cari_titik_potong(l1, l2):
    a1, b1, r1 = l1
    a2, b2, r2 = l2
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([r1, r2])
    det = np.linalg.det(A)
    if abs(det) < 1e-9:
        return None
    x, y = np.linalg.solve(A, B)
    return x, y


def titik_layak(x, y, kendala, eps=1e-6):
    if x < -eps or y < -eps:
        return False
    for a, b, r in kendala:
        if a * x + b * y > r + eps:
            return False
    return True


def metode_grafik(c1, c2, kendala):
    titik_kandidat = [(0.0, 0.0)]

    for a, b, r in kendala:
        if abs(a) > 1e-9:
            titik_kandidat.append((r / a, 0.0))
        if abs(b) > 1e-9:
            titik_kandidat.append((0.0, r / b))

    for i in range(len(kendala)):
        for j in range(i + 1, len(kendala)):
            titik = cari_titik_potong(kendala[i], kendala[j])
            if titik is not None:
                titik_kandidat.append(titik)

    titik_layak_list = []
    for (x, y) in titik_kandidat:
        if titik_layak(x, y, kendala):
            titik_layak_list.append((round(x, 4), round(y, 4)))
    titik_layak_list = list(set(titik_layak_list))

    hasil_tiap_titik = []
    for (x, y) in titik_layak_list:
        z = c1 * x + c2 * y
        hasil_tiap_titik.append((x, y, z))
    hasil_tiap_titik.sort(key=lambda t: -t[2])

    x_opt, y_opt, z_opt = hasil_tiap_titik[0]

    x_maks = max([r / a for a, b, r in kendala if a > 1e-9] + [x_opt]) * 1.4
    x_maks = max(x_maks, 10)
    x_vals = np.linspace(0, x_maks, 400)

    fig, ax = plt.subplots(figsize=(7, 6))
    y_upper = np.full_like(x_vals, np.inf)
    warna = ["blue", "red", "green", "purple", "orange", "brown"]

    for idx, (a, b, r) in enumerate(kendala):
        warna_garis = warna[idx % len(warna)]
        if abs(b) > 1e-9:
            y_line = (r - a * x_vals) / b
            ax.plot(x_vals, y_line, color=warna_garis,
                    label=f"{a:g}x + {b:g}y ≤ {r:g}")
            y_upper = np.minimum(y_upper, np.where(y_line >= 0, y_line, 0))
        else:
            x_batas = r / a
            ax.axvline(x_batas, color=warna_garis, label=f"{a:g}x ≤ {r:g}")

    y_upper = np.clip(y_upper, 0, None)
    ax.fill_between(x_vals, 0, y_upper, color="gray", alpha=0.5,
                     label="Daerah Penyelesaian (Feasible Region)")
    ax.plot(x_opt, y_opt, marker="*", color="green", markersize=18,
            label=f"Titik Optimal ({x_opt:g}, {y_opt:g})")

    ax.set_title("Metode Grafik - Program Linear")
    ax.set_xlabel("Sumbu X")
    ax.set_ylabel("Sumbu Y")
    ax.set_xlim(0, x_maks)
    ax.set_ylim(0, x_maks)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(fontsize=8)
    fig.tight_layout()

    return fig, hasil_tiap_titik, (x_opt, y_opt, z_opt)


# =====================================================================
# ANTARMUKA STREAMLIT
# =====================================================================
st.title("📈 Kalkulator Program Linear")
st.caption("Metode Grafik & Metode Simpleks — Program Linear 2 Variabel")

st.markdown(
    "Selesaikan soal **Maksimumkan Z = c1.x + c2.y** dengan kendala "
    "`a.x + b.y ≤ r` sekaligus dengan dua metode: Grafik dan Simpleks."
)

with st.sidebar:
    st.header("⚙️ Input Soal")
    st.subheader("Fungsi Tujuan")
    c1 = st.number_input("Koefisien x (c1)", value=5.0, step=1.0)
    c2 = st.number_input("Koefisien y (c2)", value=4.0, step=1.0)

    st.subheader("Kendala")
    jumlah_kendala = st.number_input("Jumlah kendala", min_value=1, max_value=6, value=2, step=1)

    default_kendala = [(1.0, 2.0, 14.0), (3.0, 1.0, 21.0)]
    kendala = []
    for i in range(int(jumlah_kendala)):
        st.markdown(f"**Kendala ke-{i+1}:** a·x + b·y ≤ r")
        da, db, dr = default_kendala[i] if i < len(default_kendala) else (1.0, 1.0, 10.0)
        col1, col2, col3 = st.columns(3)
        a = col1.number_input(f"a{i+1}", value=da, key=f"a{i}")
        b = col2.number_input(f"b{i+1}", value=db, key=f"b{i}")
        r = col3.number_input(f"r{i+1}", value=dr, key=f"r{i}")
        kendala.append((a, b, r))

    hitung = st.button("🚀 Hitung Solusi", use_container_width=True, type="primary")

if hitung:
    st.subheader("📋 Ringkasan Soal")
    kendala_str = "  \n".join(
        [f"Kendala {i+1}: {a:g}x + {b:g}y ≤ {r:g}" for i, (a, b, r) in enumerate(kendala)]
    )
    st.markdown(f"**Maksimumkan Z = {c1:g}x + {c2:g}y**  \n{kendala_str}  \nx ≥ 0, y ≥ 0")

    tab_grafik, tab_simpleks, tab_ringkasan = st.tabs(["📐 Metode Grafik", "🧮 Metode Simpleks", "✅ Perbandingan Hasil"])

    with tab_grafik:
        fig, hasil_tiap_titik, (x_opt, y_opt, z_opt) = metode_grafik(c1, c2, kendala)
        col_plot, col_table = st.columns([1.3, 1])
        with col_plot:
            st.pyplot(fig)
        with col_table:
            st.markdown("**Titik-titik Sudut Feasible**")
            df_titik = pd.DataFrame(hasil_tiap_titik, columns=["x", "y", "Z"])
            df_titik["Optimal"] = df_titik.apply(
                lambda row: "⭐" if (row["x"], row["y"], row["Z"]) == (x_opt, y_opt, z_opt) else "", axis=1
            )
            st.dataframe(df_titik, use_container_width=True, hide_index=True)
            st.success(f"**Titik Optimal:** x = {x_opt:g}, y = {y_opt:g}, Z = {z_opt:g}")

    with tab_simpleks:
        hasil_simpleks, riwayat_tabel, nama_kolom, unbounded = metode_simpleks(c1, c2, kendala)
        if unbounded is not None:
            st.error("Solusi tidak terbatas (unbounded).")
        else:
            for it, tabel, basis in riwayat_tabel:
                st.markdown(f"**Iterasi ke-{it}**")
                df_iter = pd.DataFrame(tabel, columns=nama_kolom)
                df_iter.insert(0, "Basis", basis + ["Z"])
                st.dataframe(df_iter.style.format(precision=2), use_container_width=True, hide_index=True)
            xs, ys, zs = hasil_simpleks
            st.success(f"**Solusi Optimal (Simpleks):** x = {xs:.2f}, y = {ys:.2f}, Z = {zs:.2f}")

    with tab_ringkasan:
        st.markdown("### Perbandingan Hasil Kedua Metode")
        rows = []
        if unbounded is None:
            xs, ys, zs = hasil_simpleks
            rows.append(["Metode Simpleks", f"{xs:.2f}", f"{ys:.2f}", f"{zs:.2f}"])
        rows.append(["Metode Grafik", f"{x_opt:.2f}", f"{y_opt:.2f}", f"{z_opt:.2f}"])
        df_banding = pd.DataFrame(rows, columns=["Metode", "x", "y", "Z"])
        st.table(df_banding)
        st.info("Kedua metode menghasilkan nilai optimal yang sama (jika soal memiliki solusi terbatas).")
else:
    st.info("⬅️ Atur fungsi tujuan dan kendala di sidebar, lalu klik **Hitung Solusi**.")

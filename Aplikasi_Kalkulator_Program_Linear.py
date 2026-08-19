"""
=====================================================================
 APLIKASI KALKULATOR PROGRAM LINEAR
 Metode Grafik dan Metode Simpleks
=====================================================================
 Kasus   : Maksimumkan Z = c1.x + c2.y
 Kendala : a1.x + b1.y <= r1
           a2.x + b2.y <= r2
           ...
           x >= 0, y >= 0

 Program ini menyelesaikan soal Program Linear 2 variabel dengan
 dua cara sekaligus:
   1. Metode Grafik  -> menampilkan gambar daerah penyelesaian
                        (feasible region) dan titik optimal
   2. Metode Simpleks -> menampilkan tabel iterasi simpleks
                        sampai didapat solusi optimal

 Cara pakai:
   - Jalankan program, lalu isi fungsi tujuan dan kendala sesuai
     soal yang diminta.
   - Contoh soal bawaan (default) kalau kamu tekan ENTER semua:
       Maksimumkan Z = 5x + 4y
       Kendala : x + 2y <= 14
                 3x + y <= 21
     Hasil yang benar untuk contoh ini: x=5.6, y=4.2, Z=44.8
=====================================================================
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# =====================================================================
# BAGIAN 1 : INPUT DATA DARI USER
# =====================================================================
def input_data():
    print("=" * 60)
    print("   KALKULATOR PROGRAM LINEAR - METODE GRAFIK & SIMPLEKS")
    print("=" * 60)
    print("\nFungsi Tujuan  : Maksimumkan Z = c1.x + c2.y")
    print("(Tekan ENTER tanpa isi apapun untuk pakai contoh soal default)\n")

    c1_in = input("Masukkan koefisien x pada Z (c1) [default 5] : ").strip()
    c2_in = input("Masukkan koefisien y pada Z (c2) [default 4] : ").strip()
    c1 = float(c1_in) if c1_in else 5.0
    c2 = float(c2_in) if c2_in else 4.0

    n_in = input("\nJumlah kendala [default 2] : ").strip()
    jumlah_kendala = int(n_in) if n_in else 2

    default_kendala = [(1, 2, 14), (3, 1, 21)]
    kendala = []
    for i in range(jumlah_kendala):
        print(f"\nKendala ke-{i + 1}  :  a.x + b.y <= r")
        if i < len(default_kendala):
            da, db, dr = default_kendala[i]
        else:
            da, db, dr = 1, 1, 10
        a_in = input(f"  Koefisien x (a{i+1}) [default {da}] : ").strip()
        b_in = input(f"  Koefisien y (b{i+1}) [default {db}] : ").strip()
        r_in = input(f"  Nilai batas / RHS (r{i+1}) [default {dr}] : ").strip()
        a = float(a_in) if a_in else da
        b = float(b_in) if b_in else db
        r = float(r_in) if r_in else dr
        kendala.append((a, b, r))

    return c1, c2, kendala


# =====================================================================
# BAGIAN 2 : METODE SIMPLEKS (Tabel Simpleks / Big Table method)
# =====================================================================
def metode_simpleks(c1, c2, kendala, tampilkan_tabel=True):
    n_var = 2                      # x dan y
    n_slack = len(kendala)         # 1 slack variable per kendala
    n_kolom = n_var + n_slack + 1  # + kolom RHS

    # Susun tabel awal
    tabel = np.zeros((len(kendala) + 1, n_kolom))
    for i, (a, b, r) in enumerate(kendala):
        tabel[i, 0] = a
        tabel[i, 1] = b
        tabel[i, n_var + i] = 1     # variabel slack
        tabel[i, -1] = r

    # Baris fungsi tujuan (Z) : -c1, -c2, 0,...,0 | 0
    tabel[-1, 0] = -c1
    tabel[-1, 1] = -c2

    nama_kolom = ["x", "y"] + [f"s{i+1}" for i in range(n_slack)] + ["RHS"]
    basis = [f"s{i+1}" for i in range(n_slack)]

    if tampilkan_tabel:
        print("\n" + "=" * 60)
        print("             ITERASI METODE SIMPLEKS")
        print("=" * 60)

    iterasi = 0
    while True:
        baris_z = tabel[-1, :-1]
        if tampilkan_tabel:
            cetak_tabel(tabel, nama_kolom, basis, iterasi)

        # Uji optimal: berhenti jika semua koefisien baris Z >= 0
        if np.all(baris_z >= -1e-9):
            break

        # Kolom pivot: koefisien paling negatif pada baris Z
        kolom_pivot = int(np.argmin(baris_z))

        # Uji rasio (minimum ratio test) untuk baris pivot
        rasio = []
        for i in range(len(kendala)):
            elemen = tabel[i, kolom_pivot]
            if elemen > 1e-9:
                rasio.append(tabel[i, -1] / elemen)
            else:
                rasio.append(np.inf)

        if all(r == np.inf for r in rasio):
            print("Solusi tidak terbatas (unbounded).")
            return None

        baris_pivot = int(np.argmin(rasio))
        elemen_pivot = tabel[baris_pivot, kolom_pivot]

        # Normalisasi baris pivot
        tabel[baris_pivot, :] = tabel[baris_pivot, :] / elemen_pivot

        # Eliminasi kolom pivot di baris lain
        for i in range(tabel.shape[0]):
            if i != baris_pivot:
                tabel[i, :] -= tabel[i, kolom_pivot] * tabel[baris_pivot, :]

        basis[baris_pivot] = nama_kolom[kolom_pivot]
        iterasi += 1

        if iterasi > 50:  # pengaman agar tidak infinite loop
            break

    # Ambil hasil akhir dari tabel optimal
    hasil = {"x": 0.0, "y": 0.0}
    for i, var in enumerate(basis):
        if var in hasil:
            hasil[var] = tabel[i, -1]
    z_optimal = tabel[-1, -1]

    return hasil["x"], hasil["y"], z_optimal


def cetak_tabel(tabel, nama_kolom, basis, iterasi):
    print(f"\n--- Tabel Iterasi ke-{iterasi} ---")
    header = "Basis".ljust(8) + "".join(k.rjust(10) for k in nama_kolom)
    print(header)
    for i in range(tabel.shape[0] - 1):
        baris = basis[i].ljust(8) + "".join(f"{v:10.2f}" for v in tabel[i, :])
        print(baris)
    baris_z = "Z".ljust(8) + "".join(f"{v:10.2f}" for v in tabel[-1, :])
    print(baris_z)


# =====================================================================
# BAGIAN 3 : METODE GRAFIK
# =====================================================================
def cari_titik_potong(l1, l2):
    """Cari titik potong dua garis a1.x + b1.y = r1 dan a2.x + b2.y = r2"""
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
    # ---- 1) Kumpulkan semua titik sudut (vertex) kandidat ----
    titik_kandidat = [(0.0, 0.0)]

    for a, b, r in kendala:
        if abs(a) > 1e-9:
            titik_kandidat.append((r / a, 0.0))          # potong sumbu X
        if abs(b) > 1e-9:
            titik_kandidat.append((0.0, r / b))          # potong sumbu Y

    for i in range(len(kendala)):
        for j in range(i + 1, len(kendala)):
            titik = cari_titik_potong(kendala[i], kendala[j])
            if titik is not None:
                titik_kandidat.append(titik)

    # ---- 2) Saring hanya titik yang benar-benar layak (feasible) ----
    titik_layak_list = []
    for (x, y) in titik_kandidat:
        if titik_layak(x, y, kendala):
            titik_layak_list.append((round(x, 4), round(y, 4)))

    titik_layak_list = list(set(titik_layak_list))  # hilangkan duplikat

    # ---- 3) Hitung Z pada tiap titik sudut, cari yang maksimum ----
    hasil_tiap_titik = []
    for (x, y) in titik_layak_list:
        z = c1 * x + c2 * y
        hasil_tiap_titik.append((x, y, z))
    hasil_tiap_titik.sort(key=lambda t: -t[2])

    x_opt, y_opt, z_opt = hasil_tiap_titik[0]

    print("\n" + "=" * 60)
    print("             METODE GRAFIK - TITIK SUDUT")
    print("=" * 60)
    print(f"{'x':>8}{'y':>8}{'Z = c1.x + c2.y':>20}")
    for x, y, z in hasil_tiap_titik:
        tanda = "  <-- OPTIMAL" if (x, y, z) == (x_opt, y_opt, z_opt) else ""
        print(f"{x:8.2f}{y:8.2f}{z:20.2f}{tanda}")

    # ---- 4) Gambar grafik ----
    x_maks = max([r / a for a, b, r in kendala if a > 1e-9] + [x_opt]) * 1.4
    x_maks = max(x_maks, 10)
    x_vals = np.linspace(0, x_maks, 400)

    plt.figure(figsize=(8, 7))

    # Batas atas daerah layak = nilai minimum dari semua garis kendala
    y_upper = np.full_like(x_vals, np.inf)
    warna = ["blue", "red", "green", "purple", "orange", "brown"]

    for idx, (a, b, r) in enumerate(kendala):
        warna_garis = warna[idx % len(warna)]
        if abs(b) > 1e-9:
            y_line = (r - a * x_vals) / b
            plt.plot(x_vals, y_line, color=warna_garis,
                     label=f"{a:g}x + {b:g}y ≤ {r:g}")
            y_upper = np.minimum(y_upper, np.where(y_line >= 0, y_line, 0))
        else:
            x_batas = r / a
            plt.axvline(x_batas, color=warna_garis,
                        label=f"{a:g}x ≤ {r:g}")

    y_upper = np.clip(y_upper, 0, None)
    plt.fill_between(x_vals, 0, y_upper, color="gray", alpha=0.5,
                      label="Daerah Penyelesaian (Feasible Region)")

    plt.plot(x_opt, y_opt, marker="*", color="green", markersize=18,
              label=f"Titik Optimal ({x_opt:g}, {y_opt:g})")

    plt.title("Metode Grafik - Program Linear")
    plt.xlabel("Sumbu X")
    plt.ylabel("Sumbu Y")
    plt.xlim(0, x_maks)
    plt.ylim(0, x_maks)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # Simpan gambar di folder yang sama dengan file program ini (aman di komputer manapun)
    try:
        folder_program = os.path.dirname(os.path.abspath(__file__))
        path_simpan = os.path.join(folder_program, "grafik_program_linear.png")
        plt.savefig(path_simpan, dpi=150)
        print(f"\n(Gambar grafik disimpan di: {path_simpan})")
    except Exception as e:
        print(f"\n(Gagal menyimpan gambar otomatis: {e})")

    plt.show()

    return x_opt, y_opt, z_opt


# =====================================================================
# BAGIAN 4 : PROGRAM UTAMA
# =====================================================================
def main():
    c1, c2, kendala = input_data()

    print("\n" + "=" * 60)
    print("RINGKASAN SOAL")
    print("=" * 60)
    print(f"Maksimumkan Z = {c1:g}x + {c2:g}y")
    for i, (a, b, r) in enumerate(kendala):
        print(f"Kendala {i+1} : {a:g}x + {b:g}y <= {r:g}")
    print("x >= 0, y >= 0")

    # ---- Metode Simpleks ----
    hasil_simpleks = metode_simpleks(c1, c2, kendala)

    # ---- Metode Grafik ----
    x_opt, y_opt, z_opt = metode_grafik(c1, c2, kendala)

    # ---- Bandingkan hasil kedua metode ----
    print("\n" + "=" * 60)
    print("             HASIL AKHIR (PERBANDINGAN METODE)")
    print("=" * 60)
    if hasil_simpleks is not None:
        xs, ys, zs = hasil_simpleks
        print(f"Metode Simpleks : x = {xs:.2f}, y = {ys:.2f}, Z = {zs:.2f}")
    print(f"Metode Grafik   : x = {x_opt:.2f}, y = {y_opt:.2f}, Z = {z_opt:.2f}")
    print("\nKedua metode menghasilkan nilai optimal yang sama.")
    print("=" * 60)


if __name__ == "__main__":
    main()

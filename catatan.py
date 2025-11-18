# ==============================

import mysql.connector
from datetime import datetime

# ==============================
# CONNECT KE DATABASE MYSQL
# ==============================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",       # default Laragon: kosong
    database="keuangan"
)

cur = conn.cursor()

# ==============================
# FUNGSI TAMBAH TRANSAKSI
# ==============================
def tambah_transaksi(jenis):
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deskripsi = input("Deskripsi: ")
    jumlah = int(input("Jumlah: "))

    sql = "INSERT INTO transaksi (tanggal, jenis, deskripsi, jumlah) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (tanggal, jenis, deskripsi, jumlah))
    conn.commit()

    print("✔ Transaksi berhasil disimpan!\n")


# ==============================
# FUNGSI LIHAT TRANSAKSI
# ==============================
def lihat_transaksi():
    cur.execute("SELECT * FROM transaksi ORDER BY id DESC")
    rows = cur.fetchall()

    print("\n=== DAFTAR TRANSAKSI ===")
    for r in rows:
        print(f"[{r[0]}] {r[1]} | {r[2]} | {r[3]} | Rp {r[4]}")
    print("")


# ==============================
# FUNGSI SALDO
# ==============================
def lihat_saldo():
    cur.execute("SELECT SUM(jumlah) FROM transaksi WHERE jenis='masuk'")
    total_masuk = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(jumlah) FROM transaksi WHERE jenis='keluar'")
    total_keluar = cur.fetchone()[0] or 0

    saldo = total_masuk - total_keluar

    print(f"\nTotal pemasukan : Rp {total_masuk}")
    print(f"Total pengeluaran: Rp {total_keluar}")
    print(f"Saldo saat ini   : Rp {saldo}\n")


# ==============================
# MENU
# ==============================
def menu():
    while True:
        print("=== APLIKASI KEUANGAN PYTHON + MYSQL ===")
        print("1. Tambah pemasukan")
        print("2. Tambah pengeluaran")
        print("3. Lihat transaksi")
        print("4. Lihat saldo")
        print("5. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_transaksi("masuk")
        elif pilih == "2":
            tambah_transaksi("keluar")
        elif pilih == "3":
            lihat_transaksi()
        elif pilih == "4":
            lihat_saldo()
        elif pilih == "5":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    menu()

    

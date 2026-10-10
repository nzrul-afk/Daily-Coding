def baca_file_aman(nama_file):
    try:
        with open(nama_file, "r") as baca:
            print(baca.readline())
    except FileNotFoundError:
        print("[CRITICAL] Gagal! File tidak ditemukan di sistem.")
    finally:
        print("Operasi pencarian file selesai.")

baca_file_aman("corrupted_log.txt") 
            
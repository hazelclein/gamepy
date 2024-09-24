import random

def tebak_angka():
    print("Selamat datang di game Tebak Angka!")
    print("Saya sudah memilih angka antara 1 dan 100.")
    
    angka_rahasia = random.randint(1, 100)
    tebakan = None
    percobaan = 0
    
    while tebakan != angka_rahasia:
        try:
            tebakan = int(input("Masukkan tebakan Anda: "))
            percobaan += 1
            
            if tebakan < angka_rahasia:
                print("Tebakan Anda terlalu rendah. Coba lagi!")
            elif tebakan > angka_rahasia:
                print("Tebakan Anda terlalu tinggi. Coba lagi!")
            else:
                print(f"Selamat! Anda berhasil menebak angka {angka_rahasia} dalam {percobaan} percobaan.")
        except ValueError:
            print("Silakan masukkan angka yang valid.")

if __name__ == "__main__":
    tebak_angka()

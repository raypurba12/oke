# submit_manual.py - SEMI OTOMATIS dengan TEMPLATE
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_browser():
    """Buka Chrome browser"""
    print("\n" + "="*60)
    print("SEMI-OTOMATIS GOOGLE FORM FILLER")
    print("="*60)
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-sync")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Browser berhasil dibuka!")
        return driver
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generate_template():
    """Generate template data random"""
    nama_depan = ["Ahmad", "Budi", "Citra", "Dewi", "Eko", "Fitri", "Gunawan", "Hana", "Indra", "Joko", 
                  "Rina", "Agus", "Maya", "Doni", "Lina", "Rudi", "Sari", "Bambang", "Ani", "Hendro"]
    nama_belakang = ["Rizki", "Santoso", "Lestari", "Prasetyo", "Handayani", "Wijaya", "Pertiwi", "Kusuma", 
                     "Susanti", "Setiawan", "Marlina", "Hermawan", "Dewi", "Sutrisno", "Wijayanti", "Saputra"]
    
    jenis_kelamin = ["Laki-laki", "Perempuan"]
    usia = ["<26 Tahun", "20-30 Tahun", "31-40 Tahun", "41-50 Tahun", ">50 Tahun"]
    pekerjaan = ["Mahasiswa", "Pegawai Swasta", "Pegawai Negeri", "Wiraswasta", "Lainnya"]
    pendidikan = ["SMA", "D3", "S1", "S2", "S3"]
    domisili = ["DKI Jakarta", "Jawa Barat", "Jawa Timur", "Jawa Tengah", "DI Yogyakarta", 
                "Banten", "Sumatera Utara", "Sumatera Barat", "Bali", "Sulawesi Selatan"]
    
    # Jawaban Webqual (20 pertanyaan) dengan distribusi weighted
    webqual_options = ["STS (1)", "TS (2)", "N (3)", "S (4)", "SS (5)"]
    webqual_answers = []
    
    for _ in range(20):
        choice = random.choices(
            webqual_options,
            weights=[0.10, 0.15, 0.20, 0.35, 0.20]  # Lebih banyak jawaban positif
        )[0]
        webqual_answers.append(choice)
    
    template = {
        "nama": f"{random.choice(nama_depan)} {random.choice(nama_belakang)}",
        "jenis_kelamin": random.choice(jenis_kelamin),
        "usia": random.choice(usia),
        "pekerjaan": random.choice(pekerjaan),
        "pendidikan": random.choice(pendidikan),
        "domisili": random.choice(domisili),
        "webqual": webqual_answers
    }
    
    return template

def print_template(template, nomor):
    """Tampilkan template dengan format yang bagus"""
    print(f"\n{'='*60}")
    print(f"📋 TEMPLATE PENGISIAN #{nomor}")
    print(f"{'='*60}")
    print(f"Nama           : {template['nama']}")
    print(f"Jenis Kelamin  : {template['jenis_kelamin']}")
    print(f"Usia           : {template['usia']}")
    print(f"Pekerjaan      : {template['pekerjaan']}")
    print(f"Pendidikan     : {template['pendidikan']}")
    print(f"Domisili       : {template['domisili']}")
    print(f"\n📊 20 PERTANYAAN WEBQUAL 4.0:")
    print(f"{'─'*60}")
    
    # Tampilkan dalam 2 kolom untuk lebih compact
    for i in range(0, 20, 2):
        left = f"  {i+1:2d}. {template['webqual'][i]}"
        if i+1 < 20:
            right = f"{i+2:2d}. {template['webqual'][i+1]}"
            print(f"{left:<30} {right}")
        else:
            print(left)
    
    print(f"{'─'*60}")
    print(f"\n💡 Keterangan: STS=Sangat Tidak Setuju, TS=Tidak Setuju,")
    print(f"               N=Netral, S=Setuju, SS=Sangat Setuju")
    print(f"{'='*60}\n")

def main():
    # Setup browser
    driver = setup_browser()
    if not driver:
        return
    
    # Tanya berapa kali mau isi
    print("\n" + "="*60)
    try:
        jumlah = int(input("Mau isi berapa kali? "))
        print(f"✓ Akan mengisi {jumlah} kali")
    except:
        print("❌ Input tidak valid, default 1 kali")
        jumlah = 1
    
    print("\n" + "="*60)
    print("CARA KERJA:")
    print("1. Browser akan membuka form Google")
    print("2. Terminal akan menampilkan TEMPLATE data random")
    print("3. Anda isi form sesuai template (atau ubah sesuai keinginan)")
    print("4. Klik tombol KIRIM di form")
    print("5. Kembali ke terminal, tekan ENTER")
    print("6. Form akan otomatis refresh untuk pengisian berikutnya")
    print("="*60)
    
    url = "https://docs.google.com/forms/d/e/1FAIpQLSc4S3rsa1MQywUMa6MKJK6EUDU2UeO4zeFWGFmsnM-VgsvtLg/viewform"
    
    for i in range(jumlah):
        print(f"\n{'='*60}")
        print(f"🔄 PENGISIAN KE-{i+1} dari {jumlah}")
        print(f"{'='*60}")
        
        # Generate template
        template = generate_template()
        
        # Buka form
        driver.get(url)
        print(f"✓ Form terbuka di browser")
        time.sleep(2)
        
        # Tampilkan template
        print_template(template, i+1)
        
        print("�  Silakan isi form sesuai template di atas")
        print("👉 Klik KIRIM setelah selesai")
        print("👉 Kembali ke sini dan tekan ENTER untuk lanjut\n")
        
        # Tunggu user selesai
        input("⏸  Tekan ENTER setelah selesai submit... ")
        
        print(f"✅ Pengisian ke-{i+1} selesai!")
        
        # Jeda sebentar
        if i < jumlah - 1:
            print(f"\n⏳ Siap untuk pengisian berikutnya...")
            time.sleep(2)
    
    # Selesai
    print("\n" + "="*60)
    print(f"✅ SELESAI! Total {jumlah} pengisian")
    print("="*60)
    
    # Tanya mau tutup browser atau tidak
    print("\nMau tutup browser?")
    tutup = input("Ketik 'y' untuk tutup, atau ENTER untuk biarkan terbuka: ")
    
    if tutup.lower() == 'y':
        driver.quit()
        print("✓ Browser ditutup")
    else:
        print("✓ Browser tetap terbuka")
        print("💡 Tutup manual jika sudah selesai")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Program dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

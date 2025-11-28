# app_manual.py - Web App untuk Manual Filling dengan Template
from flask import Flask, render_template, request, jsonify, session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import secrets
import threading

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Global driver
driver = None
driver_lock = threading.Lock()

# Data untuk generate template
NAMA_DEPAN = ["Ahmad", "Budi", "Citra", "Dewi", "Eko", "Fitri", "Gunawan", "Hana", "Indra", "Joko", 
              "Rina", "Agus", "Maya", "Doni", "Lina", "Rudi", "Sari", "Bambang", "Ani", "Hendro"]
NAMA_BELAKANG = ["Rizki", "Santoso", "Lestari", "Prasetyo", "Handayani", "Wijaya", "Pertiwi", "Kusuma", 
                 "Susanti", "Setiawan", "Marlina", "Hermawan", "Dewi", "Sutrisno", "Wijayanti", "Saputra"]
JENIS_KELAMIN = ["Laki-laki", "Perempuan"]
USIA = ["<26 Tahun", "20-30 Tahun", "31-40 Tahun", "41-50 Tahun", ">50 Tahun"]
PEKERJAAN = ["Mahasiswa", "Pegawai Swasta", "Pegawai Negeri", "Wiraswasta", "Lainnya"]
PENDIDIKAN = ["SMA", "D3", "S1", "S2", "S3"]
DOMISILI = ["DKI Jakarta", "Jawa Barat", "Jawa Timur", "Jawa Tengah", "DI Yogyakarta", 
            "Banten", "Sumatera Utara", "Sumatera Barat", "Bali", "Sulawesi Selatan"]
WEBQUAL_OPTIONS = ["STS", "TS", "N", "S", "SS"]

def setup_driver():
    """Setup Chrome driver"""
    options = Options()
    
    # Production mode (Railway/Docker)
    options.add_argument("--headless")  # Headless mode untuk server
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-sync")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    
    return webdriver.Chrome(options=options)

def generate_template():
    """Generate template data random"""
    webqual_answers = []
    for _ in range(20):
        choice = random.choices(
            WEBQUAL_OPTIONS,
            weights=[0.10, 0.15, 0.20, 0.35, 0.20]
        )[0]
        webqual_answers.append(choice)
    
    return {
        "nama": f"{random.choice(NAMA_DEPAN)} {random.choice(NAMA_BELAKANG)}",
        "jenis_kelamin": random.choice(JENIS_KELAMIN),
        "usia": random.choice(USIA),
        "pekerjaan": random.choice(PEKERJAAN),
        "pendidikan": random.choice(PENDIDIKAN),
        "domisili": random.choice(DOMISILI),
        "webqual": webqual_answers
    }

@app.route('/')
def index():
    return render_template('index_simple.html')

@app.route('/start', methods=['POST'])
def start():
    """Mulai session dan buka browser"""
    global driver
    
    data = request.json
    form_url = data.get('form_url')
    jumlah = int(data.get('jumlah', 1))
    
    # Simpan di session
    session['form_url'] = form_url
    session['jumlah'] = jumlah
    session['current'] = 0
    
    # Setup driver jika belum ada
    with driver_lock:
        if not driver:
            try:
                driver = setup_driver()
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': True})

@app.route('/next-form')
def next_form():
    """Buka form berikutnya di browser"""
    global driver
    
    current = session.get('current', 0)
    jumlah = session.get('jumlah', 1)
    form_url = session.get('form_url', '')
    
    if current >= jumlah:
        return jsonify({'done': True, 'total': jumlah})
    
    session['current'] = current + 1
    
    # Buka form di browser
    with driver_lock:
        if driver:
            try:
                driver.get(form_url)
            except:
                pass
    
    return jsonify({
        'done': False,
        'current': current + 1,
        'total': jumlah
    })

@app.route('/check-submit')
def check_submit():
    """Cek apakah user sudah submit form"""
    global driver
    
    try:
        with driver_lock:
            if driver:
                try:
                    current_url = driver.current_url
                    page_source = driver.page_source.lower()
                    
                    # Cek berbagai indikator submit berhasil
                    indicators = [
                        "terima kasih" in page_source,
                        "respons anda telah direkam" in page_source,
                        "your response has been recorded" in page_source,
                        "formresponse" in current_url,
                        "kirim respons lain" in page_source,
                        "submit another response" in page_source
                    ]
                    
                    if any(indicators):
                        print("✓ Submit terdeteksi!")
                        return jsonify({'submitted': True})
                    else:
                        return jsonify({'submitted': False})
                except Exception as e:
                    print(f"Error check submit: {e}")
                    return jsonify({'submitted': False})
    except:
        pass
    
    return jsonify({'submitted': False})

@app.route('/close-browser', methods=['POST'])
def close_browser():
    """Tutup browser"""
    global driver
    
    with driver_lock:
        if driver:
            try:
                driver.quit()
                driver = None
                return jsonify({'success': True})
            except:
                return jsonify({'success': False})
    
    return jsonify({'success': False})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

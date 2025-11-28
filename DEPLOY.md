# Deploy ke Railway

## Langkah-langkah:

### 1. Persiapan
- Buat akun di [Railway.app](https://railway.app)
- Install Git (jika belum)
- Push code ke GitHub

### 2. Push ke GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO-NAME.git
git push -u origin main
```

### 3. Deploy di Railway
1. Login ke Railway.app
2. Klik "New Project"
3. Pilih "Deploy from GitHub repo"
4. Pilih repository Anda
5. Railway akan otomatis detect Dockerfile
6. Tunggu build selesai (~5-10 menit)
7. Klik "Generate Domain" untuk dapat URL publik

### 4. Environment Variables (Opsional)
Jika perlu, tambahkan di Railway dashboard:
- `PORT` = 5000 (otomatis di-set Railway)

### 5. Akses App
Setelah deploy selesai, buka URL yang diberikan Railway.
Contoh: `https://your-app.up.railway.app`

## Catatan Penting:

### ⚠️ Headless Mode
Browser berjalan dalam mode headless (tidak ada GUI).
User tidak akan lihat browser, tapi form tetap terisi.

### 💰 Biaya
Railway gratis untuk:
- $5 credit/bulan
- ~500 jam runtime
- Cukup untuk testing & usage ringan

Jika habis, upgrade ke plan berbayar ($5/bulan).

### 🔧 Troubleshooting

**Build gagal:**
- Cek logs di Railway dashboard
- Pastikan Dockerfile benar
- Pastikan requirements.txt lengkap

**Chrome crash:**
- Tambahkan `--disable-dev-shm-usage` (sudah ada)
- Upgrade Railway plan jika memory kurang

**Form tidak terisi:**
- Cek logs untuk error
- Test dulu di local sebelum deploy

## Testing Local dengan Docker

```bash
# Build image
docker build -t form-filler .

# Run container
docker run -p 5000:5000 form-filler

# Akses di browser
http://localhost:5000
```

## Update App

Setelah deploy, untuk update:
```bash
git add .
git commit -m "Update"
git push
```

Railway akan otomatis re-deploy.

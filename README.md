# Aplikasi NGASAL - Absensi Digital

Aplikasi web sederhana untuk absensi dengan 2 endpoint berbeda (SS - Kantor dan WH - Rumah).

## Fitur
- ✅ 2 Button untuk absen (SS dan WH)
- ✅ Python Flask Backend
- ✅ Terintegrasi dengan Google Apps Script
- ✅ Konfirmasi dialog sebelum kirim
- ✅ Full response dari server ditampilkan
- ✅ Random VISITORID auto-generated

## Setup

### Requirements
- Python 3.8+
- Flask
- Flask-CORS
- requests

### Installation

1. Clone repository:
```bash
git clone https://github.com/Anggyf55/NGASAL.git
cd NGASAL
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run server:
```bash
python server.py
```

4. Buka browser: `http://localhost:5000`

## Struktur File

```
.
├── index.html       # Frontend HTML/CSS/JavaScript
├── server.py        # Backend Flask
├── requirements.txt # Python dependencies
└── .gitignore
```

## Konfigurasi

Edit `server.py` untuk mengubah data default:

### DEFAULT_DATA_SS (Kantor - Snapshot)
- LATITUDE: -6.187057576827758
- LONGITUDE: 106.82053837546468
- ADDRESS: PGMTA, Jl. K.H. Wahid Hasyim...

### DEFAULT_DATA_WH (Rumah - Work From Home)
- Ubah LATITUDE, LONGITUDE, ADDRESS sesuai lokasi rumah Anda

## API Endpoints

### POST /api/absen/ss
Kirim absen SS (Snapshot - Kantor)

### POST /api/absen/wh  
Kirim absen WH (Work From Home - Rumah)

## Note
- VISITORID di-generate random otomatis
- Setiap klik button ada konfirmasi terlebih dahulu
- Response dari Google Apps Script ditampilkan full

## License
MIT

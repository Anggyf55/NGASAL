from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import os
import uuid

app = Flask(__name__)
CORS(app)

# Google Apps Script URL
GAS_URL = 'https://script.google.com/macros/s/AKfycbyIBXAwP07ts56CEKctmrzMrc_JGIO0skGbmaNGt2Ixix8_SAYb64HrMuGDPUlOgFmQ/callback?nocache_id=8'

# Generate random VISITORID dengan format yang sama
def generate_visitor_id():
    """Generate random VISITORID format: d1167536305195a257cc44b7f5491a23"""
    return 'd' + uuid.uuid4().hex[:31]

# Default data untuk SS (Kantor/Snapshot)
DEFAULT_DATA_SS = {
    "NIK": "00",
    "PASS": "00rtdcgggj",
    "LATITUDE": -6.216638733549987,
    "LONGITUDE": 106.81797119610248,
    "ADDRESS": "Jl. Jenderal Sudirman No.Kav 45, RT.3/RW.4, Karet Semanggi, Kecamatan Setiabudi, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12930, Indonesia",
    "BRANCHNAME": "SAMPOERNA STRATEGIC - Lt. 22",
    "REMARKS": "",
    "VISITORID": generate_visitor_id(),
    "USERAGENT": "android"
}

# Default data untuk WH (Work From Home) - UBAH LATITUDE, LONGITUDE, ADDRESS SESUAI RUMAH ANDA
DEFAULT_DATA_WH = {
    "NIK": "00",
    "PASS": "00rtdcgggj",
    "LATITUDE": -6.187057576827758,  # ← UBAH LATITUDE RUMAH ANDA
    "LONGITUDE": 106.82053837546468,  # ← UBAH LONGITUDE RUMAH ANDA
    "ADDRESS": "PGMTA, Jl. K.H. Wahid Hasyim No.27, RT.10/RW.2, Kb. Kacang, Kecamatan Tanah Abang, Kota Jakarta Pusat, Daerah Khusus Ibukota Jakarta 10240, Indonesia",  # ← UBAH ADDRESS RUMAH ANDA
    "BRANCHNAME": "WORK HUB  - K.H. Wahid Hasyim",
    "REMARKS": "",
    "VISITORID": generate_visitor_id(),
    "USERAGENT": "android"
}

@app.route('/')
def index():
    """Serve HTML file"""
    return send_file('index.html')

@app.route('/api/absen/ss', methods=['POST'])
def absen_ss():
    """Absen SS (Snapshot) - Kantor"""
    return send_absen_to_gas('WFO', DEFAULT_DATA_SS)

@app.route('/api/absen/wh', methods=['POST'])
def absen_wh():
    """Absen WH (Work From Home) - Rumah"""
    return send_absen_to_gas('WFO', DEFAULT_DATA_WH)

def send_absen_to_gas(status, data_template):
    """Generic function to send attendance to Google Apps Script"""
    try:
        # Build attendance data
        attendance_data = data_template.copy()
        attendance_data['STATUS'] = status
        
        # Build request payload exactly like curl
        request_value = [
            "addAttendance",
            json.dumps([attendance_data]),
            None,
            [0],
            None,
            None,
            1,
            0
        ]
        
        request_string = json.dumps(request_value)
        body = 'request=' + requests.utils.quote(request_string)
        
        print(f"📤 Sending request to GAS...")
        print(f"Status: {status}")
        print(f"Body length: {len(body)} bytes")
        
        # Send to Google Apps Script with proper headers (exact copy dari curl)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; SM-G780G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
            'Sec-Ch-Ua-Platform': 'Android',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Sec-Ch-Ua-Mobile': '?1',
            'X-Same-Domain': '1',
            'Origin': 'https://script.google.com',
            'X-Client-Data': 'CLOBywE=',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://script.google.com/'
        }
        
        response = requests.post(GAS_URL, data=body, headers=headers, timeout=10)
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"📨 Response Text:\n{response.text}\n")
        
        return jsonify({
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'message': response.text,  # Full response tanpa extract
            'data': {
                'status': status,
                'nik': data_template['NIK'],
                'latitude': data_template['LATITUDE'],
                'longitude': data_template['LONGITUDE']
            }
        })
        
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'Request timeout - Google Apps Script tidak merespons'
        }), 504
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Network error: {str(e)}'
        }), 500
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Server starting on http://0.0.0.0:" + str(port))
    print(f"📍 Google Apps Script: {GAS_URL}")
    app.run(debug=False, host='0.0.0.0', port=port)


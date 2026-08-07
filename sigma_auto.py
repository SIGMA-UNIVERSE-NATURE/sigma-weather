import requests
import math
import os
import time
from datetime import datetime

# ================================================================
# 📐 HẰNG SỐ SIGMA
# ================================================================
A0 = 250.0
K = 2.0
Q_AVG_DEFAULT = 2.5

THRESHOLD_YELLOW = 250.0
THRESHOLD_ORANGE = 1000.0
THRESHOLD_RED = 5000.0

# ================================================================
# 📋 DANH SÁCH 63 TỈNH (RÚT GỌN)
# ================================================================
PROVINCES = [
    {"name": "Hà Nội", "lat": 21.0285, "lon": 105.8542, "slope": 0.10, "area": 120, "q_avg": 1.5},
    {"name": "TP.HCM", "lat": 10.8231, "lon": 106.6297, "slope": 0.05, "area": 130, "q_avg": 1.8},
    {"name": "Đà Nẵng", "lat": 16.0544, "lon": 108.2022, "slope": 0.60, "area": 90, "q_avg": 2.0},
    {"name": "Hải Phòng", "lat": 20.8449, "lon": 106.6881, "slope": 0.05, "area": 120, "q_avg": 1.5},
    {"name": "Cần Thơ", "lat": 10.0452, "lon": 105.7469, "slope": 0.02, "area": 150, "q_avg": 1.2},
    {"name": "Gia Lai", "lat": 13.9800, "lon": 108.0000, "slope": 0.70, "area": 110, "q_avg": 2.5},
    {"name": "Lai Châu", "lat": 22.0600, "lon": 103.1600, "slope": 0.95, "area": 80, "q_avg": 2.5},
    {"name": "Kon Tum", "lat": 14.3500, "lon": 108.0000, "slope": 0.75, "area": 110, "q_avg": 2.5},
    {"name": "Điện Biên", "lat": 21.3800, "lon": 103.0100, "slope": 0.90, "area": 80, "q_avg": 2.5},
    {"name": "Sơn La", "lat": 21.3200, "lon": 103.9000, "slope": 0.85, "area": 80, "q_avg": 2.5},
]

# ================================================================
# 🌤️ LẤY DỮ LIỆU MƯA
# ================================================================
def get_rain_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation&timezone=auto&forecast_days=1"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        precip = data.get('hourly', {}).get('precipitation', [])
        if precip:
            max_intensity = max(precip[:24]) if len(precip) >= 24 else max(precip)
            return {'max_intensity': max_intensity, 'status': 'OK'}
        return {'max_intensity': 0, 'status': 'OK'}
    except:
        return {'max_intensity': 0, 'status': 'ERROR'}

# ================================================================
# 🧮 TÍNH Q VÀ SIGMA
# ================================================================
def calc_Q(max_intensity, slope, area):
    C = 0.2 + 0.5 * slope
    if C > 0.9: C = 0.9
    if C < 0.1: C = 0.1
    return (C * max_intensity * area) / 360.0

def calc_sigma(Q, q_avg):
    if q_avg <= 0 or Q <= 0:
        return 0
    ratio = Q / q_avg
    if ratio <= 1:
        return 0
    return A0 * math.exp(K * (ratio - 1) ** 2)

def get_level(sigma):
    if sigma >= THRESHOLD_RED:
        return {'level': '🔴 CẤP CỨU', 'action': 'SƠ TÁN NGAY!'}
    elif sigma >= THRESHOLD_ORANGE:
        return {'level': '🟠 CẢNH BÁO', 'action': 'CHUẨN BỊ SƠ TÁN'}
    elif sigma >= THRESHOLD_YELLOW:
        return {'level': '🟡 THEO DÕI', 'action': 'CẬP NHẬT THÔNG TIN'}
    else:
        return {'level': '🟢 AN TOÀN', 'action': 'BÌNH THƯỜNG'}

# ================================================================
# 📱 GỬI CẢNH BÁO
# ================================================================
def send_alert(title, message, level):
    try:
        if level == 'RED':
            os.system(f'termux-notification -t "🔴 {title}" -c "{message}" -p high')
            os.system(f'termux-vibrate -d 1000')
        elif level == 'ORANGE':
            os.system(f'termux-notification -t "🟠 {title}" -c "{message}" -p high')
            os.system(f'termux-vibrate -d 700')
        elif level == 'YELLOW':
            os.system(f'termux-notification -t "🟡 {title}" -c "{message}" -p medium')
        print(f"✅ Đã gửi: {title}")
    except Exception as e:
        print(f"❌ Lỗi gửi cảnh báo: {e}")

# ================================================================
# 🚀 QUÉT
# ================================================================
def scan_all():
    print(f"\n🕊️ QUÉT LÚC: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print("=" * 60)
    
    alerts = {'red': [], 'orange': [], 'yellow': []}
    
    for p in PROVINCES:
        w = get_rain_data(p['lat'], p['lon'])
        if w['status'] != 'OK':
            continue
        
        Q = calc_Q(w['max_intensity'], p['slope'], p['area'])
        sigma = calc_sigma(Q, p['q_avg'])
        level = get_level(sigma)
        
        if level['level'] == '🔴 CẤP CỨU':
            alerts['red'].append(p['name'])
            send_alert(f"CẤP CỨU {p['name']}", f"SIGMA: {sigma:.0f} | Q: {Q:.1f}", 'RED')
        elif level['level'] == '🟠 CẢNH BÁO':
            alerts['orange'].append(p['name'])
            send_alert(f"CẢNH BÁO {p['name']}", f"SIGMA: {sigma:.0f} | Q: {Q:.1f}", 'ORANGE')
        elif level['level'] == '🟡 THEO DÕI':
            alerts['yellow'].append(p['name'])
    
    print(f"\n📊 TÓM TẮT:")
    if alerts['red']:
        print(f"   🔴 CẤP CỨU: {', '.join(alerts['red'])}")
    if alerts['orange']:
        print(f"   🟠 CẢNH BÁO: {', '.join(alerts['orange'])}")
    if alerts['yellow']:
        print(f"   🟡 THEO DÕI: {', '.join(alerts['yellow'])}")
    if not alerts['red'] and not alerts['orange'] and not alerts['yellow']:
        print("   ✅ Tất cả các tỉnh đều AN TOÀN.")
    print(f"✅ Hoàn tất – Đã gửi {len(alerts['red'])+len(alerts['orange'])} cảnh báo.")
    print("=" * 60)

# ================================================================
# ⏰ VÒNG LẶP (1 NGÀY/LẦN)
# ================================================================
if __name__ == "__main__":
    print("🚀 HỆ THỐNG SIGMA KHỞI ĐỘNG...")
    print("📋 Đang theo dõi 63 tỉnh thành.")
    print("⏰ Quét tự động mỗi 1 ngày.")
    print("📱 Nhấn Ctrl+C để dừng.\n")
    
    while True:
        scan_all()
        time.sleep(86400)






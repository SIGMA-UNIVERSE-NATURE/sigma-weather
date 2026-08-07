import requests
import math
import os
import time
import json
from datetime import datetime

# ================================================================
# 📐 HẰNG SỐ SIGMA
# ================================================================
A0 = 360.0
BETA1 = 0.55
BETA2 = 0.04
DECAY = 0.4

# Ngưỡng cảnh báo (đã điều chỉnh để tránh báo động giả)
THRESHOLD_YELLOW = 30.0
THRESHOLD_ORANGE = 50.0
THRESHOLD_RED = 75.0

# ================================================================
# 📋 DANH SÁCH 63 TỈNH THÀNH (ĐÃ CẬP NHẬT ĐẦY ĐỦ)
# ================================================================
PROVINCES = [
    {"name": "Hà Nội", "lat": 21.0285, "lon": 105.8542},
    {"name": "Hải Phòng", "lat": 20.8449, "lon": 106.6881},
    {"name": "Hải Dương", "lat": 20.9400, "lon": 106.3300},
    {"name": "Hưng Yên", "lat": 20.6500, "lon": 106.0600},
    {"name": "Thái Bình", "lat": 20.4500, "lon": 106.3300},
    {"name": "Nam Định", "lat": 20.4300, "lon": 106.1700},
    {"name": "Ninh Bình", "lat": 20.2500, "lon": 105.9700},
    {"name": "Bắc Ninh", "lat": 21.1800, "lon": 106.0600},
    {"name": "Vĩnh Phúc", "lat": 21.3000, "lon": 105.5900},
    {"name": "Phú Thọ", "lat": 21.4000, "lon": 105.2200},
    {"name": "Quảng Ninh", "lat": 20.9500, "lon": 107.0800},
    {"name": "Lạng Sơn", "lat": 21.8400, "lon": 106.7500},
    {"name": "Cao Bằng", "lat": 22.6600, "lon": 106.2600},
    {"name": "Bắc Kạn", "lat": 22.1300, "lon": 105.8300},
    {"name": "Thái Nguyên", "lat": 21.5900, "lon": 105.8300},
    {"name": "Tuyên Quang", "lat": 21.8200, "lon": 105.2100},
    {"name": "Hà Giang", "lat": 22.8200, "lon": 104.9800},
    {"name": "Bắc Giang", "lat": 21.2700, "lon": 106.1900},
    {"name": "Lào Cai", "lat": 22.4800, "lon": 103.9700},
    {"name": "Yên Bái", "lat": 21.7000, "lon": 104.8700},
    {"name": "Sơn La", "lat": 21.3200, "lon": 103.9000},
    {"name": "Điện Biên", "lat": 21.3800, "lon": 103.0100},
    {"name": "Lai Châu", "lat": 22.0600, "lon": 103.1600},
    {"name": "Hòa Bình", "lat": 20.8100, "lon": 105.3300},
    {"name": "Thanh Hóa", "lat": 19.8000, "lon": 105.7700},
    {"name": "Nghệ An", "lat": 18.6700, "lon": 105.6900},
    {"name": "Hà Tĩnh", "lat": 18.3400, "lon": 105.9000},
    {"name": "Quảng Bình", "lat": 17.4700, "lon": 106.6200},
    {"name": "Quảng Trị", "lat": 16.7500, "lon": 107.1800},
    {"name": "Thừa Thiên Huế", "lat": 16.4700, "lon": 107.5900},
    {"name": "Đà Nẵng", "lat": 16.0544, "lon": 108.2022},
    {"name": "Quảng Nam", "lat": 15.5700, "lon": 108.4900},
    {"name": "Quảng Ngãi", "lat": 15.1200, "lon": 108.8000},
    {"name": "Bình Định", "lat": 13.7700, "lon": 109.2300},
    {"name": "Phú Yên", "lat": 13.0800, "lon": 109.2900},
    {"name": "Khánh Hòa", "lat": 12.2400, "lon": 109.1900},
    {"name": "Ninh Thuận", "lat": 11.5600, "lon": 108.9800},
    {"name": "Bình Thuận", "lat": 10.9300, "lon": 108.1000},
    {"name": "Kon Tum", "lat": 14.3500, "lon": 108.0000},
    {"name": "Gia Lai", "lat": 13.9800, "lon": 108.0000},
    {"name": "Đắk Lắk", "lat": 12.6600, "lon": 108.0300},
    {"name": "Đắk Nông", "lat": 12.7100, "lon": 107.6000},
    {"name": "Lâm Đồng", "lat": 11.9400, "lon": 108.4400},
    {"name": "TP.HCM", "lat": 10.8231, "lon": 106.6297},
    {"name": "Bình Phước", "lat": 11.7500, "lon": 106.8800},
    {"name": "Tây Ninh", "lat": 11.3200, "lon": 106.1200},
    {"name": "Bình Dương", "lat": 11.0800, "lon": 106.8000},
    {"name": "Đồng Nai", "lat": 10.9500, "lon": 107.0600},
    {"name": "Bà Rịa - Vũng Tàu", "lat": 10.3400, "lon": 107.0900},
    {"name": "Long An", "lat": 10.5300, "lon": 106.4000},
    {"name": "Tiền Giang", "lat": 10.3500, "lon": 106.3600},
    {"name": "Bến Tre", "lat": 10.2300, "lon": 106.3700},
    {"name": "Trà Vinh", "lat": 9.9300, "lon": 106.3400},
    {"name": "Vĩnh Long", "lat": 10.2500, "lon": 105.9700},
    {"name": "Đồng Tháp", "lat": 10.4600, "lon": 105.6200},
    {"name": "Cần Thơ", "lat": 10.0452, "lon": 105.7469},
    {"name": "An Giang", "lat": 10.3800, "lon": 105.4300},
    {"name": "Kiên Giang", "lat": 10.0200, "lon": 105.1100},
    {"name": "Cà Mau", "lat": 9.1800, "lon": 105.1500},
    {"name": "Sóc Trăng", "lat": 9.6000, "lon": 105.9700},
    {"name": "Bạc Liêu", "lat": 9.2900, "lon": 105.7200},
    {"name": "Hậu Giang", "lat": 9.7800, "lon": 105.4700},
]

# ================================================================
# 🌤️ HÀM LẤY DỮ LIỆU MƯA
# ================================================================
def get_rain_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation&timezone=auto&forecast_days=1"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        precip = data.get('hourly', {}).get('precipitation', [])
        if not precip:
            return None
        r_24h = sum(precip[:24])
        r_1h = max(precip[:24]) if precip[:24] else 0
        peak_hour = precip.index(r_1h) if r_1h > 0 else 0
        return {'r_24h': round(r_24h, 1), 'r_1h': round(r_1h, 1), 'peak_hour': peak_hour}
    except Exception as e:
        return None

# ================================================================
# 🧮 TÍNH Q VÀ SIGMA
# ================================================================
def calculate_Q(r_24h):
    return BETA1 * r_24h + BETA2 * (r_24h ** 2)

def calculate_sigma(Q, current_hour, peak_hour):
    delta = current_hour - peak_hour
    return A0 * math.exp(-DECAY * (delta ** 2))

# ================================================================
# 📱 GỬI CẢNH BÁO (OPPO)
# ================================================================
def send_alert(title, message, level):
    try:
        if level == 'RED':
            os.system(f'termux-notification -t "🔴 {title}" -c "{message}" -p high')
            os.system(f'termux-vibrate -d 1000')
            os.system(f'termux-tts-speak "{message}" 2>/dev/null')
        elif level == 'ORANGE':
            os.system(f'termux-notification -t "🟠 {title}" -c "{message}" -p high')
            os.system(f'termux-vibrate -d 700')
        elif level == 'YELLOW':
            os.system(f'termux-notification -t "🟡 {title}" -c "{message}" -p medium')
        print(f"✅ Đã gửi: {title}")
    except Exception as e:
        print(f"❌ Lỗi gửi: {e}")

# ================================================================
# 🚀 HÀM QUÉT
# ================================================================
def scan_all():
    print(f"\n🕊️ QUÉT LÚC: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print("=" * 60)
    
    current_hour = datetime.now().hour + datetime.now().minute / 60.0
    alert_count = 0
    red_alerts = []
    orange_alerts = []
    yellow_alerts = []
    
    for p in PROVINCES:
        data = get_rain_data(p['lat'], p['lon'])
        if not data:
            continue
        
        Q = calculate_Q(data['r_24h'])
        sigma = calculate_sigma(Q, current_hour, data['peak_hour'])
        
        if sigma >= THRESHOLD_RED:
            send_alert(f"CẤP CỨU {p['name']}", f"SIGMA: {sigma:.1f} | Q: {Q:.1f} m³/s", 'RED')
            red_alerts.append(p['name'])
            alert_count += 1
        elif sigma >= THRESHOLD_ORANGE:
            send_alert(f"CẢNH BÁO {p['name']}", f"SIGMA: {sigma:.1f} | Q: {Q:.1f} m³/s", 'ORANGE')
            orange_alerts.append(p['name'])
            alert_count += 1
        elif sigma >= THRESHOLD_YELLOW:
            send_alert(f"THEO DÕI {p['name']}", f"SIGMA: {sigma:.1f} | Q: {Q:.1f} m³/s", 'YELLOW')
            yellow_alerts.append(p['name'])
            alert_count += 1
    
    # Báo cáo tóm tắt
    print(f"\n📊 TÓM TẮT:")
    if red_alerts:
        print(f"   🔴 CẤP CỨU: {', '.join(red_alerts)}")
    if orange_alerts:
        print(f"   🟠 CẢNH BÁO: {', '.join(orange_alerts)}")
    if yellow_alerts:
        print(f"   🟡 THEO DÕI: {', '.join(yellow_alerts)}")
    if not red_alerts and not orange_alerts and not yellow_alerts:
        print("   ✅ Tất cả các tỉnh đều AN TOÀN.")
    
    print(f"✅ Hoàn tất – Đã gửi {alert_count} cảnh báo.")
    print("=" * 60)

# ================================================================
# ⏰ VÒNG LẶP 20 PHÚT
# ================================================================
if __name__ == "__main__":
    print("🚀 HỆ THỐNG SIGMA KHỞI ĐỘNG...")
    print("📋 Đang theo dõi 63 tỉnh thành.")
    print("⏰ Quét tự động mỗi 20 phút.")
    print("📱 Nhấn Ctrl+C để dừng.\n")
    
    while True:
        scan_all()
        print("⏰ Chờ 20 phút...")
        time.sleep(1200)

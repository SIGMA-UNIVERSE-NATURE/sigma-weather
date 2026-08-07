import requests
import math
import json
import os
from datetime import datetime

# ================================================================
# 📐 HẰNG SỐ SIGMA
# ================================================================
A0 = 360.0
BETA1 = 0.55
BETA2 = 0.04

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
    except:
        return None

# ================================================================
# 🧮 TÍNH Q VÀ SIGMA
# ================================================================
def calculate_Q(r_24h):
    return BETA1 * r_24h + BETA2 * (r_24h ** 2)

def calculate_sigma(Q, current_hour, peak_hour, decay=0.4):
    delta = current_hour - peak_hour
    return A0 * math.exp(-decay * (delta ** 2))

# ================================================================
# 📱 GỬI CẢNH BÁO (OPPO)
# ================================================================
def send_alert(title, message, level):
    try:
        if level == 'RED':
            os.system(f'termux-notification -t "🔴 {title}" -c "{message}" -p high')
            os.system(f'termux-vibrate -d 1000')
            os.system(f'termux-tts-speak "{message}"')
        elif level == 'ORANGE':
            os.system(f'termux-notification -t "🟠 {title}" -c "{message}" -p high')
            os.system(f'termux-vibrate -d 700')
        elif level == 'YELLOW':
            os.system(f'termux-notification -t "🟡 {title}" -c "{message}" -p medium')
        print(f"✅ Đã gửi: {title}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

# ================================================================
# 🚀 CHƯƠNG TRÌNH CHÍNH
# ================================================================
def main():
    print(f"\n🕊️ SIGMA ALERT - {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    
    # Tỉnh Gia Lai – nơi đang có mưa lớn
    lat, lon = 13.98, 108.00
    data = get_rain_data(lat, lon)
    
    if not data:
        print("❌ Không lấy được dữ liệu.")
        return
    
    Q = calculate_Q(data['r_24h'])
    current_hour = datetime.now().hour + datetime.now().minute / 60.0
    sigma = calculate_sigma(Q, current_hour, data['peak_hour'])
    
    print(f"📍 Gia Lai | Mưa 24h: {data['r_24h']}mm | Q: {Q:.1f} | SIGMA: {sigma:.1f}")
    
    if sigma >= 75:
        send_alert(f"CẤP CỨU Gia Lai", f"SIGMA: {sigma:.1f}, Q: {Q:.1f}", 'RED')
    elif sigma >= 50:
        send_alert(f"CẢNH BÁO Gia Lai", f"SIGMA: {sigma:.1f}, Q: {Q:.1f}", 'ORANGE')
    elif sigma >= 30:
        send_alert(f"THEO DÕI Gia Lai", f"SIGMA: {sigma:.1f}, Q: {Q:.1f}", 'YELLOW')
    else:
        print("✅ AN TOÀN – Không có cảnh báo.")

if __name__ == "__main__":
    main()


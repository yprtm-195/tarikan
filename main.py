import requests
import base64
import json
import time
import random
import os
from datetime import datetime # Tambahkan import ini

# --- KONSTANTA ---
# URL Apps Script untuk mengambil konfigurasi input
APPS_SCRIPT_CONFIG_URL = "https://script.google.com/macros/s/AKfycbwu0GTeV9Qtdip_TtI-gYh-vR0bcquQSG3Mo0tVhyt8EWWkd3rEisv9xO9BNOfGeTAO/exec"

# URL Apps Script untuk mengirim hasil scraping
APPS_SCRIPT_OUTPUT_URL = os.environ.get("APPS_SCRIPT_OUTPUT_URL", "https://script.google.com/macros/s/AKfycbwu0GTeV9Qtdip_TtI-gYh-vR0bcquQSG3Mo0tVhyt8EWWkd3rEisv9xO9BNOfGeTAO/exec")

# Keywords yang akan dicari
KEYWORDS = ["cimory", "kanzler"]

# URL API Alfagift
API_URL = "https://webcommerce-gw.alfagift.id/v2/products/searches"

# Headers statis untuk permintaan API
STATIC_HEADERS = {
    'accept': 'application/json',
    'accept-language': 'id',
    'devicemodel': 'chrome',
    'devicetype': 'Web',
    'fingerprint': 'XZ83Mtc0WRlnPTpgVdH6wfTzBg8ifrSx6CmR0RKLDtkAw9IuhDVATi7qPjylV6IG', 
    'latitude': '0',
    'longitude': '0',
    'origin': 'https://alfagift.id',
    'priority': 'u=1, i',
    'referer': 'https://alfagift.id/',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'trxid': '4557999812', 
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

# --- FUNGSI-FUNGSI UTAMA ---

def fetch_config_from_apps_script(url):
    """
    Mengambil data konfigurasi (stores, tokens, products) dari URL Apps Script.
    """
    print(f"Mengambil konfigurasi dari Apps Script URL: {url}")
    try:
        response = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # Akan raise HTTPError untuk status kode 4xx/5xx
        config = response.json()
        print("Konfigurasi berhasil diambil.")
        return config
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil konfigurasi dari Apps Script: {e}")
        return None

def encode_base64_json(data_dict):
    """
    Meng-encode dictionary ke JSON string, lalu Base64.
    """
    json_string = json.dumps(data_dict, separators=(',', ':')) # Compact JSON
    encoded_bytes = base64.b64encode(json_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def make_api_request(store_info, current_token, keyword, static_headers):
    """
    Membuat dan mengirim permintaan API ke Alfagift.
    """
    print(f"Mengambil data {keyword} untuk toko: {store_info['store_code']}")
    
    # Buat header storecode yang di-encode
    storecode_payload = {
        "store_code": store_info['store_code'],
        "delivery": True,
        "depo_id": "",
        "sapa": True,
        "store_method": 1,
        "distance": 0, 
        "maxDistance": None,
        "flagRoute": store_info['flagroute']
    }
    encoded_storecode = encode_base64_json(storecode_payload)

    # Buat header fccode yang di-encode
    fccode_payload = {
        "seller_id": "1",
        "fc_code": store_info['fc_code']
    }
    encoded_fccode = encode_base64_json(fccode_payload)

    # Gabungkan semua header
    headers = static_headers.copy()
    headers['storecode'] = encoded_storecode
    headers['fccode'] = encoded_fccode
    headers['token'] = current_token

    # Parameter query
    params = {
        'keyword': keyword,
        'start': 0, # Atau disesuaikan jika pagination dibutuhkan
        'limit': 60 # Sesuai dengan yang dibahas
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil data dari API untuk {store_info['store_code']} ({keyword}): {e}")
        # Tambahkan logging untuk melihat respons mentah dari server jika ada error
        if e.response is not None:
            print(f"DEBUG: Status Code: {e.response.status_code}")
            print(f"DEBUG: Response Body: {e.response.text}")
        return None

def process_products_for_historical_record(api_response, filter_product_names, store_info):
    """
    Memproses respons API dan memfilter produk berdasarkan nama,
    lalu menambahkan metadata toko dan tanggal.
    """
    historical_records = []
    current_date = datetime.now().strftime('%Y-%m-%d') # Format tanggal YYYY-MM-DD
    
    if api_response and 'products' in api_response:
        for product in api_response['products']:
            if product.get('productName') in filter_product_names:
                historical_records.append({
                    'Tanggal': current_date,
                    'Kode toko': store_info.get('store_code'),
                    'Nama Toko': store_info.get('store_name'),
                    'Cabang': store_info.get('fc_code'),
                    'Nama Produk': product.get('productName'),
                    'Stok': product.get('stock')
                })
    return historical_records

def send_results_to_apps_script(url, data_to_send):
    """
    Mengirim hasil scraping ke Apps Script URL untuk ditulis ke Google Sheet.
    """
    if not data_to_send:
        print("Tidak ada data untuk dikirim ke Apps Script.")
        return

    print(f"Mengirim {len(data_to_send)} baris data ke Apps Script URL: {url}")
    try:
        # Kirim seluruh data (sekarang sudah tidak dipivot, jadi list of dicts)
        payload = {'data': data_to_send}
        response = requests.post(url, json=payload, timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        print("Data berhasil dikirim ke Apps Script.")
        print(f"Respons Apps Script: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengirim data ke Apps Script: {e}")

def main():
    """
    Fungsi utama untuk menjalankan seluruh proses scraping.
    """
    # 1. Ambil konfigurasi dari Apps Script URL
    config = fetch_config_from_apps_script(APPS_SCRIPT_CONFIG_URL)
    if not config:
        print("Gagal mengambil konfigurasi. Keluar.")
        return

    stores_data = config.get("stores", [])
    tokens_data = [str(token) for token in config.get("tokens", [])]
    filter_product_names = set(config.get("products", []))
    print(f"DEBUG: {len(filter_product_names)} nama produk filter berhasil dimuat.")

    if not stores_data:
        print("Tidak ada data toko yang ditemukan di konfigurasi. Keluar.")
        return
    if not tokens_data:
        print("Tidak ada token yang ditemukan di konfigurasi. Keluar.")
        return
    if not filter_product_names:
        print("Tidak ada nama produk filter yang ditemukan di konfigurasi. Keluar.")
        return

    all_scraped_data_long = []
    token_index = 0
    
    # 2. Proses Scraping dengan Batching dan Delay
    print(f"Memulai scraping untuk {len(stores_data)} toko...")
    
    stores_to_process = stores_data # Proses semua toko secara default

    for i in range(0, len(stores_to_process), 5):
        batch_stores = stores_to_process[i:i+5]
        print(f"\n--- Memproses batch toko: {i+1} sampai {min(i+5, len(stores_to_process))} ---")

        for store_info in batch_stores:
            current_token = tokens_data[token_index % len(tokens_data)]
            token_index += 1

            for keyword in KEYWORDS:
                api_response = make_api_request(store_info, current_token, keyword, STATIC_HEADERS)
                if api_response:
                    # Menggunakan fungsi baru untuk historical record
                    historical_records = process_products_for_historical_record(api_response, filter_product_names, store_info)
                    all_scraped_data_long.extend(historical_records)
            
            delay_intra_batch = random.uniform(1, 3)
            print(f"Jeda antar toko ({store_info['store_code']}): {delay_intra_batch:.2f} detik.")
            time.sleep(delay_intra_batch)
        
        if i + 5 < len(stores_to_process):
            delay_inter_batch = random.uniform(1, 3)
            print(f"Jeda antar batch: {delay_inter_batch:.2f} detik.")
            time.sleep(delay_inter_batch)

    # 3. Kirim hasil yang sudah dalam format panjang ke Apps Script
    print(f"\nDEBUG: Total record siap dikirim: {len(all_scraped_data_long)}")
    if all_scraped_data_long:
        send_results_to_apps_script(APPS_SCRIPT_OUTPUT_URL, all_scraped_data_long)
    else:
        print("Tidak ada data yang berhasil diambil atau difilter untuk disimpan.")

    print("\nProses scraping selesai!")

if __name__ == "__main__":
    main()
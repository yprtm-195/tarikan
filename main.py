import requests
import base64
import json
import time
import random
import os
from datetime import datetime

# --- KONSTANTA ---
APPS_SCRIPT_CONFIG_URL = "https://script.google.com/macros/s/AKfycbwu0GTeV9Qtdip_TtI-gYh-vR0bcquQSG3Mo0tVhyt8EWWkd3rEisv9xO9BNOfGeTAO/exec"
APPS_SCRIPT_OUTPUT_URL = os.environ.get("APPS_SCRIPT_OUTPUT_URL", "https://script.google.com/macros/s/AKfycbwu0GTeV9Qtdip_TtI-gYh-vR0bcquQSG3Mo0tVhyt8EWWkd3rEisv9xO9BNOfGeTAO/exec")
KEYWORDS = ["cimory", "kanzler"]
API_URL = "https://webcommerce-gw.alfagift.id/v2/products/searches"

# Konfigurasi Retry
MAX_RETRIES = 3
RETRY_DELAY = 5 # detik

STATIC_HEADERS = {
    'accept': 'application/json', 'accept-language': 'id', 'devicemodel': 'chrome',
    'devicetype': 'Web', 'fingerprint': 'XZ83Mtc0WRlnPTpgVdH6wfTzBg8ifrSx6CmR0RKLDtkAw9IuhDVATi7qPjylV6IG',
    'latitude': '0', 'longitude': '0', 'origin': 'https://alfagift.id', 'priority': 'u=1, i',
    'referer': 'https://alfagift.id/', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'trxid': '4557999812',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

# --- FUNGSI-FUNGSI UTAMA ---

def fetch_config_from_apps_script(url):
    print(f"Mengambil konfigurasi dari Apps Script URL: {url}")
    try:
        response = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        config = response.json()
        print("Konfigurasi berhasil diambil.")
        return config
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil konfigurasi dari Apps Script: {e}")
        if e.response is not None:
            print(f"DEBUG: Status Code: {e.response.status_code}")
            print(f"DEBUG: Response Body: {e.response.text}")
        return None

def encode_base64_json(data_dict):
    json_string = json.dumps(data_dict, separators=(',', ':'))
    encoded_bytes = base64.b64encode(json_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def make_api_request(store_info, current_token, keyword, static_headers):
    store_code = store_info['store_code']
    storecode_payload = {
        "store_code": store_code, "delivery": True, "depo_id": "", "sapa": True,
        "store_method": 1, "distance": 0, "maxDistance": None, "flagRoute": store_info['flagroute']
    }
    fccode_payload = {"seller_id": "1", "fc_code": store_info['fc_code']}
    headers = static_headers.copy()
    headers['storecode'] = encode_base64_json(storecode_payload)
    headers['fccode'] = encode_base64_json(fccode_payload)
    headers['token'] = current_token
    params = {'keyword': keyword, 'start': 0, 'limit': 60}

    for attempt in range(MAX_RETRIES):
        try:
            print(f"Mengambil data {keyword} untuk toko: {store_code} (Percobaan {attempt + 1})")
            response = requests.get(API_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error pada percobaan {attempt + 1} untuk {store_code} ({keyword}): {e}")
            if e.response is not None:
                print(f"DEBUG: Status Code: {e.response.status_code}")
                print(f"DEBUG: Response Body: {e.response.text}")
            
            if attempt < MAX_RETRIES - 1:
                print(f"Mencoba lagi dalam {RETRY_DELAY} detik...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Semua {MAX_RETRIES} percobaan gagal untuk {store_code} ({keyword}). Melewatkan toko ini.")
                return None

def process_products_for_historical_record(api_response, filter_product_names, store_info):
    historical_records = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    if api_response and 'products' in api_response:
        for product in api_response['products']:
            if product.get('productName') in filter_product_names:
                stock_value = product.get('stock', 0)
                if isinstance(stock_value, (int, float)) and stock_value < 0:
                    stock_value = abs(stock_value)
                
                historical_records.append({
                    'Tanggal': current_date,
                    'Kode toko': store_info.get('store_code'),
                    'Nama Toko': store_info.get('store_name'),
                    'Cabang': store_info.get('fc_code'),
                    'Nama Produk': product.get('productName'),
                    'Stok': stock_value
                })
    return historical_records
    
def get_raw_products_for_pivot(api_response, filter_product_names, store_code):
    raw_products = []
    if api_response and 'products' in api_response:
        for product in api_response['products']:
            if product.get('productName') in filter_product_names:
                stock_value = product.get('stock', 0)
                if isinstance(stock_value, (int, float)) and stock_value < 0:
                    stock_value = abs(stock_value)

                raw_products.append({
                    'store_code': store_code,
                    'productName': product.get('productName'),
                    'stock': stock_value
                })
    return raw_products

def pivot_scraped_data(scraped_data, stores_data, filter_product_names):
    print("Memulai proses pivot data...")
    product_headers = sorted(list(filter_product_names))
    final_headers = ['Kode toko', 'Nama Toko', 'Cabang'] + product_headers
    store_metadata_map = {store['store_code']: store for store in stores_data}
    pivoted_data = {}
    for item in scraped_data:
        store_code = item['store_code']
        product_name = item['productName']
        stock = item['stock']
        if store_code not in pivoted_data:
            metadata = store_metadata_map.get(store_code, {})
            pivoted_data[store_code] = {
                'Kode toko': store_code,
                'Nama Toko': metadata.get('store_name', 'N/A'),
                'Cabang': metadata.get('fc_code', 'N/A')
            }
            for p_header in product_headers:
                pivoted_data[store_code][p_header] = 0
        if product_name in pivoted_data[store_code]:
            pivoted_data[store_code][product_name] = stock
    final_rows = [final_headers]
    for store_code in sorted(pivoted_data.keys()):
        row_dict = pivoted_data[store_code]
        row_list = [row_dict.get(header, 0) for header in final_headers]
        final_rows.append(row_list)
    print("Proses pivot data selesai.")
    return final_rows

def send_results_to_apps_script(url, data_to_send, output_type):
    if not data_to_send:
        print(f"Tidak ada data untuk dikirim untuk tipe output: {output_type}")
        return
    print(f"Mengirim {len(data_to_send)} baris data ({output_type}) ke Apps Script URL...")
    try:
        payload = {'type': output_type, 'data': data_to_send}
        response = requests.post(url, json=payload, timeout=90, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        print(f"Data ({output_type}) berhasil dikirim. Respons: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengirim data ({output_type}): {e}")

def main():
    print('Memulai scraping Alfagift...')
    config = fetch_config_from_apps_script(APPS_SCRIPT_CONFIG_URL)
    if not config:
        return
    stores_data = config.get("stores", [])
    tokens_data = [str(token) for token in config.get("tokens", [])]
    filter_product_names = set(config.get("products", []))
    print(f"DEBUG: {len(filter_product_names)} nama produk filter berhasil dimuat.")
    if not all([stores_data, tokens_data, filter_product_names]):
        print("Data konfigurasi tidak lengkap.")
        return

    all_historical_records = []
    all_raw_products_for_pivot = []
    token_index = 0
    print(f"Memulai scraping untuk {len(stores_data)} toko...")
    for i in range(0, len(stores_data), 5):
        batch_stores = stores_data[i:i+5]
        print(f"\n--- Memproses batch toko: {i+1} sampai {min(i+5, len(stores_data))} ---")
        for store_info in batch_stores:
            current_token = tokens_data[token_index % len(tokens_data)]
            token_index += 1
            
            # Temporary storage for products from this store/keyword
            store_keyword_products_historical = []
            store_keyword_products_pivot = []

            for keyword in KEYWORDS:
                api_response = make_api_request(store_info, current_token, keyword, STATIC_HEADERS)
                if api_response:
                    historical_records = process_products_for_historical_record(api_response, filter_product_names, store_info)
                    store_keyword_products_historical.extend(historical_records)
                    
                    raw_products_for_pivot = get_raw_products_for_pivot(api_response, filter_product_names, store_info['store_code'])
                    store_keyword_products_pivot.extend(raw_products_for_pivot)
            
            # After processing all keywords for a single store, print the count
            print(f"Toko {store_info['store_code']}: Berhasil menarik total {len(store_keyword_products_historical)} produk.")
            all_historical_records.extend(store_keyword_products_historical)
            all_raw_products_for_pivot.extend(store_keyword_products_pivot)

            delay_intra_batch = random.uniform(1, 3)
            print(f"Jeda antar toko ({store_info['store_code']}): {delay_intra_batch:.2f} detik.")
            time.sleep(delay_intra_batch)
        if i + 5 < len(stores_data):
            delay_inter_batch = random.uniform(1, 3)
            print(f"Jeda antar batch: {delay_inter_batch:.2f} detik.")
            time.sleep(delay_inter_batch)

    if all_historical_records:
        send_results_to_apps_script(APPS_SCRIPT_OUTPUT_URL, all_historical_records, 'historical')
    else:
        print("Tidak ada data historis yang berhasil diambil untuk disimpan.")
        
    if all_raw_products_for_pivot:
        pivoted_data = pivot_scraped_data(all_raw_products_for_pivot, stores_data, filter_product_names)
        send_results_to_apps_script(APPS_SCRIPT_OUTPUT_URL, pivoted_data, 'pivot')
    else:
        print("Tidak ada data pivot yang berhasil diambil untuk disimpan.")

    print("\nProses scraping selesai!")

if __name__ == "__main__":
    main()
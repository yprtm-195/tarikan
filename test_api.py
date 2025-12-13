import requests
import base64
import json

# --- KONSTANTA ---
API_URL = "https://webcommerce-gw.alfagift.id/v2/products/searches"
TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2MmZlMGY3MzFlODYzNzYzNGY2Mzg5YzMiLCJzdWIiOiJ5b2hhbmRpLnByYXRhbWFAZ21haWwuY29tIiwiaXNzIjoid2ViY29tbWVyY2V8c2Vzc2lvbnxXRUIiLCJleHAiOjE3NjgwMjAwODcsImlhdCI6MTc2NTQyODA4N30.yoFbxrH26xOdBQS5yGcZ4nHmL3GJf-owGbfrb-tTr1g"
APPS_SCRIPT_OUTPUT_URL = "https://script.google.com/macros/s/AKfycbwu0GTeV9Qtdip_TtI-gYh-vR0bcquQSG3Mo0tVhyt8EWWkd3rEisv9xO9BNOfGeTAO/exec"

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
    
    storecode_payload = {
        "store_code": store_info['store_code'], "delivery": True, "depo_id": "", "sapa": True,
        "store_method": 1, "distance": 0, "maxDistance": None, "flagRoute": store_info['flagroute']
    }
    encoded_storecode = encode_base64_json(storecode_payload)

    fccode_payload = {"seller_id": "1", "fc_code": store_info['fc_code']}
    encoded_fccode = encode_base64_json(fccode_payload)

    headers = static_headers.copy()
    headers['storecode'] = encoded_storecode
    headers['fccode'] = encoded_fccode
    headers['token'] = current_token

    params = {'keyword': keyword, 'start': 0, 'limit': 60}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil data dari API: {e}")
        return None

def process_and_filter_products(api_response, filter_product_names, store_code):
    """
    Memproses respons API dan memfilter produk berdasarkan nama.
    """
    filtered_products_data = []
    if api_response and 'products' in api_response:
        for product in api_response['products']:
            if product.get('productName') in filter_product_names:
                filtered_products_data.append({
                    'store_code': store_code, 
                    'productName': product.get('productName'),
                    'stock': product.get('stock')
                })
    return filtered_products_data

def pivot_scraped_data(scraped_data, stores_data, filter_product_names):
    """
    Mengubah data dari format panjang ke format lebar (pivot).
    """
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

def send_results_to_apps_script(url, pivoted_data):
    """
    Mengirim hasil scraping yang sudah dipivot ke Apps Script URL.
    """
    if not pivoted_data or len(pivoted_data) <= 1:
        print("Tidak ada data untuk dikirim ke Apps Script.")
        return

    print(f"Mengirim {len(pivoted_data) - 1} baris data ke Apps Script URL: {url}")
    try:
        payload = {'data': pivoted_data}
        response = requests.post(url, json=payload, timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        print("Data berhasil dikirim ke Apps Script.")
        print(f"Respons Apps Script: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengirim data ke Apps Script: {e}")

if __name__ == "__main__":
    test_store_info = [{
        "store_code": "1YB8",
        "store_name": "ARIE LASUT MANADO [ALMA]",
        "fc_code": "1YZ1",
        "flagroute": "1Y14"
    }]
    
    # Untuk testing, kita hardcode beberapa nama produk yang kita harapkan ada
    filter_product_names = {
        "Cimory Susu UHT Matcha 250 ml",
        "Cimory Susu UHT Cokelat 250 ml",
        "Kanzler Bakso Keju 48 g",
        "Kanzler Bakso Pedas 48 g",
        # Tambahkan lebih banyak nama produk di sini jika perlu
    }
    
    all_scraped_data_long = []

    print("\n--- Testing 'cimory' ---")
    cimory_response = make_api_request(test_store_info[0], TEST_TOKEN, "cimory", STATIC_HEADERS)
    if cimory_response:
        filtered = process_and_filter_products(cimory_response, filter_product_names, test_store_info[0]['store_code'])
        all_scraped_data_long.extend(filtered)

    print("\n--- Testing 'kanzler' ---")
    kanzler_response = make_api_request(test_store_info[0], TEST_TOKEN, "kanzler", STATIC_HEADERS)
    if kanzler_response:
        filtered = process_and_filter_products(kanzler_response, filter_product_names, test_store_info[0]['store_code'])
        all_scraped_data_long.extend(filtered)

    if all_scraped_data_long:
        pivoted_data = pivot_scraped_data(all_scraped_data_long, test_store_info, filter_product_names)
        send_results_to_apps_script(APPS_SCRIPT_OUTPUT_URL, pivoted_data)
    else:
        print("Tidak ada produk yang cocok dengan filter, tidak ada data untuk dikirim.")
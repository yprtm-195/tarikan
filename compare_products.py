import json

# Data dari user (yang lu kasih tadi)
user_product_list = [
    "Cimory Eat Milk Puding Susu Rasa Cokelat 80 g",
    "Cimory Eat Milk Puding Susu Rasa Cokelat Hazelnut 80 g",
    "Cimory Eat Milk Puding Susu Rasa Marie Biskuit 80 g",
    "Kanzler Naget Ayam Original 450 g",
    "Kanzler Naget Ayam Krispi 450 g",
    "Kanzler Singles Sosis Sapi & Ayam Original 65 g",
    "Kanzler Singles Sosis Sapi & Ayam Keju 65 g",
    "Kanzler Singles Sosis Sapi & Ayam Mini 65 g",
    "Kanzler Sosis Sapi Coktail 250 g",
    "Kanzler Singles Sosis Sapi & Ayam Pedas 65 g",
    "Kanzler Stik Naget Ayam Krispi 450 g",
    "Kanzler Bakso Original 48 g",
    "Kanzler Bakso Keju 48 g",
    "Kanzler Bakso Pedas 48 g",
    "Kanzler Singles Sosis Sapi & Ayam Gochujang 60 g",
    "Kanzler Naget Ayam Krispi Pedas 450 g",
    "Kanzler Singles Bakso Gochujang 55 g",
    "Cimory Susu UHT Cokelat 250 ml",
    "Cimory Susu UHT Matcha 250 ml",
    "Cimory Susu UHT Stroberi 250 ml",
    "Cimory Susu UHT Cokelat Kotak 125 ml",
    "Cimory Susu UHT Cokelat Hazelnut Kotak 250 ml",
    "Cimory Susu UHT Cokelat Almond Kotak 250 ml",
    "Cimory Susu UHT Cokelat Cashew Kotak 250 ml",
    "Cimory Susu UHT Malt Cokelat Kotak 250 ml",
    "Cimory Susu UHT Biskuit Marie 250 ml",
    "Cimory Susu UHT Bebas Laktosa Kotak 250 ml",
    "Cimory Susu UHT Cokelat Tiramisu 250 ml",
    "Cimory Susu UHT Choco Mint Kotak 250 ml",
    "Cimory Susu UHT Milk Tea 250 ml",
    "Cimory Susu UHT Thai Tea 250 ml",
    "Cimory Susu UHT Cokelat Kotak 750 ml",
    "Cimory Susu UHT Cokelat Almond Kotak 750 ml",
    "Cimory Yogurt Squeeze Original 120 g",
    "Cimory Yogurt Squeeze Stroberi 120 g",
    "Cimory Yogurt Squeeze Bluberi 120 g",
    "Cimory Yogurt Squeeze Ketan Mangga 120 g",
    "Cimory Minuman Yogurt Stroberi 240 ml",
    "Cimory Minuman Yogurt Mix Fruits 240 ml",
    "Cimory Minuman Yogurt Bluberi 240 ml",
    "Cimory Minuman Yogurt Original 240 ml",
    "Cimory Minuman Yogurt Mixed Berry 240 ml",
    "Cimory Minuman Yogurt Mini Blueberry 4 x 65 ml",
    "Cimory Minuman Yogurt Mini Stroberi 4 x 65 ml",
    "Cimory Yogurt Squeeze Brown Sugar 120 g",
    "Cimory Yogurt Stik Rasa Stroberi 40 g",
    "Cimory Yogurt Stik Rasa Bluberi 40 g",
    "Cimory Yogurt Stik Rasa Original 40 g",
    "Cimory Yogurt Stik Rasa Ketan Mangga 40 g",
    "Cimory Yogurt Stik Rasa Brown Sugar 40 g",
    "Cimory Yogurt Bites Yuzu 120 g",
    "Cimory Yogurt Bites Berry Blend 120 g",
    "Cimory Yogurt Bites Stroberi Leci 120 g",
    "Cimory Yogurt Bites Stroberi Mangga 120 g",
    "Cimory Yogurt Bites Stroberi 120 g",
    "Cimory Yogurt Bites Bluberi 120 g",
    "Cimory Minuman Yogurt Tanpa Gula Tambahan Tropical Fruits 240 ml",
    "Cimory Minuman Yogurt Tanpa Gula Tambahan Blueberry 240 ml",
    "Cimory Minuman Yogurt Tanpa Gula Tambahan Stroberi 240 ml",
    "Cimory Minuman Yogurt Low Fat Stroberi & Mangga 240 ml",
    "Cimory Yogurt Stik Jeruk 40 g",
    "Cimory Yogurt Stik Anggur Kyoho 40 g",
]

# Ambil dari output test_api.py yang lalu
# Saya akan gabungkan respons cimory dan kanzler
api_response_text = """
{
  "cimory_response": {
    "totalData": 53, "totalPage": 1, "pageSize": 53, "currentPage": 0,
    "products": [{"productId": "812188", "productName": "Cimory Susu UHT Matcha 250 ml", "stock": 11}, {"productId": "725439", "productName": "Cimory Susu UHT Cokelat 250 ml", "stock": 21}, {"productId": "769006", "productName": "Cimory Susu UHT Stroberi 250 ml", "stock": 2}, {"productId": "745134", "productName": "Cimory Yogurt Squeeze Stroberi 120 g", "stock": 7}, {"productId": "24088", "productName": "Cimory Minuman Yogurt Stroberi 240 ml", "stock": 7}, {"productId": "688080", "productName": "Cimory Minuman Yogurt Original 240 ml", "stock": 7}, {"productId": "745133", "productName": "Cimory Yogurt Squeeze Original 120 g", "stock": 9}, {"productId": "759791", "productName": "Cimory Yogurt Squeeze Bluberi 120 g", "stock": 9}, {"productId": "24090", "productName": "Cimory Minuman Yogurt Bluberi 240 ml", "stock": 9}, {"productId": "816619", "productName": "Cimory Yogurt Bites Bluberi 120 g", "stock": 9}, {"productId": "816618", "productName": "Cimory Yogurt Bites Stroberi 120 g", "stock": 8}, {"productId": "816620", "productName": "Cimory Yogurt Bites Yuzu 120 g", "stock": 9}, {"productId": "832136", "productName": "Cimory Yogurt Stik Jeruk 40 g", "stock": 19}, {"productId": "800634", "productName": "Cimory Yogurt Stik Rasa Bluberi 40 g", "stock": 50}, {"productId": "813021", "productName": "Cimory Yogurt Stik Rasa Original 40 g", "stock": 46}, {"productId": "767661", "productName": "Cimory Susu UHT Biskuit Marie 250 ml", "stock": 14}, {"productId": "829774", "productName": "Cimory Susu UHT Milk Tea 250 ml", "stock": 6}, {"productId": "774189", "productName": "Cimory Yogurt Squeeze Ketan Mangga 120 g", "stock": 12}, {"productId": "780667", "productName": "Cimory Susu UHT Cokelat Tiramisu 250 ml", "stock": 4}, {"productId": "832137", "productName": "Cimory Yogurt Stik Anggur Kyoho 40 g", "stock": 18}, {"productId": "749825", "productName": "Cimory Susu UHT Cokelat Kotak 125 ml", "stock": 6}, {"productId": "800635", "productName": "Cimory Yogurt Stik Rasa Stroberi 40 g", "stock": 56}, {"productId": "829775", "productName": "Cimory Susu UHT Thai Tea 250 ml", "stock": 9}, {"productId": "688079", "productName": "Cimory Minuman Yogurt Mixed Berry 240 ml", "stock": 8}, {"productId": "826962", "productName": "Cimory Yogurt Bites Stroberi Mangga 120 g", "stock": 8}, {"productId": "816621", "productName": "Cimory Yogurt Bites Stroberi Leci 120 g", "stock": 7}, {"productId": "826963", "productName": "Cimory Yogurt Bites Berry Blend 120 g", "stock": 10}, {"productId": "827938", "productName": "Cimory Susu UHT Cokelat Kotak 750 ml", "stock": 3}, {"productId": "774896", "productName": "Cimory Yogurt Squeeze Brown Sugar 120 g", "stock": 8}, {"productId": "24089", "productName": "Cimory Minuman Yogurt Mix Fruits 240 ml", "stock": 6}, {"productId": "821214", "productName": "Cimory Yogurt Stik Rasa Brown Sugar 40 g", "stock": 35}, {"productId": "725440", "productName": "Cimory Susu UHT Bebas Laktosa Kotak 250 ml", "stock": 5}, {"productId": "736758", "productName": "Cimory Susu UHT Malt Cokelat Kotak 250 ml", "stock": 6}, {"productId": "799475", "productName": "Cimory Susu UHT Choco Mint Kotak 250 ml", "stock": 1}, {"productId": "736757", "productName": "Cimory Susu UHT Cokelat Hazelnut Kotak 250 ml", "stock": 7}, {"productId": "755861", "productName": "Cimory Susu UHT Cokelat Almond Kotak 250 ml", "stock": 11}, {"productId": "755859", "productName": "Cimory Susu UHT Cokelat Cashew Kotak 250 ml", "stock": 11}, {"productId": "813020", "productName": "Cimory Yogurt Stik Rasa Ketan Mangga 40 g", "stock": 19}, {"productId": "688077", "productName": "Cimory Minuman Yogurt Mini Stroberi 4 x 65 ml", "stock": 4}, {"productId": "688078", "productName": "Cimory Minuman Yogurt Mini Blueberry 4 x 65 ml", "stock": 9}, {"productId": "827913", "productName": "Cimory Eat Milk Puding Susu Rasa Cokelat 80 g", "stock": 1}, {"productId": "731347", "productName": "Cimory Minuman Yogurt Tanpa Gula Tambahan Stroberi 240 ml", "stock": 7}, {"productId": "731346", "productName": "Cimory Minuman Yogurt Low Fat Stroberi & Mangga 240 ml", "stock": 7}, {"productId": "831221", "productName": "Cimory Minuman Yogurt Tanpa Gula Tambahan Blueberry 240 ml", "stock": 7}, {"productId": "827912", "productName": "Cimory Eat Milk Puding Susu Rasa Cokelat Hazelnut 80 g", "stock": 11}, {"productId": "708650", "productName": "Cimory Minuman Yogurt Tanpa Gula Tambahan Tropical Fruits 240 ml", "stock": 5}, {"productId": "827914", "productName": "Cimory Eat Milk Puding Susu Rasa Marie Biskuit 80 g", "stock": 7}, {"productId": "771442", "productName": "Cimory Minuman Yogurt Mangga 240 ml", "stock": 0}, {"productId": "756985", "productName": "Cimory Yogurt Squeeze Madu 120 g", "stock": 0}, {"productId": "769005", "productName": "Cimory Susu UHT Bluberi 250 ml", "stock": 0}, {"productId": "774897", "productName": "Cimory Yogurt Squeeze Taro Ungu 120 g", "stock": 0}, {"productId": "833729", "productName": "Cimory Eat Milk Puding Susu Rasa Matcha 80 g", "stock": 0}, {"productId": "794271", "productName": "Cimory Susu UHT Cokelat Almond Kotak 750 ml", "stock": 0}]
  },
  "kanzler_response": {
    "totalData": 14, "totalPage": 1, "pageSize": 14, "currentPage": 0,
    "products": [{"productId": "770817", "productName": "Kanzler Bakso Keju 48 g", "stock": 16}, {"productId": "788873", "productName": "Kanzler Bakso Pedas 48 g", "stock": 26}, {"productId": "770816", "productName": "Kanzler Bakso Original 48 g", "stock": 14}, {"productId": "824864", "productName": "Kanzler Singles Bakso Gochujang 55 g", "stock": 25}, {"productId": "753887", "productName": "Kanzler Singles Sosis Sapi & Ayam Mini 65 g", "stock": 30}, {"productId": "786417", "productName": "Kanzler Singles Sosis Sapi & Ayam Gochujang 60 g", "stock": 35}, {"productId": "753886", "productName": "Kanzler Singles Sosis Sapi & Ayam Keju 65 g", "stock": 28}, {"productId": "753885", "productName": "Kanzler Singles Sosis Sapi & Ayam Original 65 g", "stock": 33}, {"productId": "755865", "productName": "Kanzler Singles Sosis Sapi & Ayam Pedas 65 g", "stock": 30}, {"productId": "776861", "productName": "Kanzler Naget Ayam Krispi 450 g", "stock": 0}, {"productId": "776863", "productName": "Kanzler Sosis Sapi Coktail 250 g", "stock": 0}, {"productId": "776860", "productName": "Kanzler Naget Ayam Original 450 g", "stock": 0}, {"productId": "803277", "productName": "Kanzler Stik Naget Ayam Krispi 450 g", "stock": 0}, {"productId": "817502", "productName": "Kanzler Naget Ayam Krispi Pedas 450 g", "stock": 0}]
  }
}
"""

data = json.loads(api_response_text)
api_product_names = set()
for product in data["cimory_response"]["products"]:
    api_product_names.add(product["productName"])
for product in data["kanzler_response"]["products"]:
    api_product_names.add(product["productName"])

user_product_set = set(user_product_list)

# Bandingkan
print("--- Perbandingan Nama Produk ---")

# Produk di daftar lu yang TIDAK ADA di API
not_in_api = user_product_set - api_product_names
if not_in_api:
    print("\n[PERHATIAN] Produk berikut ada di daftar lu, tapi TIDAK DITEMUKAN di API:")
    for name in sorted(list(not_in_api)):
        print(f"- {name}")
else:
    print("\n[INFO] Semua produk di daftar lu ada di dalam respons API.")


# Produk di API yang TIDAK ADA di daftar lu
not_in_user_list = api_product_names - user_product_set
if not_in_user_list:
    print("\n[INFO] Produk berikut ada di API, tapi TIDAK ADA di daftar lu (mungkin mau ditambah?):")
    for name in sorted(list(not_in_user_list)):
        print(f"- {name}")
else:
    print("\n[INFO] Semua produk dari API sudah ada di daftar lu.")

if not not_in_api:
    print("\n[KESIMPULAN] Kelihatannya semua nama produk di daftar lu sudah cocok dengan nama dari API. Seharusnya filter sudah berjalan benar.")
else:
    print("\n[KESIMPULAN] Ada nama produk yang tidak cocok. Coba perbaiki nama produk di Google Sheet lu sesuai daftar 'TIDAK DITEMUKAN' di atas.")

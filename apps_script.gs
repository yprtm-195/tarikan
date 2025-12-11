function doGet(e) {
  // Pastikan ID spreadsheet ini sesuai dengan punya lu
  const SPREADSHEET_ID = "10HlR0rRseB1TasNfKmMqkqq7A51D50Pci6eFVF63F74";
  
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    
    // Nama-nama sheet-nya
    const storeSheet = ss.getSheetByName("Daftar Toko");
    const tokenSheet = ss.getSheetByName("Daftar Token");
    const productSheet = ss.getSheetByName("Daftar Produk");

    // Ambil semua data dari masing-masing sheet
    const storeDataValues = storeSheet.getDataRange().getValues();
    const tokenDataValues = tokenSheet.getDataRange().getValues();
    const productDataValues = productSheet.getDataRange().getValues();
    
    // --- Proses Data Toko (jadi list of objects) ---
    let stores = [];
    if (storeDataValues.length > 1) { // Check if there's more than just a header
      const storeHeaders = storeDataValues.shift(); // Ambil header & hapus dari data
      stores = storeDataValues.map(row => {
        let storeObj = {};
        storeHeaders.forEach((header, i) => {
          storeObj[header] = row[i];
        });
        return storeObj;
      });
    }

    // --- Proses Data Token & Produk (jadi list biasa) ---
    const tokens = tokenDataValues.flat().filter(String); // .flat() untuk meratakan & .filter(String) untuk hapus sel kosong
    const products = productDataValues.flat().filter(String);
    
    const output = {
      stores: stores,
      tokens: tokens,
      products: products
    };
    
    return ContentService.createTextOutput(JSON.stringify(output))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    const errorOutput = {
      status: "error",
      message: err.message,
      stack: err.stack
    };
    return ContentService.createTextOutput(JSON.stringify(errorOutput))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  const SPREADSHEET_ID = "10HlR0rRseB1TasNfKmMqkqq7A51D50Pci6eFVF63F74";
  const SHEET_NAME_OUTPUT = "Hasil Stok"; // Nama sheet output
  
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    let outputSheet = ss.getSheetByName(SHEET_NAME_OUTPUT);

    if (!outputSheet) {
      // Jika sheet tidak ada, buat sheet baru
      outputSheet = ss.insertSheet(SHEET_NAME_OUTPUT);
    }

    // Ambil data dari payload JSON
    const payload = JSON.parse(e.postData.contents);
    const dataToWrite = payload.data;

    if (!Array.isArray(dataToWrite) || dataToWrite.length === 0) {
      throw new Error("Data yang diterima dari Python bukan array atau kosong.");
    }
    
    // Hapus semua konten lama dari sheet
    outputSheet.clear(); 
    
    // Tulis semua data baru sekaligus untuk performa terbaik
    outputSheet.getRange(1, 1, dataToWrite.length, dataToWrite[0].length).setValues(dataToWrite);

    return ContentService.createTextOutput(JSON.stringify({status: "success", message: `${dataToWrite.length - 1} baris data berhasil ditulis.`}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    const errorOutput = {
      status: "error",
      message: err.message,
      stack: err.stack
    };
    return ContentService.createTextOutput(JSON.stringify(errorOutput))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Fungsi ini akan otomatis jalan setiap kali spreadsheet dibuka
 * dan membuat menu custom 'Admin'.
 */
function onOpen(e) {
  SpreadsheetApp.getUi()
      .createMenu('Admin')
      .addItem('1. Authorize Script', 'authorizeScript')
      .addItem('2. Run Archive Manually', 'archiveSheet')
      .addToUi();
}

/**
 * Fungsi ini hanya untuk memicu proses otorisasi.
 * Dengan memanggil service DriveApp dan SpreadsheetApp,
 * Google akan otomatis meminta izin yang dibutuhkan.
 */
function authorizeScript() {
  try {
    DriveApp.getFolders();
    SpreadsheetApp.getActiveSpreadsheet();
    SpreadsheetApp.getUi().alert('Otorisasi Berhasil', 'Skrip sekarang punya izin yang dibutuhkan.', SpreadsheetApp.getUi().ButtonSet.OK);
  } catch (e) {
    SpreadsheetApp.getUi().alert('Otorisasi Gagal', e.toString(), SpreadsheetApp.getUi().ButtonSet.OK);
  }
}

// ================================================================
// KODE LAMA DI BAWAH INI (JANGAN DIUBAH)
// ================================================================

function doGet(e) {
  const SPREADSHEET_ID = "10HlR0rRseB1TasNfKmMqkqq7A51D50Pci6eFVF63F74";
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const storeSheet = ss.getSheetByName("Daftar Toko");
    const tokenSheet = ss.getSheetByName("Daftar Token");
    const productSheet = ss.getSheetByName("Daftar Produk");
    const storeDataValues = storeSheet.getDataRange().getValues();
    const rawTokenData = tokenSheet.getDataRange().getValues();
    const rawProductData = productSheet.getDataRange().getValues();
    let stores = [];
    if (storeDataValues.length > 1) {
      const storeHeaders = storeDataValues.shift();
      stores = storeDataValues.map(row => {
        let storeObj = {};
        storeHeaders.forEach((header, i) => { storeObj[header] = row[i]; });
        return storeObj;
      });
    }
    let tokens = [];
    if (rawTokenData.length > 1) {
      rawTokenData.shift();
      tokens = rawTokenData.map(row => String(row[1])).filter(String);
    }
    let products = [];
    if (rawProductData.length > 1) {
      rawProductData.shift();
      products = rawProductData.map(row => String(row[1])).filter(String);
    }
    const output = { stores: stores, tokens: tokens, products: products };
    return ContentService.createTextOutput(JSON.stringify(output))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    const errorOutput = { status: "error", message: err.message, stack: err.stack };
    return ContentService.createTextOutput(JSON.stringify(errorOutput))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  const SPREADSHEET_ID = "10HlR0rRseB1TasNfKmMqkqq7A51D50Pci6eFVF63F74";
  const SHEET_NAME_HISTORICAL = "Riwayat Stok";
  const SHEET_NAME_PIVOT = "Stok Terkini";

  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const payload = JSON.parse(e.postData.contents);
    const outputType = payload.type;
    const data = payload.data;

    if (!outputType || !data || !Array.isArray(data) || data.length === 0) {
      throw new Error("Payload tidak valid.");
    }

    if (outputType === 'pivot') {
      let pivotSheet = ss.getSheetByName(SHEET_NAME_PIVOT);
      if (!pivotSheet) pivotSheet = ss.insertSheet(SHEET_NAME_PIVOT);
      pivotSheet.clear();
      pivotSheet.getRange(1, 1, data.length, data[0].length).setValues(data);
      return ContentService.createTextOutput(JSON.stringify({status: "success", message: `Sheet '${SHEET_NAME_PIVOT}' berhasil ditimpa.`})).setMimeType(ContentService.MimeType.JSON);
    
    } else if (outputType === 'historical') {
      let historicalSheet = ss.getSheetByName(SHEET_NAME_HISTORICAL);
      if (!historicalSheet) historicalSheet = ss.insertSheet(SHEET_NAME_HISTORICAL);
      const headers = Object.keys(data[0]);
      const values = data.map(obj => headers.map(header => obj[header]));
      const lastRow = historicalSheet.getLastRow();
      if (lastRow === 0) {
        const dataWithHeader = [headers].concat(values);
        historicalSheet.getRange(1, 1, dataWithHeader.length, dataWithHeader[0].length).setValues(dataWithHeader);
        return ContentService.createTextOutput(JSON.stringify({status: "success", message: `Header + ${values.length} baris ditulis ke '${SHEET_NAME_HISTORICAL}'.`})).setMimeType(ContentService.MimeType.JSON);
      } else {
        historicalSheet.getRange(lastRow + 1, 1, values.length, values[0].length).setValues(values);
        return ContentService.createTextOutput(JSON.stringify({status: "success", message: `${values.length} baris ditambahkan ke '${SHEET_NAME_HISTORICAL}'.`})).setMimeType(ContentService.MimeType.JSON);
      }
    } else {
      throw new Error(`Tipe output '${outputType}' tidak dikenali.`);
    }

  } catch (err) {
    const errorOutput = { status: "error", message: err.message, stack: err.stack };
    return ContentService.createTextOutput(JSON.stringify(errorOutput))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function archiveSheet() {
  const SPREADSHEET_ID = "10HlR0rRseB1TasNfKmMqkqq7A51D50Pci6eFVF63F74";
  const SHEET_NAME_SOURCE = "Riwayat Stok";
  const ARCHIVE_FOLDER_NAME = "Arsip Stok Alfagift";
  
  try {
    const sourceSpreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sourceSheet = sourceSpreadsheet.getSheetByName(SHEET_NAME_SOURCE);

    if (!sourceSheet) {
      console.log(`Sheet sumber '${SHEET_NAME_SOURCE}' tidak ditemukan. Proses arsip dibatalkan.`);
      return;
    }
    
    const lastRow = sourceSheet.getLastRow();
    if (lastRow <= 1) {
      console.log(`Tidak ada data untuk diarsip di '${SHEET_NAME_SOURCE}'.`);
      return;
    }
    
    const dataRange = sourceSheet.getDataRange();
    const dataToArchive = dataRange.getValues();
    
    let archiveFolder;
    const folders = DriveApp.getFoldersByName(ARCHIVE_FOLDER_NAME);
    if (folders.hasNext()) {
      archiveFolder = folders.next();
    } else {
      archiveFolder = DriveApp.createFolder(ARCHIVE_FOLDER_NAME);
    }
    
    const now = new Date();
    const formattedDate = Utilities.formatDate(now, Session.getScriptTimeZone(), "yyyy-MM-dd");
    const archiveSpreadsheetName = `Arsip Stok - ${formattedDate}`;
    
    const newSpreadsheet = SpreadsheetApp.create(archiveSpreadsheetName);
    const newSheet = newSpreadsheet.getSheets()[0];
    newSheet.setName(SHEET_NAME_SOURCE);
    
    newSheet.getRange(1, 1, dataToArchive.length, dataToArchive[0].length).setValues(dataToArchive);
    console.log(`Berhasil membuat arsip: '${archiveSpreadsheetName}'.`);
    
    const newFile = DriveApp.getFileById(newSpreadsheet.getId());
    newFile.moveTo(archiveFolder);
    console.log(`File '${archiveSpreadsheetName}' berhasil dipindahkan ke folder '${ARCHIVE_FOLDER_NAME}'.`);
    
    sourceSheet.getRange(2, 1, lastRow - 1, sourceSheet.getLastColumn()).clearContent();
    console.log(`Berhasil mengosongkan data di sheet '${SHEET_NAME_SOURCE}'.`);
    
  } catch(err) {
    console.error(`Proses arsip gagal: ${err.toString()}`);
  }
}

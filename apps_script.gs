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
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const payload = JSON.parse(e.postData.contents);
    const outputType = payload.type;
    const data = payload.data;

    if (!outputType || !data || !Array.isArray(data) || data.length === 0) {
      throw new Error("Payload tidak valid. Harus ada 'type' dan 'data' (array tidak kosong).");
    }

    if (outputType === 'pivot') {
      const SHEET_NAME_PIVOT = "Stok Terkini";
      let pivotSheet = ss.getSheetByName(SHEET_NAME_PIVOT);
      if (!pivotSheet) {
        pivotSheet = ss.insertSheet(SHEET_NAME_PIVOT);
      }
      pivotSheet.clear();
      pivotSheet.getRange(1, 1, data.length, data[0].length).setValues(data);
      return ContentService.createTextOutput(JSON.stringify({status: "success", message: `Sheet '${SHEET_NAME_PIVOT}' berhasil ditimpa dengan ${data.length - 1} baris data pivot.`})).setMimeType(ContentService.MimeType.JSON);
    
    } else if (outputType === 'historical') {
      const SHEET_NAME_HISTORICAL = "Riwayat Stok";
      let historicalSheet = ss.getSheetByName(SHEET_NAME_HISTORICAL);
      if (!historicalSheet) {
        historicalSheet = ss.insertSheet(SHEET_NAME_HISTORICAL);
      }
      const headers = Object.keys(data[0]);
      const values = data.map(obj => headers.map(header => obj[header]));
      const lastRow = historicalSheet.getLastRow();
      if (lastRow === 0) {
        const dataWithHeader = [headers].concat(values);
        historicalSheet.getRange(1, 1, dataWithHeader.length, dataWithHeader[0].length).setValues(dataWithHeader);
        return ContentService.createTextOutput(JSON.stringify({status: "success", message: `Sheet '${SHEET_NAME_HISTORICAL}' kosong. Header + ${values.length} baris data berhasil ditulis.`})).setMimeType(ContentService.MimeType.JSON);
      } else {
        historicalSheet.getRange(lastRow + 1, 1, values.length, values[0].length).setValues(values);
        return ContentService.createTextOutput(JSON.stringify({status: "success", message: `${values.length} baris data berhasil ditambahkan ke '${SHEET_NAME_HISTORICAL}'.`})).setMimeType(ContentService.MimeType.JSON);
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

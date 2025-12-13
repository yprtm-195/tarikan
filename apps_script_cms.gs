function doGet(e) {
  const SPREADSHEET_ID = "10HlR0rRseB1TasNfKmMqkqq7A51D50Pci6eFVF63F74";
  const SHEET_NAME_PIVOT = "Stok Terkini";
  
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const pivotSheet = ss.getSheetByName(SHEET_NAME_PIVOT);
    
    if (!pivotSheet) {
      throw new Error(`Sheet dengan nama '${SHEET_NAME_PIVOT}' tidak ditemukan.`);
    }

    const data = pivotSheet.getDataRange().getValues();
    
    return ContentService.createTextOutput(JSON.stringify({ data: data }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    const errorOutput = {
      status: "error",
      message: err.message
    };
    return ContentService.createTextOutput(JSON.stringify(errorOutput))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

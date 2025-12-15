// Fungsi doGet dan doPost tetap sama seperti sebelumnya...
function doGet(e) { /* ... isi fungsi ... */ }
function doPost(e) { /* ... isi fungsi ... */ }

// --- FUNGSI BARU UNTUK ARSIP ---
function archiveSheet() {
  const SPREADSHEET_ID = "10HlR0rRseB1TasNfKmMqkqq7A51D50Pci6eFVF63F74";
  const SHEET_NAME_SOURCE = "Riwayat Stok";
  const ARCHIVE_FOLDER_NAME = "Arsip Stok Alfagift"; // Nama folder arsip
  
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
    
    // --- Logika Folder ---
    let archiveFolder;
    const folders = DriveApp.getFoldersByName(ARCHIVE_FOLDER_NAME);
    if (folders.hasNext()) {
      archiveFolder = folders.next();
      console.log(`Folder arsip '${ARCHIVE_FOLDER_NAME}' ditemukan.`);
    } else {
      archiveFolder = DriveApp.createFolder(ARCHIVE_FOLDER_NAME);
      console.log(`Folder arsip '${ARCHIVE_FOLDER_NAME}' dibuat.`);
    }
    
    // Buat nama file arsip baru
    const now = new Date();
    const formattedDate = Utilities.formatDate(now, Session.getScriptTimeZone(), "yyyy-MM-dd");
    const archiveSpreadsheetName = `Arsip Stok - ${formattedDate}`;
    
    // Buat spreadsheet baru
    const newSpreadsheet = SpreadsheetApp.create(archiveSpreadsheetName);
    const newSheet = newSpreadsheet.getSheets()[0];
    newSheet.setName(SHEET_NAME_SOURCE);
    
    // Salin data ke spreadsheet arsip
    newSheet.getRange(1, 1, dataToArchive.length, dataToArchive[0].length).setValues(dataToArchive);
    console.log(`Berhasil membuat arsip di spreadsheet baru: '${archiveSpreadsheetName}'.`);
    
    // Pindahkan spreadsheet baru ke folder arsip
    const newFile = DriveApp.getFileById(newSpreadsheet.getId());
    newFile.moveTo(archiveFolder);
    console.log(`File '${archiveSpreadsheetName}' berhasil dipindahkan ke folder '${ARCHIVE_FOLDER_NAME}'.`);
    
    // Kosongkan sheet sumber (sisakan header)
    sourceSheet.getRange(2, 1, lastRow - 1, sourceSheet.getLastColumn()).clearContent();
    console.log(`Berhasil mengosongkan data di sheet '${SHEET_NAME_SOURCE}'.`);
    
  } catch(err) {
    console.error(`Proses arsip gagal: ${err.toString()}`);
  }
}

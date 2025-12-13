document.addEventListener('DOMContentLoaded', function() {
    const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxTNN-7FaYzql3TZza6dvPcQRFfizCsq_JAh3ZYrWL6amYkHUZO_RdomRJBslSBBHFQvg/exec';
    const loadingDiv = document.getElementById('loading');
    const tableContainer = document.getElementById('table-container');
    const tableHead = document.querySelector('#stock-table thead');
    const tableBody = document.querySelector('#stock-table tbody');

    async function fetchData() {
        try {
            const response = await fetch(APPS_SCRIPT_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const jsonResponse = await response.json();
            if (jsonResponse.status === 'error') {
                throw new Error(`Apps Script error: ${jsonResponse.message}`);
            }
            renderTable(jsonResponse.data);
        } catch (error) {
            loadingDiv.textContent = `Gagal memuat data: ${error.message}`;
            console.error("Fetch error:", error);
        }
    }

    function renderTable(data) {
        if (!data || data.length === 0) {
            loadingDiv.textContent = 'Tidak ada data untuk ditampilkan.';
            return;
        }

        // Clear loading message and any previous table content
        loadingDiv.style.display = 'none';
        tableHead.innerHTML = '';
        tableBody.innerHTML = '';

        // First row is the header
        const headerRow = document.createElement('tr');
        const headers = data[0];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        tableHead.appendChild(headerRow);

        // The rest of the rows are data
        const dataRows = data.slice(1);
        dataRows.forEach(rowData => {
            const tr = document.createElement('tr');
            rowData.forEach(cellData => {
                const td = document.createElement('td');
                td.textContent = cellData;
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }

    fetchData();
});

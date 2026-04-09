const API_BASE = "http://localhost:8000";

const entitySelect = document.getElementById('entity-select');
const entityId = document.getElementById('entity-id');
const entityJson = document.getElementById('entity-json');
const crudOutput = document.getElementById('crud-output');

const examplePayloads = {
    products: {
        ProductId: 101,
        ProductName: "Enterprise Laptop Pro",
        Brand: "TechCorp",
        CategoryName: "Electronics",
        Price: 1299.99,
        Description: "High-end laptop designed for enterprise use with robust security features.",
        IsAvailable: true,
        StockQuantity: 50,
        ImageUrl: ["http://example.com/laptop.png"]
    },
    orders: {
        OrderID: 201,
        UserId: 5001,
        OrderDate: "2026-04-08T10:00:00Z",
        Status: "processing",
        TotalAmount: 1299.99,
        Items: [101]
    }
};

document.getElementById('crud-get').addEventListener('click', () => {
    const type = entitySelect.value;
    entityJson.value = JSON.stringify(examplePayloads[type], null, 2);
    crudOutput.textContent = "Loaded example payload for " + type;
});

async function handleCrud(method, url, payload = null) {
    crudOutput.textContent = "Processing...";
    try {
        const options = { method, headers: {} };
        if (payload) {
            options.headers['Content-Type'] = 'application/json';
            options.body = payload;
        }
        
        const response = await fetch(url, options);
        const data = await response.json();
        
        if (!response.ok) {
            crudOutput.textContent = `Error (${response.status}): ${data.message || 'Unknown error'}\nDetail: ${data.detail || 'None'}`;
            crudOutput.classList.add('error-text');
            return;
        }

        crudOutput.classList.remove('error-text');
        crudOutput.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        crudOutput.textContent = "Error: " + err.message;
    }
}

document.getElementById('crud-add').addEventListener('click', () => {
    const type = entitySelect.value;
    handleCrud('POST', `${API_BASE}/vector/${type}`, entityJson.value);
});

document.getElementById('crud-update').addEventListener('click', () => {
    const type = entitySelect.value;
    const id = entityId.value.trim();
    if (!id) {
        crudOutput.textContent = "Please enter an Entity ID to update.";
        return;
    }
    handleCrud('PUT', `${API_BASE}/vector/${type}/${id}`, entityJson.value);
});

document.getElementById('crud-delete').addEventListener('click', () => {
    const type = entitySelect.value;
    const id = entityId.value.trim();
    if (!id) {
        crudOutput.textContent = "Please enter an Entity ID to delete.";
        return;
    }
    handleCrud('DELETE', `${API_BASE}/vector/${type}/${id}`);
});

document.getElementById('search-btn').addEventListener('click', () => {
    const q = document.getElementById('search-input').value.trim();
    if (!q) {
        crudOutput.textContent = "Please enter a search query.";
        return;
    }
    handleCrud('GET', `${API_BASE}/vector/search?q=${encodeURIComponent(q)}`);
});

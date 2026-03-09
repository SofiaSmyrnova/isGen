function generatePatients() {
    const countInput = document.getElementById("count-input");
    const formsContainer = document.getElementById("patients-forms");
    const resultsList = document.getElementById("results-list");

    if (!countInput || !formsContainer || !resultsList) {
        return;
    }

    let count = parseInt(countInput.value, 10);

    if (isNaN(count) || count < 1) {
        count = 1;
    }

    if (count > 20) {
        count = 20;
    }

    countInput.value = count;
    formsContainer.innerHTML = "";

    resultsList.innerHTML = `
        <div class="result-placeholder">
            Results will appear here
        </div>
    `;

    for (let i = 1; i <= count; i++) {
        formsContainer.innerHTML += `
            <div class="patient-form">
                <div class="form-row">
                    <label for="name-${i}">Patient name</label>
                    <input type="text" id="name-${i}" placeholder="Enter patient name">
                </div>

                <div class="form-row">
                    <label for="temp-${i}">Temperature (°C)</label>
                    <input type="text" id="temp-${i}" placeholder="Example: 36.6">
                </div>

                <div class="form-row">
                    <label for="sat-${i}">Saturation (%)</label>
                    <input type="number" id="sat-${i}" placeholder="Example: 98">
                </div>
            </div>
        `;
    }
}

async function diagnosePatients() {
    const countInput = document.getElementById("count-input");
    const resultsList = document.getElementById("results-list");

    if (!countInput || !resultsList) {
        return;
    }

    const count = parseInt(countInput.value, 10) || 1;
    const patients = [];

    for (let i = 1; i <= count; i++) {
        const name = document.getElementById(`name-${i}`)?.value.trim() || "";
        const temperature = document.getElementById(`temp-${i}`)?.value.trim() || "";
        const saturation = document.getElementById(`sat-${i}`)?.value.trim() || "";

        patients.push({
            name: name,
            temperature: temperature,
            saturation: saturation
        });
    }

    resultsList.innerHTML = `
        <div class="result-placeholder">
            Processing...
        </div>
    `;

    try {
        const response = await fetch("/api/flue-detector", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ patients: patients })
        });

        const data = await response.json();
        resultsList.innerHTML = "";

        if (!data.results || !Array.isArray(data.results) || data.results.length === 0) {
            resultsList.innerHTML = `
                <div class="result-card status-error">
                    No results received
                </div>
            `;
            return;
        }

        data.results.forEach((result) => {
            const safeStatus = result.status || "error";

            resultsList.innerHTML += `
                <div class="result-card status-${safeStatus}">
                    ${result.message}
                </div>
            `;
        });
    } catch (error) {
        resultsList.innerHTML = `
            <div class="result-card status-error">
                Server connection error
            </div>
        `;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    generatePatients();
});

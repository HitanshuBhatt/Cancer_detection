// Configuration: Update this to your FastAPI backend URL
const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', () => {
    fetchPatients();

    // Set up search functionality if you add a search input with id="patientSearch"
    const searchInput = document.getElementById('patientSearch');
    if (searchInput) {
        searchInput.addEventListener('input', filterPatients);
    }
});

/**
 * Fetch all patients from the MySQL database via FastAPI
 */
async function fetchPatients() {
    try {
        const response = await fetch(`${API_BASE_URL}/patients`);
        if (!response.ok) throw new Error("Failed to fetch patients");
        
        const patients = await response.json();
        renderPatientTable(patients);
    } catch (error) {
        console.error("Error loading patients:", error);
        // Fallback: keep existing static HTML if server is down
    }
}

/**
 * Dynamically build the table rows
 * Matches the structure in your patients.html: 
 * Name, Age (calculated from DOB), Condition (Cancer Type), Status
 */
function renderPatientTable(patients) {
    const tableBody = document.querySelector('.data-table tbody');
    tableBody.innerHTML = ''; // Clear existing static rows

    patients.forEach(patient => {
        const row = document.createElement('tr');
        
        // Calculate age from Date of Birth
        const age = calculateAge(patient.dob);

        row.innerHTML = `
            <td>${patient.first_name} ${patient.last_name}</td>
            <td>${age}</td>
            <td>${patient.cancer_type || 'N/A'}</td>
            <td><span class="status-tag ${patient.status?.toLowerCase() || 'stable'}">${patient.status || 'Stable'}</span></td>
        `;

        // Make the row clickable to view details (optional)
        row.style.cursor = "pointer";
        row.onclick = () => window.location.href = `patient-details.html?id=${patient.patient_id}`;

        tableBody.appendChild(row);
    });
}

/**
 * Utility: Calculate age based on YYYY-MM-DD string
 */
function calculateAge(dobString) {
    if (!dobString) return "N/A";
    const birthday = new Date(dobString);
    const ageDifMs = Date.now() - birthday.getTime();
    const ageDate = new Date(ageDifMs); 
    return Math.abs(ageDate.getUTCFullYear() - 1970);
}

/**
 * Client-side search filtering
 */
function filterPatients() {
    const searchTerm = document.getElementById('patientSearch').value.toLowerCase();
    const rows = document.querySelectorAll('.data-table tbody tr');

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

async function registerPatient(event) {
    event.preventDefault();

    const API_BASE_URL = "http://127.0.0.1:8000";

    try {
        // All these IDs now match your HTML exactly
        const patientData = {
            first_name: document.getElementById('firstName').value,
            last_name: document.getElementById('lastName').value,
            dob: document.getElementById('dob').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value,
            medical_conditions: document.getElementById('other_conditions').value,
            gender: document.getElementById('gender').value
        };

        const response = await fetch(`${API_BASE_URL}/register-patient`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(patientData)
        });

        const result = await response.json();

        if (response.ok) {
            alert("✅ Patient successfully registered!");
            event.target.reset(); // Clears the form
            if (typeof fetchPatients === "function") fetchPatients(); // Refresh table if function exists
        } else {
            alert("❌ Registration failed: " + (result.detail || "Unknown error"));
        }
    } catch (error) {
        console.error("Critical Error:", error);
        alert("❌ Could not connect to the server. Check if main.py is running.");
    }
}
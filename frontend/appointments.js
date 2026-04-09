const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', () => {
    // Load dropdown and list on page start
    loadPatientDropdown();
    fetchAppointments();
});

/**
 * 1. LOAD DROPDOWN: Fetches patients so we have real IDs to link to
 */
async function loadPatientDropdown() {
    const patientSelect = document.getElementById('patientSelect');
    if (!patientSelect) return;

    try {
        const response = await fetch(`${API_BASE_URL}/patients`);
        const patients = await response.json();

        // Clear existing options except the placeholder
        patientSelect.innerHTML = '<option value="">-- Select a Patient --</option>';

        patients.forEach(p => {
            const option = document.createElement('option');
            option.value = p.patient_id; 
            option.textContent = `${p.first_name} ${p.last_name}`; 
            patientSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Failed to load patients for dropdown:", error);
    }
}

/**
 * 2. CREATE: Sends numeric IDs to the /add-appointment endpoint
 */
async function addAppointment(event) {
    event.preventDefault();

    const formData = new FormData();
    // We get the values from the NEW IDs we added to the HTML
    formData.append("patient_id", document.getElementById('patientSelect').value);
    formData.append("doctor_id", document.getElementById('doctorId').value);
    formData.append("appt_date", document.getElementById('appointmentDate').value);
    formData.append("appt_time", document.getElementById('appointmentTime').value);
    formData.append("reason", document.getElementById('appointmentReason').value);

    try {
        const response = await fetch(`${API_BASE_URL}/add-appointment`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert("✅ Appointment successfully saved to the Database!");
            location.reload(); 
        } else {
            const errorData = await response.json();
            alert("❌ Server Error: " + errorData.error);
        }
    } catch (error) {
        console.error("Connection Error:", error);
        alert("❌ Could not connect to the server.");
    }
}

/**
 * 3. READ: Fetches from the appointments table and displays cards
 */
/**
 * 3. READ: Fetches from the appointments table with Patient Names
 */
async function fetchAppointments() {
    const listContainer = document.getElementById('appointmentsList');
    if (!listContainer) return;

    try {
        const response = await fetch(`${API_BASE_URL}/get-appointments`);
        const appointments = await response.json();

        if (appointments.length === 0) {
            listContainer.innerHTML = "<p style='color: #64748b;'>No appointments found.</p>";
            return;
        }

        listContainer.innerHTML = '';
        appointments.forEach(appt => {
            const card = document.createElement('div');
            card.className = 'appointment-card';
            
            // We use the first_name and last_name returned by your new JOIN query
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                    <div>
                        <strong style="color: #2563eb; font-size: 1.1rem;">
                            Patient: ${appt.first_name} ${appt.last_name}
                        </strong>
                        <p style="margin: 5px 0; font-weight: 500;">Reason: ${appt.reason}</p>
                        <small style="color: #64748b;">📅 Scheduled: ${new Date(appt.appointment_time).toLocaleString()}</small>
                    </div>
                    <span class="status-tag stable">${appt.status || 'Confirmed'}</span>
                </div>
            `;
            listContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Error fetching data:", error);
        listContainer.innerHTML = "<p style='color: #ef4444;'>Error loading data from database.</p>";
    }
}
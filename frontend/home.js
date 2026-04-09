async function loadDashboard() {
    try {
        const response = await fetch('http://127.0.0.1:8000/get-appointments');
        const appointments = await response.json();
        
        // 1. Get Today's Date in YYYY-MM-DD format (e.g., "2026-04-09")
        const todayStr = new Date().toISOString().split('T')[0];

        // 2. Filter using the first 10 characters of your DB timestamp
        const todaysAppts = appointments.filter(appt => {
            // This extracts "2026-04-09" from "2026-04-09 20:44:00"
            const dbDateOnly = appt.appointment_time.substring(0, 10);
            return dbDateOnly === todayStr;
        });
        
        // 3. Update the UI Counters using your HTML IDs
        const todayCount = document.getElementById('todayAppointments');
        const totalCount = document.getElementById('totalAppointments');

        if (todayCount) todayCount.textContent = todaysAppts.length; // Shows 2
        if (totalCount) totalCount.textContent = appointments.length; // Shows 3

        window.todaysApptsData = todaysAppts;

    } catch (error) {
        console.error("Database sync error:", error);
    }
}

function toggleAppointments() {
    const panel = document.getElementById('expanded-appointments');
    // Ensure display property is handled correctly for the first click
    if (panel.style.display === 'none' || panel.style.display === '') {
        panel.style.display = 'block';
        displayTodayTable(); 
    } else {
        panel.style.display = 'none';
    }
}
function displayTodayTable() {
    const listBody = document.getElementById('appointment-list');
    if (!listBody || !window.todaysApptsData) return;

    listBody.innerHTML = ''; 

    window.todaysApptsData.forEach(app => {
        // 1. Time extraction from "YYYY-MM-DD HH:MM:SS"
        const timeVal = app.appointment_time ? app.appointment_time.substring(11, 16) : "Unavailable";
        
        // 2. Combine first_name and last_name from your API
        const firstName = app.first_name || "";
        const lastName = app.last_name || "";
        const fullName = (firstName || lastName) ? `${firstName} ${lastName}`.trim() : "Unavailable";
        
        // 3. Email is not in your current get-appointments query
        const contactVal = app.email || "No Email Provided";
        const reasonVal = app.reason || "Unavailable";

        const row = `
            <tr>
                <td><strong>${timeVal}</strong></td>
                <td>${fullName}</td>
                <td>${contactVal}</td>
                <td>${reasonVal}</td>
                <td>
                    <button class="btn small-btn" onclick="reschedule(${app.appointment_id})">Reschedule</button>
                    <button class="btn small-btn danger-btn" onclick="cancel(${app.appointment_id})">Cancel</button>
                </td>
            </tr>`;
        listBody.insertAdjacentHTML('beforeend', row);
    });
}

// Display the doctor's name
const doctorName = localStorage.getItem('doctorName');
if (doctorName && document.querySelector('.logo')) {
    document.querySelector('.logo').innerText = `MediCare | Dr. ${doctorName}`;
}
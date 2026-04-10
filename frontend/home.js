async function loadDashboard() {
    try {
        const response = await fetch('http://127.0.0.1:8000/get-appointments');
        const appointments = await response.json();

        // FIX: Use local time instead of ISO (UTC) to avoid timezone skips
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const todayStr = `${year}-${month}-${day}`;

        // Filter data
        const todayAppts = appointments.filter(a => a.appointment_time.startsWith(todayStr));
        const upcomingAppts = appointments.filter(a => new Date(a.appointment_time) > now);

        // CRITICAL: Save this so toggleAppointments() can see it
        window.todaysApptsData = todayAppts;

        // Update Stat Cards
        document.getElementById('todayAppointments').innerText = todayAppts.length;
        document.getElementById('totalAppointments').innerText = appointments.length;
        document.getElementById('futureAppointments').innerText = upcomingAppts.length;

        console.log("System Date (Local):", todayStr);
        console.log("Appointments Found for Today:", todayAppts.length);

    } catch (error) {
        console.error("❌ Dashboard Load Error:", error);
    }
}
// Function to show/hide the table when clicking the "Today's Appointments" card
function toggleAppointments() {
    const panel = document.getElementById('expanded-appointments');
    panel.style.display = (panel.style.display === 'none') ? 'block' : 'none';
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
function loadDashboard() {
    // 1. Get appointments from localStorage (or your database later)
    const appointments = JSON.parse(localStorage.getItem('appointments')) || [];
    
    // 2. Get Today's Date in YYYY-MM-DD format
    const today = new Date().toISOString().split('T')[0];

    // 3. Filter for Today's Appointments
    const todaysAppts = appointments.filter(appt => appt.date === today);
    
    // 4. Update the Dashboard UI
    const todayCountElement = document.getElementById('todayAppointments');
    const totalCountElement = document.getElementById('totalAppointments');
    const futureCountElement = document.getElementById('futureAppointments');

    if (todayCountElement) {
        todayCountElement.textContent = todaysAppts.length;
    }

    if (totalCountElement) {
        totalCountElement.textContent = appointments.length;
    }

    if (futureCountElement) {
        const futureAppts = appointments.filter(appt => appt.date > today);
        futureCountElement.textContent = futureAppts.length;
    }
}

// Display the doctor's name from the login session
const doctorName = localStorage.getItem('doctorName');
if (doctorName) {
    document.querySelector('.logo').innerText = `MediCare | Dr. ${doctorName}`;
}
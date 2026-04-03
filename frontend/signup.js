// Registration Logic
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const userData = {
        name: document.getElementById('regName').value,
        reason: document.getElementById('regReason').value,
        dob: document.getElementById('regDob').value,
        contact: document.getElementById('regContact').value,
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value
    };

    // Sending data to your backend server (Example URL)
    const response = await fetch('https://your-api-url.com/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });

    if (response.ok) {
        alert("Registration Successful! You can now log in.");
        window.location.href = "index.html";
    }
});
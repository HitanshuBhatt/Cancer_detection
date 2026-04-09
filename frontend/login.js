document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message'); // Optional: an element to show errors

    try {
        // Send request to your FastAPI backend
        const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // 1. Success! Store the doctor's name for the dashboard
            localStorage.setItem('doctorName', data.name);
            
            // 2. Redirect to dashboard as defined in your backend logic
            console.log("Login successful! Redirecting...");
            window.location.href = "home.html"; 
        } else {
            // 3. Handle unauthorized access (Incorrect email/password or wrong role)
            alert(data.detail || "Invalid email or password. Please try again.");
        }
    } catch (error) {
        console.error("Connection Error:", error);
        alert("Could not connect to the server. Is your FastAPI running?");
    }
});
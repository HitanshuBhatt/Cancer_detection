document.getElementById('signupForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Get values from the form
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const dob = document.getElementById('dob').value;
    const address = document.getElementById('address').value;
    const password = document.getElementById('password').value;

    const userData = {
        full_name: fullName,
        email: email,
        password: password,
        dob: dob,
        address: address
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registration successful! Redirecting to login...");
            window.location.href = "login.html";
        } else {
            // Show error (e.g., if email already exists)
            alert("Error: " + (data.detail || "Registration failed"));
        }
    } catch (error) {
        console.error("Connection Error:", error);
        alert("Could not connect to the server. Please ensure your backend is running.");
    }
});
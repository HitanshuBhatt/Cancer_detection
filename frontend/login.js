document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Simulate a successful login check
    if (email === "admin@example.com" && password === "password123") {
        console.log("Login successful! Redirecting...");
        window.location.href = "home.html"; 
    } else {
        alert("Invalid email or password. Please try again.");
    }
});
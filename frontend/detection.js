// 1. Get references to the HTML elements
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const resultDiv = document.getElementById("result");
const loadingDiv = document.getElementById("loading");

// 2. Handle the Image Selection & Preview logic
fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];

    if (file) {
        // Create a temporary URL for the selected image
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block"; // Show the preview
        
        // Clear and hide previous results while a new file is being selected
        resultDiv.style.display = "none";
        resultDiv.innerHTML = "";
    }
});

// 3. Main function to upload the image and get AI predictions
async function uploadImage() {
    const file = fileInput.files[0];

    // Basic validation
    if (!file) {
        alert("Please select a medical scan (CT/X-ray) before running the diagnostic.");
        return;
    }

    // UI Feedback: Show loading and hide old results
    loadingDiv.style.display = "block";
    resultDiv.style.display = "none";

    // Prepare the data for the API (Multipart form data)
    const formData = new FormData();
    formData.append("file", file);

    try {
        // Connect to your FastAPI backend
        const response = await fetch("http://127.0.0.1:8000/predict-lung-cancer", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("AI Prediction Received:", data);

        // Hide loading and show the result container
        loadingDiv.style.display = "none";
        resultDiv.style.display = "block";

        // Inject the result with themed styling
        resultDiv.innerHTML = `
            <div style="border-bottom: 1px solid #dbe7f3; margin-bottom: 15px; padding-bottom: 5px;">
                <h3 style="color: #64748b; font-size: 0.9rem; text-transform: uppercase;">Diagnostic Analysis</h3>
            </div>
            <h3 class="prediction-text" style="color: #2563eb; font-size: 1.6rem; margin: 10px 0;">
                ${data.prediction}
            </h3>
            <p style="color: #1e293b; font-size: 1.1rem;">
                AI Confidence: <span style="font-weight: 700; color: #0f4c81;">${Number(data.confidence).toFixed(2)}%</span>
            </p>
            <p style="margin-top: 20px; font-size: 0.8rem; color: #94a3b8; font-style: italic;">
                Model: EfficientNet-B0 Medical Image Classifier
            </p>
        `;

    } catch (error) {
        console.error("Diagnostic Error:", error);
        
        loadingDiv.style.display = "none";
        resultDiv.style.display = "block";
        
        // Show a styled error message if the backend isn't running
        resultDiv.innerHTML = `
            <div style="color: #d62828; padding: 10px; border: 1px solid #fecaca; background: #fef2f2; border-radius: 8px;">
                <strong>⚠️ Connection Failed:</strong><br>
                Could not connect to the AI server. Please ensure your Python backend is running on port 8000.
            </div>
        `;
    }
}

async function loadDashboardData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/get-today-appointments');
        const todayAppointments = await response.json();

        // 1. Update the 'Today's Appointments' counter
        document.getElementById('todayCount').innerText = todayAppointments.length;

        // 2. Populate the 'Scheduled for Today' table
        const tableBody = document.querySelector('#todayTable tbody');
        tableBody.innerHTML = ''; // Clear old data

        if (todayAppointments.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5">No appointments for today.</td></tr>';
        } else {
            todayAppointments.forEach(appt => {
                const row = `
                    <tr>
                        <td>${appt.time}</td>
                        <td>${appt.first_name} ${appt.last_name}</td>
                        <td>${appt.contact || 'N/A'}</td>
                        <td>${appt.reason}</td>
                        <td><span class="status-${appt.status.toLowerCase()}">${appt.status}</span></td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', row);
            });
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}
function loginDoctor(event) {
  event.preventDefault();
  window.location.href = "dashboard.html";
  return false;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric"
  });
}

function renderAppointmentGraph(appointments) {
  const today = new Date().toISOString().split("T")[0];

  let past = [];
  let present = [];
  let future = [];

  appointments.forEach((appt) => {
    const formattedDate = formatDate(appt.date);

    if (appt.date < today) {
      past.push(formattedDate);
    } else if (appt.date === today) {
      present.push(formattedDate);
    } else {
      future.push(formattedDate);
    }
  });

  const max = Math.max(past.length, present.length, future.length, 1);

  const pastBar = document.getElementById("pastBar");
  const presentBar = document.getElementById("presentBar");
  const futureBar = document.getElementById("futureBar");

  const pastCount = document.getElementById("pastCount");
  const presentCount = document.getElementById("presentCount");
  const futureCount = document.getElementById("futureCount");

  if (pastBar) {
    pastBar.style.width = `${(past.length / max) * 100}%`;
    pastBar.textContent = past.join(", ") || "None";
  }

  if (presentBar) {
    presentBar.style.width = `${(present.length / max) * 100}%`;
    presentBar.textContent = present.join(", ") || "None";
  }

  if (futureBar) {
    futureBar.style.width = `${(future.length / max) * 100}%`;
    futureBar.textContent = future.join(", ") || "None";
  }

  if (pastCount) pastCount.textContent = past.length;
  if (presentCount) presentCount.textContent = present.length;
  if (futureCount) futureCount.textContent = future.length;
}
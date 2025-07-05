// Open the modal when the user clicks the "Apply" button
function openModal(jobId) {
    // Placeholder for fetching job details dynamically
    document.getElementById("jobDetails").innerHTML = "<p>Job details for job ID: " + jobId + "...</p>"; // You can replace this with real data fetching

    // Show the modal
    document.getElementById("jobModal").style.display = "block";
}

// Close the modal
function closeModal() {
    document.getElementById("jobModal").style.display = "none";
}

// Close the modal if clicked outside the modal content
window.onclick = function(event) {
    if (event.target == document.getElementById("jobModal")) {
        closeModal();
    }
}
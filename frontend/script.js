const jobsDiv = document.getElementById("jobs");
const spinner = document.getElementById("spinner");
const searchInput = document.getElementById("job-search");

// Hamburger menu toggle
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav-links");
hamburger.addEventListener("click", ()=> navLinks.classList.toggle("active"));

// Fetch jobs from backend
let jobsData = [];
fetch("http://localhost:8000/jobs")
  .then(res => res.json())
  .then(data => {
    jobsData = data;
    spinner.style.display = "none";
    renderJobs(jobsData);
  })
  .catch(err => console.error(err));

// Render jobs dynamically
function renderJobs(jobs) {
    jobsDiv.innerHTML = "";
    if(jobs.length === 0) {
        jobsDiv.innerHTML = "<p>No jobs available right now. Check back later!</p>";
        return;
    }
    jobs.forEach(job => {
        const div = document.createElement("div");
        div.className = "job";
        div.innerHTML = `
          <strong>${job.company}</strong>
          ${["Google","Amazon","Meta","Apple","Netflix","Microsoft","SBI"].includes(job.company) ? `<span class="job-badge">Top</span>` : ""}
          <br>Role: ${job.role}<br>
          Location: ${job.location}<br>
          <a href="${job.apply_link}" target="_blank">Apply Now</a>`;
        jobsDiv.appendChild(div);
    });
}

// Job Search Filter
searchInput.addEventListener("input", (e) => {
    const filtered = jobsData.filter(job => 
        job.company.toLowerCase().includes(e.target.value.toLowerCase()) ||
        job.role.toLowerCase().includes(e.target.value.toLowerCase()) ||
        job.location.toLowerCase().includes(e.target.value.toLowerCase())
    );
    renderJobs(filtered);
});

// Contact Form Submission
document.getElementById("contact-form").addEventListener("submit", e => {
    e.preventDefault();
    document.getElementById("contact-msg").innerText = "Thank you! We'll get back to you soon.";
    e.target.reset();
});

// Smooth scroll
document.querySelectorAll('nav a').forEach(anchor => {
  anchor.addEventListener('click', function(e){
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
  });
});

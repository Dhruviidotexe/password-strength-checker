const input = document.querySelector("#passwordInput");
const toggle = document.querySelector("#togglePassword");
const clearButton = document.querySelector("#clearButton");
const scoreValue = document.querySelector("#scoreValue");
const strengthLabel = document.querySelector("#strengthLabel");
const meterFill = document.querySelector("#meterFill");
const checksList = document.querySelector("#checksList");
const suggestionsList = document.querySelector("#suggestionsList");
const entropyValue = document.querySelector("#entropyValue");
const entropyText = document.querySelector("#entropyText");
const poolText = document.querySelector("#poolText");
const mascot = document.querySelector("#moodMascot");

let debounceTimer;
let visible = false;
let animatedScore = 0;

const checkLabels = [
  ["length", "12+ characters", false],
  ["excellent_length", "16+ characters", false],
  ["lowercase", "Lowercase letters", false],
  ["uppercase", "Uppercase letters", false],
  ["numbers", "Numbers", false],
  ["special", "Special characters", false],
  ["diversity", "Character diversity", false],
  ["repetition", "No excessive repetition detected", true],
  ["sequence", "No predictable sequence detected", true],
  ["common", "No common password pattern", true],
];

function animateNumber(target) {
  const start = animatedScore;
  const startTime = performance.now();
  const duration = 420;
  function tick(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    animatedScore = Math.round(start + (target - start) * eased);
    scoreValue.textContent = animatedScore;
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

function resetUi() {
  input.value = "";
  animatedScore = 0;
  scoreValue.textContent = "0";
  strengthLabel.textContent = "Let's put it to the test.";
  meterFill.style.width = "0%";
  meterFill.dataset.level = "";
  entropyValue.textContent = "0";
  entropyText.textContent = "Entropy estimates how unpredictable a password is based on its length and character set.";
  poolText.textContent = "Character pool: 0 possible characters";
  mascot.dataset.mood = "empty";
  checksList.innerHTML = "";
  suggestionsList.innerHTML = "<li>Enter a password above and we'll break down its strength.</li>";
  input.type = "password";
  visible = false;
  toggle.setAttribute("aria-label", "Show password");
}

function renderChecks(checks) {
  checksList.innerHTML = "";
  checkLabels.forEach(([key, label, inverted]) => {
    const value = Boolean(checks[key]);
    const passed = inverted ? !value : value;
    const li = document.createElement("li");
    li.className = passed ? "pass" : "warn";
    li.textContent = `${passed ? "✓" : "⚠"} ${label}`;
    checksList.appendChild(li);
  });
}

function renderSuggestions(items) {
  suggestionsList.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    suggestionsList.appendChild(li);
  });
}

function setMood(score) {
  if (!input.value) mascot.dataset.mood = "empty";
  else if (score < 50) mascot.dataset.mood = "weak";
  else if (score < 70) mascot.dataset.mood = "moderate";
  else mascot.dataset.mood = "strong";
}

async function analyze() {
  const password = input.value;
  if (!password) {
    resetUi();
    return;
  }
  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to analyze password.");

    animateNumber(data.score);
    strengthLabel.textContent = data.strength;
    meterFill.style.width = `${data.score}%`;
    meterFill.dataset.level = data.strength.toLowerCase().replaceAll(" ", "-");
    entropyValue.textContent = data.entropy;
    entropyText.textContent = `${data.length} characters. Entropy is an estimate based on length and character set, not a guarantee.`;
    poolText.textContent = `Character pool: ~${data.character_pool} possible characters`;
    renderChecks(data.checks);
    renderSuggestions(data.suggestions);
    setMood(data.score);
  } catch (error) {
    strengthLabel.textContent = "Analysis unavailable";
    suggestionsList.innerHTML = "";
    const li = document.createElement("li");
    li.textContent = "Something went wrong. Try again in a moment.";
    suggestionsList.appendChild(li);
  }
}

input.addEventListener("input", () => {
  window.clearTimeout(debounceTimer);
  debounceTimer = window.setTimeout(analyze, 140);
});

toggle.addEventListener("click", () => {
  visible = !visible;
  input.type = visible ? "text" : "password";
  toggle.classList.toggle("visible", visible);
  toggle.setAttribute("aria-label", visible ? "Hide password" : "Show password");
  input.focus();
});

clearButton.addEventListener("click", resetUi);

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = document.querySelector(link.getAttribute("href"));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add("shown");
  });
}, { threshold: 0.16 });

document.querySelectorAll(".reveal").forEach((item) => observer.observe(item));
window.setTimeout(() => document.body.classList.add("intro-done"), 4400);
resetUi();

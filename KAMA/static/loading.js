let facts = [];
let shuffledFacts = [];
let currentFactIndex = 0;
const factElement = document.getElementById('fact');

function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

async function loadFacts() {
  try {
    const response = await fetch("/static/facts.txt");
    if (!response.ok) throw new Error("Failed to fetch facts.txt");

    const text = await response.text();
    const lines = text.split("\n");

    facts = lines
      .map(line => line.trim())
      .filter(line => line && !line.match(/^\d+\.?\s*$/))
      .map(line => line.replace(/^\d+\.\s*/, "")); // Remove "1.", "2.", etc.

    if (facts.length === 0) throw new Error("No facts found");

    shuffledFacts = shuffleArray(facts);
    displayFact();
    setInterval(displayFact, 6000);
  } catch (error) {
    console.error("Error loading facts:", error);
    factElement.textContent = "Did you know? Loading takes time, but learning is instant!";
    factElement.style.opacity = "1";
  }
}

function displayFact() {
  if (shuffledFacts.length > 0) {
    factElement.textContent = shuffledFacts[currentFactIndex];
    currentFactIndex = (currentFactIndex + 1) % shuffledFacts.length;
    if (currentFactIndex === 0) shuffledFacts = shuffleArray(facts);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadFacts();

  const userRole = document.body.dataset.role;

  setTimeout(() => {
    if (userRole === "faculty") {
      window.location.href = "/faculty";
    } else if (userRole === "admin") {
      window.location.href = "/admin";
    } else {
      window.location.href = "/student";
    }
  }, 8000);
});

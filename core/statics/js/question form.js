
const steps = document.querySelectorAll(".step");
const dots = document.querySelectorAll(".dot");
let currentStep = 0;

document.getElementById("nextBtn").addEventListener("click", () => {
  if (currentStep < steps.length - 1) {
    steps[currentStep].classList.add("d-none");
    currentStep++;
    steps[currentStep].classList.remove("d-none");
    updateUI();
  }
});

document.getElementById("prevBtn").addEventListener("click", () => {
  if (currentStep > 0) {
    steps[currentStep].classList.add("d-none");
    currentStep--;
    steps[currentStep].classList.remove("d-none");
    updateUI();
  }
});

document.querySelectorAll(".emoji-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".emoji-btn").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
  });
});

function updateUI() {
  document.getElementById("stepIndicator").innerText = `${currentStep + 1} / 8`;
  dots.forEach(dot => dot.classList.remove("active"));
  dots[currentStep].classList.add("active");
}

const input = document.getElementById("locationInput");
const suggestions = document.getElementById("suggestions");

input.addEventListener("input", () => {
  const q = input.value.trim().toLowerCase();
  suggestions.innerHTML = "";
  if (!q) return;

  const matches = locations.filter(loc => loc.toLowerCase().includes(q));
  matches.slice(0, 10).forEach(m => {
    const li = document.createElement("li");
    li.textContent = m;
    li.onclick = () => {
      input.value = m;
      suggestions.innerHTML = "";
    };
    suggestions.appendChild(li);
  });
});

document.addEventListener("click", (e) => {
  if (e.target !== input) {
    suggestions.innerHTML = "";
  }
});

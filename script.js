async function analyzeDNA() {
  const input = document.getElementById("dnaInput");
  const output = document.getElementById("result");

  const dna = (input.value || "").trim();

  output.textContent = "Analyzing...";

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dna })
    });

    const data = await res.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    output.textContent = "Error: " + e;
  }
}

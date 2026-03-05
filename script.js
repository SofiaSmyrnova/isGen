async function go() {
  const dna = (document.getElementById("dna").value || "").trim();

  const spinner = document.getElementById("spinner");
  const placeholder = document.getElementById("placeholder");
  const results = document.getElementById("results");
  const metaRow = document.getElementById("metaRow");

  if (placeholder) placeholder.style.display = "none";
  if (results) {
    results.style.display = "flex";          
    results.classList.add("visible");
    results.innerHTML = "<div class='section-title'>Processing</div><pre>Sending request...</pre>";
  }
  if (spinner) spinner.style.display = "inline-block";

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dna })
    });

    const text = await res.text();

    if (results) {
      results.innerHTML =
        `<div class="section-title">Server response (status ${res.status})</div>` +
        `<pre style="white-space:pre-wrap; font-size:12px;">${escapeHtml(text)}</pre>`;
    }

    if (!res.ok) return;

    const data = JSON.parse(text);

    if (metaRow) metaRow.style.display = "flex";
    const mLen = document.getElementById("mLen");
    const mCodons = document.getElementById("mCodons");
    const mGC = document.getElementById("mGC");

    const seq = data.cleaned_dna || "";
    if (mLen) mLen.textContent = seq.length ? String(seq.length) : "—";
    if (mCodons) mCodons.textContent = (data.codon_count ?? "—");
    if (mGC) {
      const g = (seq.match(/G/g) || []).length;
      const c = (seq.match(/C/g) || []).length;
      const gc = seq.length ? Math.round(((g + c) * 1000) / seq.length) / 10 : 0;
      mGC.textContent = seq.length ? `${gc}%` : "—";
    }

  } catch (e) {
    if (results) {
      results.innerHTML =
        `<div class="section-title">JS error</div>` +
        `<pre style="white-space:pre-wrap; font-size:12px;">${escapeHtml(String(e))}</pre>`;
    }
  } finally {
    if (spinner) spinner.style.display = "none";
  }
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function go() {

  const dna = (document.getElementById("dna").value || "").trim();

  const spinner = document.getElementById("spinner");
  const results = document.getElementById("results");
  const placeholder = document.getElementById("placeholder");
  const metaRow = document.getElementById("metaRow");

  const mLen = document.getElementById("mLen");
  const mCodons = document.getElementById("mCodons");
  const mGC = document.getElementById("mGC");

  if (spinner) spinner.style.display = "inline-block";

  const res = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ dna: dna })
  });

  const data = await res.json();

  if (spinner) spinner.style.display = "none";
  if (placeholder) placeholder.style.display = "none";

  if (results) {
    results.classList.add("visible");
  }

  if (metaRow) metaRow.style.display = "flex";

  if (mLen) mLen.textContent = data.cleaned_dna ? data.cleaned_dna.length : "—";
  if (mCodons) mCodons.textContent = data.codon_count ?? "—";

  if (mGC) {
    const seq = data.cleaned_dna || "";
    const g = (seq.match(/G/g) || []).length;
    const c = (seq.match(/C/g) || []).length;
    const gc = seq.length ? Math.round(((g + c) * 1000) / seq.length) / 10 : 0;
    mGC.textContent = seq.length ? `${gc}%` : "—";
  }

  renderPretty(data);
}



function renderPretty(d){

  const results = document.getElementById("results");

  results.innerHTML = `

  <div class="section-title">Summary</div>

  <div class="stat-grid">

  <div class="stat-cell">
  <div class="s-label">Length</div>
  <div class="s-value">${d.cleaned_dna.length}</div>
  </div>

  <div class="stat-cell">
  <div class="s-label">Codons</div>
  <div class="s-value">${d.codon_count}</div>
  </div>

  <div class="stat-cell">
  <div class="s-label">Start Codon</div>
  <div class="s-value ${d.start_ok ? "ok":"err"}">
  ${d.start_ok ? "OK":"Mutation"}
  </div>
  </div>

  <div class="stat-cell">
  <div class="s-label">Stop Codon</div>
  <div class="s-value ${d.ends_with_stop ? "ok":"warn"}">
  ${d.ends_with_stop ? "OK":"Missing"}
  </div>
  </div>

  </div>


  <div class="section-title">RNA</div>

  <div class="freq-table">
  <div class="freq-row" style="grid-template-columns:1fr;">
  <div style="font-family:'DM Mono', monospace; letter-spacing:0.1em;">
  ${d.rna || "—"}
  </div>
  </div>
  </div>



  <div class="section-title">Codon Frequency</div>

  <div class="freq-table">

  ${Object.entries(d.frequency || {}).map(([codon,count])=>`

  <div class="freq-row">

  <div class="codon-tag">${codon}</div>

  <div class="freq-bar-wrap">
  <div class="freq-bar" style="width:${count*25}px"></div>
  </div>

  <div class="freq-count">${count}</div>

  </div>

  `).join("")}

  </div>


  <div class="section-title">Palindromes</div>

  <div class="freq-table">

  ${(d.palindromes || []).length === 0 ?

  `<div class="freq-row" style="grid-template-columns:1fr;">
  <div>None</div>
  </div>`

  :

  d.palindromes.map(c=>`

  <div class="freq-row">

  <div class="codon-tag">${c}</div>
  <div></div>
  <div class="freq-count">pal</div>

  </div>

  `).join("")}

  </div>


  <div class="section-title">Known Mutations</div>

  <div class="mut-list">

  ${(d.known_mutations_found || []).length === 0 ?

  `<div class="mut-item">
  <div class="codon">None</div>
  <div class="desc">No known mutations detected</div>
  </div>`

  :

  d.known_mutations_found.map(m=>`

  <div class="mut-item">

  <div class="codon">${m.codon}</div>
  <div class="desc">${m.description || ""}</div>

  </div>

  `).join("")}

  </div>

  `;
}

"""Flask app for the Prompt Injection Playground.

Interactive demo where users type prompts and see them classified
as injection or benign, with explanations of why.
"""

import json
from flask import Flask, render_template_string, request, jsonify
from src.demo.classifier import classify_prompt, EXAMPLE_PROMPTS
from src.research.taxonomy import ATTACK_TAXONOMY
from src.research.detection import DETECTION_TECHNIQUES
from src.research.prevention import PREVENTION_STRATEGIES

app = Flask(__name__)

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Prompt Injection Playground</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0a0a0f;--surface:#12121a;--surface2:#1a1a26;--surface3:#222233;
  --border:#2a2a3d;--border-glow:#3d3d5c;
  --text:#e0e0ec;--text-dim:#8888a0;--text-muted:#55556a;
  --red:#ff3355;--red-dim:#ff335520;--red-glow:#ff335540;
  --green:#00dd88;--green-dim:#00dd8820;--green-glow:#00dd8840;
  --blue:#4488ff;--blue-dim:#4488ff20;--blue-glow:#4488ff40;
  --amber:#ffaa22;--amber-dim:#ffaa2220;
  --purple:#aa66ff;--purple-dim:#aa66ff15;
  --mono:'JetBrains Mono',monospace;--sans:'Space Grotesk',sans-serif;
}
html{font-size:15px}
body{
  background:var(--bg);color:var(--text);font-family:var(--sans);
  min-height:100vh;overflow-x:hidden;
}
body::before{
  content:'';position:fixed;inset:0;z-index:-1;
  background:
    radial-gradient(ellipse 800px 600px at 20% 20%,#ff335508,transparent),
    radial-gradient(ellipse 600px 800px at 80% 80%,#4488ff06,transparent);
}

/* Scanline effect */
body::after{
  content:'';position:fixed;inset:0;z-index:9999;pointer-events:none;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.03) 2px,rgba(0,0,0,.03) 4px);
}

.container{max-width:1100px;margin:0 auto;padding:2rem 1.5rem}

/* Header */
header{text-align:center;padding:3rem 0 2rem}
header h1{
  font-family:var(--mono);font-size:2rem;font-weight:700;
  letter-spacing:-0.02em;
  background:linear-gradient(135deg,var(--red),var(--blue));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
header .subtitle{color:var(--text-dim);font-size:.9rem;margin-top:.5rem;font-family:var(--mono)}
header .badge{
  display:inline-block;margin-top:1rem;
  padding:.3rem .8rem;border-radius:2px;
  background:var(--red-dim);border:1px solid var(--red);
  color:var(--red);font-family:var(--mono);font-size:.7rem;
  text-transform:uppercase;letter-spacing:.1em;
}

/* Input area */
.input-section{
  background:var(--surface);border:1px solid var(--border);
  border-radius:4px;padding:1.5rem;margin-bottom:1.5rem;
  position:relative;
}
.input-section::before{
  content:'INPUT >';position:absolute;top:.6rem;left:1rem;
  font-family:var(--mono);font-size:.65rem;color:var(--text-muted);
  letter-spacing:.15em;text-transform:uppercase;
}
textarea{
  width:100%;height:120px;margin-top:1rem;
  background:var(--surface2);border:1px solid var(--border);
  border-radius:2px;padding:1rem;resize:vertical;
  color:var(--text);font-family:var(--mono);font-size:.85rem;
  line-height:1.6;outline:none;transition:border-color .2s;
}
textarea:focus{border-color:var(--blue);box-shadow:0 0 0 1px var(--blue-glow)}
textarea::placeholder{color:var(--text-muted)}

.controls{display:flex;gap:.8rem;margin-top:1rem;align-items:center;flex-wrap:wrap}
.btn{
  font-family:var(--mono);font-size:.8rem;padding:.6rem 1.4rem;
  border:1px solid;border-radius:2px;cursor:pointer;
  transition:all .15s;letter-spacing:.02em;
}
.btn-primary{
  background:var(--red);border-color:var(--red);color:#fff;
}
.btn-primary:hover{background:#ff1144;box-shadow:0 0 20px var(--red-glow)}
.btn-secondary{
  background:transparent;border-color:var(--border);color:var(--text-dim);
}
.btn-secondary:hover{border-color:var(--text-dim);color:var(--text)}

/* Examples */
.examples{display:flex;gap:.5rem;flex-wrap:wrap;margin-left:auto}
.example-chip{
  font-family:var(--mono);font-size:.65rem;padding:.35rem .7rem;
  border-radius:2px;cursor:pointer;transition:all .15s;
  border:1px solid var(--border);background:var(--surface2);color:var(--text-dim);
}
.example-chip:hover{border-color:var(--text-dim);color:var(--text)}
.example-chip.injection{border-color:var(--red-dim);color:var(--red)}
.example-chip.injection:hover{border-color:var(--red);background:var(--red-dim)}
.example-chip.benign{border-color:var(--green-dim);color:var(--green)}
.example-chip.benign:hover{border-color:var(--green);background:var(--green-dim)}

/* Result panel */
.result{
  background:var(--surface);border:1px solid var(--border);
  border-radius:4px;padding:1.5rem;margin-bottom:1.5rem;
  display:none;animation:fadeSlide .3s ease;
}
@keyframes fadeSlide{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.result.show{display:block}
.result.injection{border-color:var(--red);box-shadow:0 0 30px var(--red-dim)}
.result.benign{border-color:var(--green);box-shadow:0 0 30px var(--green-dim)}

.result-header{display:flex;align-items:center;gap:1rem;margin-bottom:1rem}
.verdict{
  font-family:var(--mono);font-size:1.1rem;font-weight:700;
  text-transform:uppercase;letter-spacing:.05em;
}
.result.injection .verdict{color:var(--red)}
.result.benign .verdict{color:var(--green)}

.confidence-bar{
  flex:1;height:6px;background:var(--surface3);border-radius:3px;overflow:hidden;
}
.confidence-fill{height:100%;border-radius:3px;transition:width .5s ease}
.result.injection .confidence-fill{background:linear-gradient(90deg,var(--amber),var(--red))}
.result.benign .confidence-fill{background:linear-gradient(90deg,var(--blue),var(--green))}
.confidence-label{font-family:var(--mono);font-size:.75rem;color:var(--text-dim)}

.result-section{margin-top:1.2rem}
.result-section h3{
  font-family:var(--mono);font-size:.7rem;color:var(--text-muted);
  text-transform:uppercase;letter-spacing:.15em;margin-bottom:.6rem;
}
.result-section p{font-size:.85rem;line-height:1.7;color:var(--text-dim)}
.category-tag{
  display:inline-block;padding:.2rem .6rem;border-radius:2px;
  font-family:var(--mono);font-size:.7rem;
  background:var(--red-dim);border:1px solid var(--red);color:var(--red);
}

.patterns-list{list-style:none;margin-top:.5rem}
.patterns-list li{
  padding:.6rem .8rem;margin-bottom:.4rem;
  background:var(--surface2);border-left:2px solid var(--red);
  border-radius:0 2px 2px 0;font-size:.8rem;line-height:1.5;
}
.patterns-list li .pat-cat{
  font-family:var(--mono);font-size:.65rem;color:var(--amber);
  display:block;margin-bottom:.2rem;
}
.patterns-list li .pat-explain{color:var(--text-dim)}

.defense-list{list-style:none;margin-top:.5rem}
.defense-list li{
  padding:.5rem .8rem;margin-bottom:.3rem;
  background:var(--green-dim);border-left:2px solid var(--green);
  border-radius:0 2px 2px 0;
  font-size:.8rem;line-height:1.5;color:var(--text-dim);
}

/* Knowledge panels */
.knowledge{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
  gap:1rem;margin-top:2rem;
}
.k-panel{
  background:var(--surface);border:1px solid var(--border);
  border-radius:4px;padding:1.2rem;
}
.k-panel h3{
  font-family:var(--mono);font-size:.75rem;color:var(--purple);
  text-transform:uppercase;letter-spacing:.1em;margin-bottom:.8rem;
  padding-bottom:.5rem;border-bottom:1px solid var(--border);
}
.k-item{margin-bottom:.8rem}
.k-item h4{font-size:.8rem;color:var(--text);margin-bottom:.2rem}
.k-item p{font-size:.75rem;color:var(--text-muted);line-height:1.5}

footer{
  text-align:center;padding:3rem 0 2rem;
  font-family:var(--mono);font-size:.7rem;color:var(--text-muted);
}
footer a{color:var(--blue);text-decoration:none}

/* Loading */
.loading{display:none;align-items:center;gap:.5rem;color:var(--text-dim);font-family:var(--mono);font-size:.8rem}
.loading.show{display:flex}
.spinner{
  width:14px;height:14px;border:2px solid var(--border);
  border-top-color:var(--blue);border-radius:50%;
  animation:spin .6s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}

@media(max-width:768px){
  html{font-size:14px}
  .container{padding:1rem}
  header h1{font-size:1.5rem}
  .examples{margin-left:0;margin-top:.5rem}
  .controls{flex-direction:column;align-items:stretch}
}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>&gt;_ PROMPT INJECTION PLAYGROUND</h1>
    <div class="subtitle">Interactive classifier for LLM prompt injection attacks</div>
    <div class="badge">⚠ Educational Demo — Heuristic Detection Only</div>
  </header>

  <div class="input-section">
    <textarea id="prompt-input" placeholder="Type a prompt to classify... try injecting instructions, jailbreaking, or asking a normal question."></textarea>
    <div class="controls">
      <button class="btn btn-primary" onclick="classifyPrompt()">⚡ Analyze</button>
      <button class="btn btn-secondary" onclick="clearAll()">Clear</button>
      <div class="loading" id="loading"><div class="spinner"></div>Analyzing...</div>
      <div class="examples" id="examples"></div>
    </div>
  </div>

  <div class="result" id="result">
    <div class="result-header">
      <div class="verdict" id="verdict"></div>
      <div class="confidence-bar"><div class="confidence-fill" id="conf-fill"></div></div>
      <div class="confidence-label" id="conf-label"></div>
    </div>
    <div id="category-row" class="result-section" style="display:none">
      <h3>Attack Category</h3>
      <span class="category-tag" id="category"></span>
    </div>
    <div class="result-section">
      <h3>Analysis</h3>
      <p id="explanation"></p>
    </div>
    <div id="patterns-section" class="result-section" style="display:none">
      <h3>Matched Patterns</h3>
      <ul class="patterns-list" id="patterns"></ul>
    </div>
    <div class="result-section">
      <h3>Defense Recommendations</h3>
      <ul class="defense-list" id="defenses"></ul>
    </div>
  </div>

  <div class="knowledge">
    <div class="k-panel">
      <h3>Attack Taxonomy</h3>
      <div id="taxonomy-list"></div>
    </div>
    <div class="k-panel">
      <h3>Detection Methods</h3>
      <div id="detection-list"></div>
    </div>
    <div class="k-panel">
      <h3>Prevention Strategies</h3>
      <div id="prevention-list"></div>
    </div>
  </div>

  <footer>
    CCI Undergraduate Research — Prompt Injection Security &middot;
    <a href="https://owasp.org/www-project-top-10-for-large-language-model-applications/" target="_blank">OWASP LLM Top 10</a>
  </footer>
</div>

<script>
const examples = {{ examples | tojson }};
const taxonomy = {{ taxonomy | tojson }};
const detection = {{ detection | tojson }};
const prevention = {{ prevention | tojson }};

// Populate examples
const exDiv = document.getElementById('examples');
examples.forEach(ex => {
  const chip = document.createElement('span');
  chip.className = 'example-chip ' + (ex.label === 'Injection' ? 'injection' : 'benign');
  chip.textContent = ex.description;
  chip.title = ex.text;
  chip.onclick = () => {
    document.getElementById('prompt-input').value = ex.text;
    classifyPrompt();
  };
  exDiv.appendChild(chip);
});

// Populate knowledge panels (first 4 each)
function populateKnowledge() {
  const taxList = document.getElementById('taxonomy-list');
  taxonomy.slice(0, 5).forEach(t => {
    taxList.innerHTML += `<div class="k-item"><h4>${t.category}</h4><p>${t.description.substring(0, 120)}...</p></div>`;
  });
  const detList = document.getElementById('detection-list');
  detection.forEach(d => {
    detList.innerHTML += `<div class="k-item"><h4>${d.technique}</h4><p>${d.description.substring(0, 120)}...</p></div>`;
  });
  const prevList = document.getElementById('prevention-list');
  prevention.slice(0, 5).forEach(p => {
    prevList.innerHTML += `<div class="k-item"><h4>${p.strategy}</h4><p>${p.description.substring(0, 120)}...</p></div>`;
  });
}
populateKnowledge();

async function classifyPrompt() {
  const text = document.getElementById('prompt-input').value.trim();
  if (!text) return;
  
  const loading = document.getElementById('loading');
  const result = document.getElementById('result');
  loading.classList.add('show');
  result.classList.remove('show', 'injection', 'benign');

  try {
    const res = await fetch('/classify', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text})
    });
    const data = await res.json();
    
    loading.classList.remove('show');
    
    const cls = data.is_injection ? 'injection' : 'benign';
    result.classList.add('show', cls);
    
    document.getElementById('verdict').textContent = data.label;
    document.getElementById('conf-fill').style.width = (data.confidence * 100) + '%';
    document.getElementById('conf-label').textContent = Math.round(data.confidence * 100) + '%';
    document.getElementById('explanation').textContent = data.explanation;
    
    const catRow = document.getElementById('category-row');
    if (data.attack_category) {
      catRow.style.display = 'block';
      document.getElementById('category').textContent = data.attack_category;
    } else {
      catRow.style.display = 'none';
    }
    
    const patternsSection = document.getElementById('patterns-section');
    const patternsList = document.getElementById('patterns');
    if (data.matched_patterns && data.matched_patterns.length > 0) {
      patternsSection.style.display = 'block';
      patternsList.innerHTML = data.matched_patterns.map(p =>
        `<li><span class="pat-cat">${p.category} › ${p.subcategory}</span><span class="pat-explain">${p.explanation}</span></li>`
      ).join('');
    } else {
      patternsSection.style.display = 'none';
    }
    
    const defList = document.getElementById('defenses');
    defList.innerHTML = (data.defense_tips || []).map(d =>
      `<li>${d}</li>`
    ).join('');
    
  } catch(e) {
    loading.classList.remove('show');
    alert('Error: ' + e.message);
  }
}

function clearAll() {
  document.getElementById('prompt-input').value = '';
  document.getElementById('result').classList.remove('show', 'injection', 'benign');
}

// Enter key to submit
document.getElementById('prompt-input').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); classifyPrompt(); }
});
</script>
</body>
</html>"""


@app.route("/")
def index():
    """Render the playground UI."""
    return render_template_string(
        HTML_TEMPLATE,
        examples=EXAMPLE_PROMPTS,
        taxonomy=ATTACK_TAXONOMY,
        detection=DETECTION_TECHNIQUES,
        prevention=PREVENTION_STRATEGIES,
    )


@app.route("/classify", methods=["POST"])
def classify():
    """Classify a prompt and return JSON result."""
    data = request.get_json()
    text = data.get("text", "")
    result = classify_prompt(text)
    return jsonify({
        "is_injection": result.is_injection,
        "confidence": result.confidence,
        "label": result.label,
        "attack_category": result.attack_category,
        "explanation": result.explanation,
        "matched_patterns": result.matched_patterns,
        "defense_tips": result.defense_tips,
    })


@app.route("/api/taxonomy")
def api_taxonomy():
    """Return full attack taxonomy."""
    return jsonify(ATTACK_TAXONOMY)


@app.route("/api/detection")
def api_detection():
    """Return detection techniques."""
    return jsonify(DETECTION_TECHNIQUES)


@app.route("/api/prevention")
def api_prevention():
    """Return prevention strategies."""
    return jsonify(PREVENTION_STRATEGIES)


def main():
    """Run the demo server."""
    print("\n  Prompt Injection Playground")
    print("  http://localhost:5000\n")
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()

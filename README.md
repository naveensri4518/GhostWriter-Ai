# GhostWriter AI 👻
### *Stories from the Other Side*

[![Repository](https://img.shields.io/badge/GitHub-naveensri4518%2FGhostWriter--Ai-181717?logo=github)](https://github.com/naveensri4518/GhostWriter-Ai)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Framework](https://img.shields.io/badge/Backend-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Code License](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Model Weights](https://img.shields.io/badge/Model%20Weights-Apache%202.0%20(Qwen)-green.svg)](https://github.com/QwenLM/Qwen2.5)
[![AI Engine: Ollama](https://img.shields.io/badge/AI%20Engine-Ollama%20(Local)-E63946.svg)](https://ollama.com)

**GhostWriter AI** is an atmospheric, Halloween-themed full-stack horror story generation web application. It conjures custom, spine-chilling horror narratives using open-weight AI models running **100% locally on your computer** through **Ollama** and a lightweight Python Flask backend.

---

## 🌟 Local AI Inference & Privacy

GhostWriter AI is built around sovereign, local AI execution:

* **100% Local Inference**: All prompts, parameters, and generated horror tales are processed on your personal hardware via a local **Ollama** daemon.
* **No Cloud API Keys or Subscriptions**: Zero dependencies on closed proprietary APIs (such as OpenAI, Anthropic, or Google Cloud). No API keys, no monthly fees, and no per-token charges.
* **Complete Offline Privacy**: Once model weights are pulled locally, you can run the entire system offline. No prompts or user data ever leave your machine.
* **Model Agnostic**: Built and optimized for **Qwen 2.5 (3B)** (`qwen2.5:3b`), but fully compatible with other open-weight models available in Ollama (such as `llama3.2`, `mistral`, `phi3`, and `gemma2`) via a single environment variable.

---

## 🎭 Features

* 🔮 **Personalized Horror Generation**: Submit custom premises, urban folklore, or click one of the eerie inspiration prompt chips.
* 🏚️ **Five Distinct Horror Categories**:
  * **Haunted House**: Oppressive architectural isolation, creaking timbers, watchful rooms, and ancestral curses trapped in decaying walls.
  * **Supernatural**: Reality-defying anomalies, ancient occult invocations, and eldritch entities from beyond.
  * **Psychological Horror**: Unreliable narrators, sensory illusions, paranoia, claustrophobia, and the terrifying descent into madness.
  * **Ghost Stories**: Restless apparitions, midnight drafts, unresolved tragedies, and spectral whispers.
  * **Urban Legends**: Modern folklore, subterranean transit corridors, cursed technology, and forbidden nighttime rituals.
* 🩸 **Three Dynamic Ending Styles**:
  * **Terrifying**: Unresolved dread, impending doom, and chilling lingering horror.
  * **Tragic**: Heartbreaking loss, painful sacrifice, and sorrowful emotional resolution.
  * **Unexpected Twist**: Mind-bending plot twist that subverts expectations and turns assumptions upside down.
* 👻 **Atmospheric User Experience**:
  * Dark Halloween palette: Void Black (`#080808`), Crimson (`#E63946`), and Spectral Violet (`#8B5CF6`).
  * Real-time HTML5 Canvas particle system rendering floating spectral mist and eerie ember particles.
  * Multi-stage animated loading state (*"The spirits are writing your story..."*).
* 📋 **Story Management**:
  * **Copy to Clipboard**: One-click formatted story copy with toast feedback.
  * **Download as `.txt`**: Export your generated tales to your local filesystem.
  * **Instant Regeneration**: Re-summon a fresh variation with the same settings in one click.
* 🛡️ **Real-Time Ollama Status Health Indicator**: Live polling verifies that the Ollama engine is online and the required model is loaded and ready.
* ⌨️ **Keyboard Accessibility**: Press `Ctrl + Enter` (or `Cmd + Enter`) anywhere inside the prompt input to immediately summon a tale.

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser (Frontend)                   │
│         HTML5  •  CSS3 (Gothic Theme)  •  Vanilla JS        │
│    • Interactive Canvas Spectral Particles                  │
│    • Real-time Health Polling & Keyboard Shortcuts          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ HTTP / REST (Fetch API)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend (app.py)                   │
│         Runs locally on http://127.0.0.1:5000               │
│                                                             │
│   GET  /             -> Renders UI with configured defaults │
│   GET  /api/health   -> Probes Ollama service & model state │
│   GET  /api/models   -> Lists locally installed models      │
│   POST /api/generate -> Validates input, constructs prompts,│
│                         and communicates with Ollama        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ HTTP POST /api/generate (Timeout: 120s)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Local Ollama Runtime Service                │
│         Runs locally on http://127.0.0.1:11434              │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │   Configured Model Weights: Qwen 2.5 (3B)           │   │
│   │   • Format: GGUF (4-bit / 8-bit quantized)          │   │
│   │   • License: Apache 2.0 (Open Weights)              │   │
│   │   • Local CPU / GPU / Vulkan acceleration           │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📸 Interface Preview & Layout

```
+-----------------------------------------------------------------------+
|  👻 GHOSTWRITER AI               [ ● Ollama: qwen2.5:3b (Ready) ]     |
|     Stories from the Other Side                                       |
+-----------------------------------------------------------------------+
|                                                                       |
|  Select Horror Category:                                              |
|  [ Haunted House ] [ Supernatural ] [ Psychological ] [ Ghost Story ] |
|                                                                       |
|  Ending Style:                                                        |
|  (o) Terrifying     ( ) Tragic     ( ) Unexpected Twist               |
|                                                                       |
|  Story Idea or Premise:                                               |
|  +-----------------------------------------------------------------+  |
|  | An antique pocket watch found in an abandoned asylum begins     |  |
|  | ticking backward at midnight...                                 |  |
|  +-----------------------------------------------------------------+  |
|  Inspiration: [ Cursed Mirror ] [ Whispering Radio ] [ Attic Trunk ]  |
|                                                                       |
|                     [ 🔮 Summon the Spirits ]                         |
|                                                                       |
+-----------------------------------------------------------------------+
|  THE ANTIQUARIAN'S LAST BREATH                                        |
|  Category: Supernatural | Ending: Unexpected Twist | Words: 360       |
|  -------------------------------------------------------------------  |
|  In the dim light of the dusty attic, a single antique pocket watch   |
|  hung from the ceiling, its hands inching backward with each tick...  |
|                                                                       |
|  [ 📋 Copy Story ]         [ 💾 Download .txt ]      [ 🔄 Re-roll ]   |
+-----------------------------------------------------------------------+
```

---

## 🛠️ Technology Stack

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript | Zero external JavaScript frameworks. Custom CSS variable system and Canvas animation engine. |
| **Backend** | Python 3.10+, Flask 3.0+ | Lightweight WSGI application providing REST endpoints and static file serving. |
| **HTTP Client** | `requests` (v2.31+) | Synchronous HTTP communication with Ollama's local REST endpoints. |
| **AI Runtime** | Ollama | Open-source local model runtime supporting macOS, Linux, and Windows. |
| **Model** | Qwen 2.5 (3B) | Alibaba Cloud's state-of-the-art 3B parameter multilingual language model. |

---

## 📂 Project Structure

```
GhostWriter-Ai/
├── app.py              # Flask server, API endpoints, prompt builder, Ollama integration
├── requirements.txt    # Minimal Python dependencies (Flask, requests)
├── verify_setup.py     # Automated test suite (routes, health checks, generation)
├── README.md           # Comprehensive project documentation
├── LICENSE             # Project MIT License & upstream notices
├── .gitignore          # Exclusions for virtual environments, caches, and secrets
├── templates/
│   └── index.html      # Responsive Halloween-themed single-page application
└── static/
    ├── css/
    │   └── style.css   # Dark gothic aesthetics, responsive layout, animations
    └── js/
        └── script.js   # Client controller, canvas effects, health checks, API calls
```

---

## 🚀 Installation & Setup

### Prerequisites

1. **Python 3.10 or higher** installed ([Download Python](https://python.org)).
2. **Ollama** installed on your machine ([Download Ollama](https://ollama.com/download)).
3. **Git** installed on your system ([Download Git](https://git-scm.com/)).

### Step 1: Clone the Repository

```bash
git clone https://github.com/naveensri4518/GhostWriter-Ai.git
cd GhostWriter-Ai
```

### Step 2: Set Up a Python Virtual Environment

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the Ollama Service

Ensure the Ollama service is active. If not running in the system background, start it in a separate terminal:

```bash
ollama serve
```

### Step 5: Pull the AI Model

GhostWriter AI is configured to use `qwen2.5:3b` (~1.9 GB), an efficient, high-performance creative writing model:

```bash
ollama pull qwen2.5:3b
```

*(Optional: You may also pull any other model, such as `ollama pull llama3.2` or `ollama pull mistral`).*

---

## 🏃 Running the Application

In your project terminal with your virtual environment activated:

```bash
python app.py
```

You should see console output:
```text
============================================================
[*] GHOSTWRITER AI - Stories from the Other Side
============================================================
 * Server running on: http://127.0.0.1:5000
 * Configured Ollama Model: qwen2.5:3b
 * Ollama Host: http://127.0.0.1:11434
============================================================
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running the Verification Test Suite

A comprehensive test suite is included in `verify_setup.py`. It validates:
1. **Frontend Rendering**: Ensures `GET /` serves valid HTML and branding.
2. **Ollama Health Check**: Validates `/api/health`, confirming Ollama is online and the model is present.
3. **Input Validation**: Tests error handling on empty or invalid inputs.
4. **End-to-End Story Generation**: Executes a live generation request with Ollama, measuring latency and validating output structure.

To execute the tests:

```bash
python verify_setup.py
```

Expected output:
```text
============================================================
RUNNING GHOSTWRITER AI TEST SUITE
============================================================
[Test 1] Testing GET / (Homepage)...
PASSED: Homepage loaded with full HTML template and configuration.

[Test 2] Testing GET /api/health...
PASSED: Health check verified Ollama is online and qwen2.5:3b is ready.

[Test 3] Testing POST /api/generate with empty prompt...
PASSED: Correctly rejected empty prompt with message: Please provide a story idea...

[Test 4] Testing End-to-End Story Generation with Ollama...
PASSED: End-to-end story generation succeeded with rich title and content.

============================================================
ALL TESTS PASSED SUCCESSFULLY! GHOSTWRITER AI IS FULLY OPERATIONAL.
============================================================
```

---

## ⚙️ Configuration & Customization

The application can be customized through environment variables:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `OLLAMA_MODEL` | `qwen2.5:3b` | The model tag Ollama uses for generation (e.g. `llama3.2`, `mistral`, `gemma2`). |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | The host URL where the Ollama API is listening. |
| `REQUEST_TIMEOUT` | `120` | Maximum time in seconds to wait for Ollama to complete story inference. |
| `PORT` | `5000` | The local port on which Flask serves the web app. |
| `HOST` | `127.0.0.1` | The network interface Flask binds to. |
| `FLASK_DEBUG` | `false` | Enables Flask debug mode and hot reloading if set to `true` or `1`. |

### Example: Running with a Different Model

```powershell
# In PowerShell:
$env:OLLAMA_MODEL = "llama3.2"
python app.py
```

```bash
# In Linux / macOS:
export OLLAMA_MODEL="llama3.2"
python app.py
```

---

## 🔍 Troubleshooting

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| **Status badge shows "Ollama Offline"** | The Ollama background process is not running. | Run `ollama serve` in a separate terminal or start the Ollama desktop app, then click the refresh icon in the UI. |
| **Status badge shows "Model Missing"** | The configured model has not been downloaded yet. | Run `ollama pull qwen2.5:3b` in your terminal. |
| **Story generation times out** | Low hardware resources or large model size. | Ensure you are using a compact 3B model (`qwen2.5:3b`) or increase timeout via `$env:REQUEST_TIMEOUT="180"`. |
| **Port 5000 is in use** | Another local service is bound to port 5000. | Start Flask on an alternate port: `$env:PORT="5050"; python app.py`. |

---

## 📜 Licensing & Open Weights Notice

* **Application Code**: Licensed under the **[MIT License](LICENSE)**. You are free to inspect, adapt, fork, and distribute the application source code.
* **Dependencies**:
  * **Flask**: BSD 3-Clause License
  * **Requests**: Apache 2.0 License
* **AI Model Weights & Runtime**:
  * **Ollama Runtime**: MIT License
  * **Qwen 2.5 (3B)** weights are developed by the Qwen Team / Alibaba Cloud and distributed under the **Apache 2.0 License**.
  * *Important Notice*: AI model weights are governed by upstream developer licenses and acceptable use policies. While Qwen 2.5 is released under Apache 2.0, other models you might choose to load (such as Meta Llama or Google Gemma) carry their own specific community licenses and terms of use. Please review the upstream license for any alternative model you pull.

---

## 🤝 Contributing

Contributions, bug reports, and horror theme enhancements are welcome!

1. Fork the repository on GitHub.
2. Create a descriptive feature branch: `git checkout -b feature/eerie-ambient-audio`
3. Commit your changes: `git commit -m 'Add spooky sound effects on generation'`
4. Push your branch: `git push origin feature/eerie-ambient-audio`
5. Open a Pull Request.

*Happy Haunting and Happy Hacking! 🎃*

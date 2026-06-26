# Shopping Assistant Agent

A secure, robust, and extensible AI Shopping Assistant built using the **Google Agent Development Kit (ADK) 2.0** and Gemini models. 

This repository contains the complete agent codebase, security boundaries, threat models, test suites, and an embeddable chat widget to integrate the agent into any external website.

---

## 🚀 Features

- **Discount Code Redemption:** Simulated secure redemption of single-use discount codes (e.g., `WELCOME50`, `SUMMER20`) with registered user verification.
- **Embedded Web Widget:** A lightweight, customizable JavaScript widget (`widget.js`) to embed the shopping assistant chat bubble directly on any website.
- **Outcome-Based Security Suite:** Full unit and security validation test coverage using `pytest`.
- **Pre-commit Scan Configuration:** Pre-configured Git hooks including Semgrep rules to scan for API credentials leakage.
- **STRIDE Threat Model:** Documented security boundaries and mitigations against common exploit paths.

---

## 📁 Repository Structure

```
.
├── shopping-assistant/
│   ├── .agents/               # Custom guidelines, validation scripts, and skills
│   ├── app/                   # Core agent implementation
│   │   ├── agent.py           # Main agent definition & tool registrations
│   │   ├── api_app.py         # CORS-enabled FastAPI backend
│   │   └── static/            # Static assets (widget.js & index.html)
│   ├── deployment/            # Infrastructure automation (Terraform)
│   ├── tests/                 # Unit, integration, and load test suites
│   ├── pyproject.toml         # Python dependencies & configuration
│   └── threat_model.md        # Documented STRIDE threat model
└── README.md                  # Root documentation (this file)
```

---

## 🛠️ Quick Start

### 1. Installation & Environment Setup
Clone this repository and sync python dependencies using `uv`:
```bash
cd shopping-assistant
uv sync
```

Ensure you have a `.env` file containing your Gemini API key:
```env
GEMINI_API_KEY="your-gemini-api-key"
```

### 2. Run Locally (Playground)
Start the local interactive ADK developer UI playground:
```bash
uv tool run --from google-agents-cli agents-cli playground
```
Open [http://localhost:8080/dev-ui/?app=app](http://localhost:8080/dev-ui/?app=app) in your web browser to chat with the agent locally.

### 3. Run the API Server
Launch the FastAPI server to serve the embeddable API and the widget scripts:
```bash
uv run uvicorn app.api_app:app --host 127.0.0.1 --port 7860
```

---

## 📦 How to Embed on Any Website

To embed the chat assistant widget on any external HTML website, add this single `<script>` tag inside your HTML body:

```html
<!-- Add this where you want the assistant to load -->
<script 
  src="http://localhost:7860/widget.js" 
  data-api-url="http://localhost:7860" 
  data-user-id="customer_jack">
</script>
```

Open [http://localhost:7860/index.html](http://localhost:7860/index.html) in your browser to view a live interactive demo of the embedded widget.

---

## 🧪 Testing

Run the outcome-based security test suite to verify tool boundaries:
```bash
uv run pytest tests/test_agent.py
```
This runs assertions checking:
- Code normalizations (whitespace/casing).
- Multi-use restrictions (single-use limit).
- Registered identity authorization.
- Schema parameter validation.

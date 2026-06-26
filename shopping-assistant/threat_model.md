# STRIDE Threat Model Assessment - `shopping-assistant`

This document performs a systematic threat modeling assessment of the `shopping-assistant` agent project based on the STRIDE framework.

---

## 1. System Boundaries & Architecture Mapping
* **Entry Points:**
  * **User Chat Interface:** Users interact via natural language.
  * **Agent Application (`app/agent.py`):** Holds the system instructions and wraps model calls.
  * **Agent Engine App Wrapper (`app/agent_runtime_app.py`):** Serves the agent on Vertex AI Agent Engine.
* **Storage Layers:**
  * **In-Memory Store (`DISCOUNT_CODES`):** Keeps track of whether single-use discount codes (e.g., `WELCOME50`, `SUMMER20`) have been redeemed.
  * **Registered Users Set (`REGISTERED_USERS`):** Contains user IDs of allowed customers.
* **Data Flow:**
  * `User Input` -> `Gemini Model (ADK)` -> `redeem_discount_code (Tool Call)` -> `In-Memory Store` -> `Tool Response` -> `User Output`.

---

## 2. STRIDE Assessment

### Spoofing (Identity Verification)
* **Threat:** A user can spoof a registered user's identity simply by stating a registered `user_id` (e.g., "I am user123").
* **Analysis:** The `redeem_discount_code` tool expects the user ID as an argument parsed by the LLM from the conversation. The agent has no mechanism to cryptographically verify or authenticate that the caller actually owns that `user_id`.
* **Mitigation:** The `user_id` should be populated securely by the backend application context (e.g., JWT claims or session context) rather than being extracted dynamically from the user's natural language input.

### Tampering (Data Manipulation)
* **Threat:** Unauthenticated state reset.
* **Analysis:** The redemption state is kept in-memory (`DISCOUNT_CODES` dictionary). Any restart of the application container resets the state, allowing previously redeemed codes to be used again. Additionally, concurrent requests could lead to race conditions if multiple workers handle redemptions concurrently without locking.
* **Mitigation:** Use a persistent, transactional database (like Cloud SQL or Firestore) with row-level locking to record redemptions atomically.

### Repudiation (Audit Trail)
* **Threat:** Lack of non-repudiation and transaction logging.
* **Analysis:** Redemptions return a string output which is printed in stdout/telemetry, but there is no secure, immutable audit log recording when and by whom a code was redeemed.
* **Mitigation:** Write audit records to an append-only transaction table or log system (e.g., Cloud Logging) with write-once/read-many constraints.

### Information Disclosure (Secret Leakage)
* **Threat:** Hardcoded mock credential exposure.
* **Analysis:** The mock API key `api_key="AIzaSyD-mock-key-value-12345"` is hardcoded directly in `app/agent.py`. In production, if real keys are checked in, they will be leaked.
* **Mitigation:** We implemented Semgrep static analysis and pre-commit hooks to block this pattern. Real credentials should always be loaded from secure environment variables (e.g., Secret Manager).

### Denial of Service (Resource Exhaustion)
* **Threat:** Quota depletion or application crash.
* **Analysis:** The agent does not enforce rate limiting on LLM invocation or tool execution. Attackers could flood the system with requests, causing high costs and exhausting Gemini API rate limits.
* **Mitigation:** Implement rate-limiting at the gateway level (e.g., API Gateway) to restrict calls per session/IP.

### Elevation of Privilege (Access Control)
* **Threat:** Guessing user IDs to perform redemptions.
* **Analysis:** Anyone can request redemption if they guess a registered user ID (e.g., `user123`), bypassing standard authorization checks.
* **Mitigation:** Bind the user session context securely to the request metadata, and validate permissions before allowing the agent runner to execute tools.

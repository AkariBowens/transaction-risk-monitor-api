# Real-Time Risk Assessment Engine

A high-performance FastAPI service designed to assess financial transaction risk in real-time. This engine evaluates transactions based on amount thresholds, blacklists, and account velocity.

## 🚀 Features

- **Automated Scoring:** Calculates risk based on multiple business rules.
- **Stateful Velocity Checks:** Uses **Redis** to track transaction frequency (Max 3 per minute).
- **Data Integrity:** Enforces strict API contracts with **Pydantic** validation and ISO-8601 timestamps.
- **Automated Testing:** Comprehensive suite using **Pytest** with automated Redis state management.

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Validation:** Pydantic v2
- **State Management:** Redis (via Docker)
- **Testing:** Pytest + HTTPX

## 📦 Installation & Setup

1. **Clone the repository:**

   ```PowerShell
   git clone https://github.com/AkariBowens/transaction-risk-monitor-api.git
   cd risk-engine
   ```

2. Start the Redis container:

   ```PowerShell
   docker run -d --name risk-redis -p 6379:6379 redis
   ```

3. Install dependencies:

   ```PowerShell
   pip install -r requirements.txt
   ```

4. Run the API:

   ```PowerShell
   uvicorn main:app --reload
   ```

## 🧪 Running Tests

The test suite includes an automated flushall fixture to ensure clean state between runs.

    ```PowerShell
    python -m pytest -v
    ```

## 💡 Engineering Highlights

**Clamping Logic:** Implemented score clamping to ensure API responses never violate schema constraints (le=100).

**Idempotent Testing:** Leveraged Pytest fixtures to reset Redis state, preventing data leakage between tests.

**UTC Normalization:** All transactions are processed using timezone.utc for global audit consistency.

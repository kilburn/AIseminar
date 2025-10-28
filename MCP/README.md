# 🧠 ContactsServer — FastMCP + FastAPI + Pydantic + SQLite  
**Author:** Antonio Lobo  

[![Docker Build](https://img.shields.io/badge/Docker-Build-success?logo=docker&style=flat-square)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Running-brightgreen?logo=fastapi&style=flat-square)](https://fastapi.tiangolo.com/)
[![MCP](https://img.shields.io/badge/Protocol-MCP-9cf?style=flat-square)](https://pvkl.nl/en/understanding-the-model-context-protocol/)

---

## 🧩 Overview

**ContactsServer** is a lightweight demonstration of the **Model Context Protocol (MCP)** using  
**FastMCP**, **FastAPI**, **Pydantic**, and an **SQLite** database.

It exposes:
- 🗂️ a **resource** — `data://contacts`: retrieves all stored contacts (validated via Pydantic),  
- 🔧 a **tool** — `save_contact`: adds or updates a contact (validated and structured using Pydantic),  
- 💬 a **prompt** — `summarise`: generates a simple summary of given text.

Each capability uses **Pydantic models** with detailed field descriptions.  
This ensures that both **LLMs and humans** can understand expected inputs and outputs directly from schema metadata.

---

## 📁 File Structure

```

.
├─ app.py                  # Main FastAPI + FastMCP application
├─ Dockerfile              # Image build definition
├─ docker-compose.yml      # Local service runner
├─ requirements.txt        # Python dependencies
├─ .env                    # Environment configuration
├─ db/
│  └─ my_database.sqlite   # (auto-created) SQLite database
└─ scripts/
└─ inspect.sh           # Utility to inspect MCP endpoints

```

---

## ⚙️ Configuration

All configuration values can be adjusted in the `.env` file:

```env
DB_PATH=/app/db/my_database.sqlite
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

---

## 🧱 Building and Running

### 1. Build the image

```bash
docker compose build
```

### 2. Start the service

```bash
docker compose up
```

Once running, the MCP server is available at
👉 **[http://localhost:8000](http://localhost:8000)**

Check health:

```bash
curl -fsS http://localhost:8000/health
# {"status":"ok"}
```

---

## 🧩 Pydantic Integration

All inputs and outputs in MCP tools, resources, and prompts use **Pydantic models** with rich field metadata.
This provides:

* ✅ Validation (e.g., email format, required fields),
* 🧾 Structured schemas that LLMs and UIs can interpret,
* 💬 Field-level descriptions for self-documentation.

### Example: Tool argument and return models

```python
class SaveContactArgs(BaseModel):
    """Input arguments required to save or update a contact."""
    name: str = Field(..., description="Full name of the contact.")
    email: EmailStr = Field(..., description="Unique e-mail address used as an identifier.")

class Contact(BaseModel):
    """Represents a single contact entry."""
    id: int = Field(..., description="Auto-incremented unique identifier.")
    name: str = Field(..., description="Full name of the contact.")
    email: EmailStr = Field(..., description="E-mail address.")
    created_at: datetime = Field(..., description="Creation timestamp (UTC).")

class SaveContactResult(BaseModel):
    """Result returned after saving a contact."""
    contact: Contact = Field(..., description="The saved or updated contact record.")
```

The MCP framework automatically surfaces these models’ descriptions to clients
so LLMs know exactly what arguments to send and what structure to expect in return.

---

## 🧠 Realistic Workflow Example

This demonstrates a complete **MCP discovery and interaction** sequence using structured models.

---

### 1️⃣ Discovery (the LLM sees what exists)

```bash
curl -s http://localhost:8000/mcp/tools | jq
```

**Server response (simplified)**

```json
{
  "tools": [
    {
      "name": "save_contact",
      "description": "Insert or update a contact in the database.",
      "args": {
        "name": "string",
        "email": "EmailStr"
      },
      "returns": "SaveContactResult"
    }
  ]
}
```

➡️ The LLM now knows there is a `save_contact` tool with described fields and types.

---

### 2️⃣ Save a New Contact

```bash
curl -s -X POST http://localhost:8000/mcp/tools/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "save_contact",
    "args": {"name": "Alice", "email": "alice@example.com"}
  }' | jq
```

**Server response**

```json
{
  "contact": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "2025-10-26T12:00:00"
  }
}
```

The returned payload adheres to the **`SaveContactResult`** schema.

---

### 3️⃣ Retrieve All Contacts

```bash
curl -s http://localhost:8000/mcp/resources/contacts | jq
```

**Server response**

```json
{
  "contacts": [
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com",
      "created_at": "2025-10-26T12:00:00"
    }
  ]
}
```

The response matches the **`ListContactsResult`** model.

---

### 4️⃣ Generate a Summary via Prompt

```bash
curl -s -X POST http://localhost:8000/mcp/prompts/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "summarize",
    "inputs": {"text": "Alice and Bob collaborate on AI ethics projects."}
  }' | jq
```

**Server response**

```json
{
  "output": "Can you summarize this text: Alice and Bob collaborate on AI ethics projects."
}
```

The output follows the **`SummarizeResult`** model.

---

### 5️⃣ End-to-End LLM Cycle

| Step | Action     | Endpoint                                       | Pydantic Models                         | Purpose                  |
| ---- | ---------- | ---------------------------------------------- | --------------------------------------- | ------------------------ |
| 1    | Discovery  | `/mcp/tools`, `/mcp/resources`, `/mcp/prompts` | Model metadata (schema)                 | LLM learns what exists   |
| 2    | Execution  | `/mcp/tools/run`                               | `SaveContactArgs` → `SaveContactResult` | Save or update contact   |
| 3    | Retrieval  | `/mcp/resources/contacts`                      | `ListContactsResult`                    | Fetch stored contacts    |
| 4    | Generation | `/mcp/prompts/run`                             | `SummarizeArgs` → `SummarizeResult`     | Summarise arbitrary text |

---

## 🔍 How the LLM Sees the Server

When listing MCP capabilities, the LLM receives JSON metadata that looks like this:

```json
{
  "tools": [
    {
      "name": "save_contact",
      "description": "Insert or update a contact in the database.",
      "schema": {
        "properties": {
          "name": {"type": "string", "description": "Full name of the contact."},
          "email": {"type": "string", "format": "email", "description": "Unique e-mail address."}
        },
        "required": ["name", "email"]
      }
    }
  ],
  "resources": [
    {
      "uri": "data://contacts",
      "description": "List all contacts.",
      "schema": {
        "type": "array",
        "items": {"$ref": "#/definitions/Contact"}
      }
    }
  ],
  "prompts": [
    {
      "name": "summarize",
      "description": "Reusable template to summarise text input.",
      "schema": {
        "properties": {
          "text": {"type": "string", "description": "Arbitrary text to summarise."}
        },
        "required": ["text"]
      }
    }
  ]
}
```

Thus, the LLM or any other MCP client can dynamically **discover**, **render**, and **safely call** capabilities.

---

## 🔒 Why Pydantic + MCP Is Powerful

| Feature                      | Benefit                                                             |
| ---------------------------- | ------------------------------------------------------------------- |
| **Field-level descriptions** | Each argument and result property is clearly explained.             |
| **Validation & typing**      | Email formats, dates, and missing fields are automatically checked. |
| **Schema visibility**        | LLMs can view structured JSON schemas before execution.             |
| **Human-friendly discovery** | Exposed metadata enables transparent, self-documenting APIs.        |

Together, FastMCP and Pydantic make your server *both AI-interpretable and human-readable*.

---

## 🧰 Troubleshooting

| Problem                        | Likely Cause            | Resolution                               |
| ------------------------------ | ----------------------- | ---------------------------------------- |
| Health check fails             | Container not yet ready | Wait a few seconds or increase interval  |
| `curl: (7)` connection refused | Port not exposed        | Ensure `-p 8000:8000` or compose mapping |
| Database empty                 | First start             | Automatically initialised on startup     |
| Validation error               | Incorrect input type    | Check Pydantic field requirements        |

---

## 🧾 scripts/inspect.sh

The included script automatically:

1. Starts the container (if not running),
2. Checks health,
3. Lists all MCP endpoints with names and descriptions,
4. Demonstrates basic tool, resource, and prompt calls.

Run:

```bash
bash scripts/inspect.sh
```

---

## 📜 Licence

MIT © 2025 Antonio Lobo

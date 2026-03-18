# 🐍 GitHub Copilot Instructions for FastAPI Project

## Project Overview
This is a small RESTful API built with Python and the FastAPI framework. We prioritize clean, modern Python standards and clear separation of concerns.

## Tech Stack & Structure
* **Primary Language:** Python 3.10+
* **Framework:** FastAPI (with Uvicorn).
* **Dependency Manager:** uv (configured via pyproject.toml).
* **Data Models:** Pydantic models for all data validation and serialization.

## Mandatory Coding Guidelines (Copilot Context)
1.  **Asynchronous Code:** All route handlers and I/O-bound functions **must** be defined using `async def` and utilize `await`.
2.  **Type Hints:** All function signatures (parameters and return values) **must** use explicit, descriptive type hints.
3.  **Testing:** Any new endpoint or utility function **must** have a corresponding test in the `tests/` directory using `pytest` and `httpx.AsyncClient`.
4.  **Model Location:** All Pydantic data models **must** be placed in a dedicated `app/models.py` file.
5.  **Return Type:** API endpoints must return standard Python dicts/lists or Pydantic models, not f-strings or raw strings.

---

## Test Generation Guidelines

### Framework & Tools
* **Test runner:** `pytest` with `pytest-asyncio` for async test support.
* **HTTP client:** `httpx.AsyncClient` with `ASGITransport` for integration tests — never use `TestClient`.
* **Coverage:** Run with `uv run pytest --cov=app tests/` and aim for **≥ 85%** coverage on changed modules.

### Folder Structure
```
tests/
├── conftest.py          # Shared fixtures (app, client, auth_token, …)
├── unit/
│   └── test_<module>.py # Isolated unit tests (e.g. tests/unit/test_models.py)
└── integration/
    └── test_<module>.py # End-to-end endpoint tests (e.g. tests/integration/test_main.py)
```
* All test files **must** live inside `tests/`. Never create test files outside this directory.
* Unit tests go under `tests/unit/`, integration tests under `tests/integration/`.

### Naming Conventions
* **Files:** `test_<module>.py` — mirrors the source file being tested.
* **Functions:** `test_<target>_<expected_behavior>` — e.g. `test_log_task_returns_structured_response`, `test_generate_report_raises_on_empty_tasks`.

### Required Pytest Markers
* Mark every async test with `@pytest.mark.asyncio`.
* Mark every integration/endpoint test additionally with `@pytest.mark.integration`.

### Shared Fixtures (`tests/conftest.py`)
Always define and reuse these fixtures instead of duplicating setup code in each test:

    import pytest
    import pytest_asyncio
    from httpx import ASGITransport, AsyncClient
    from app.main import app

    @pytest_asyncio.fixture
    async def client() -> AsyncClient:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

### Integration Test Template
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_<endpoint>_<expected_behavior>(client: AsyncClient) -> None:
        response = await client.get("/<endpoint>")
        assert response.status_code == 200
        data = response.json()
        assert "expected_field" in data

### Unit Test Template
    def test_<function>_<expected_behavior>() -> None:
        result = my_function(valid_input)
        assert result == expected_output

    def test_<function>_raises_on_invalid_input() -> None:
        with pytest.raises(ValueError):
            my_function(None)

### Required Test Coverage per Endpoint / Function
For every endpoint or utility function, generate tests covering **all three** categories:
1. **Happy path** — valid input, expected status code and response shape.
2. **Validation errors** — invalid or missing fields (expect `422 Unprocessable Entity`).
3. **Failure / edge cases** — empty data sets, boundary values, unexpected states.

### Response Validation
* Assert both the HTTP status code **and** the JSON response structure.
* Validate response payloads against the Pydantic models defined in `app/models.py`.
* Use `assert set(expected_keys).issubset(data.keys())` to verify required fields without over-constraining.
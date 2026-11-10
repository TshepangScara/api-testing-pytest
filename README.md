# REST API Test Suite: Restful-Booker

Automated API tests for [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html), a public practice booking API. Built with **Python, requests and pytest**.

**Status:** in progress. Health check and authentication are covered (6 tests: 5 pass, 1 documented defect). Booking CRUD, schema validation and CI are next.

## Tech stack

| Area | Tools |
|---|---|
| Language | Python 3.13 |
| HTTP client | requests |
| Test runner | pytest |
| Planned | jsonschema (contract tests), pytest-html (reports), GitHub Actions (CI) |

## Test coverage

| Area | Endpoint | What is tested |
|---|---|---|
| Health check | `GET /ping` | API is up (201 Created) |
| Authentication | `POST /auth` | Valid credentials return a non-empty token |
| Authentication | `POST /auth` | Wrong password returns no token and the reason "Bad credentials" |
| Authentication | `POST /auth` | Wrong password should return 401 (documented defect, see below) |
| Fixtures | n/a | Session-scoped token is a valid string and is reused across tests |

## Defect found

| Endpoint | Expected | Actual |
|---|---|---|
| `POST /auth` with a wrong password | `401 Unauthorized` | `200 OK` with `{"reason": "Bad credentials"}` |

The test is marked `xfail(strict=True, raises=AssertionError)`:

- `strict=True`: if the API is fixed, the test unexpectedly passes and fails the run, so the marker gets removed.
- `raises=AssertionError`: only the failed status-code assertion counts as the known defect. A setup error (such as missing credentials) is reported as a real error, not hidden as the known bug.

## Design decisions

- **Fixtures in `conftest.py`.** `base_url`, `credentials` and `token` are shared by every test, so no URL or login logic is repeated.
- **Session scope for auth.** `token` is session-scoped, so the suite calls `/auth` once per run instead of once per test. Its dependencies are session-scoped too, which avoids a `ScopeMismatch`.
- **No secrets in code.** Credentials are read from environment variables. If they are missing, the `credentials` fixture fails with a clear message instead of a `KeyError`.
- **Positive and negative tests.** Each endpoint is tested with valid and invalid input, asserting on status codes and JSON bodies.

## Run it locally

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Restful-Booker's public practice credentials
$env:RB_USERNAME = "admin"
$env:RB_PASSWORD = "password123"

pytest -v
```

Expected result: `5 passed, 1 xfailed`.

## Project structure

```
api-testing-pytest/
├── requirements.txt
└── tests/
    ├── conftest.py       # base_url, credentials and session-scoped token fixtures
    ├── test_health.py    # GET /ping
    └── test_auth.py      # POST /auth, positive, negative and defect tests
```

## Roadmap

- [x] Health check
- [x] Authentication tests and session-scoped token fixture
- [ ] Booking CRUD: create, read, update (with token), delete (with token)
- [ ] Negative tests: invalid IDs, missing fields, no token
- [ ] JSON Schema validation of responses
- [ ] GitHub Actions CI with an HTML report

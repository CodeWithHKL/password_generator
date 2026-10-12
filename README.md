# Password Generator API

A small HTTP API that returns random passwords, passphrases and PINs. Built with FastAPI and deployed on Vercel as a single Python serverless function. All randomness comes from Python's `secrets` module, and nothing is stored or logged by the app.

## Endpoints

Every generator endpoint requires an `X-API-Key` header and returns `403` without a valid key. With `count` above 1, the response is a JSON array.

Response shape:

```json
{ "password": "k7Qm2vX9pRw4tZs8NeBd", "length": 20, "entropy_bits": 124.7 }
```

`entropy_bits` is an estimate.

### `GET /generate`

Random character passwords. Every enabled character set appears at least once.

| Parameter | Default | Notes |
|---|---|---|
| `length` | 16 | 8-128 |
| `count` | 1 | 1-50 |
| `lower`, `upper`, `digits`, `symbols` | `true` | Toggle each character set |
| `avoid_ambiguous` | `true` | Leaves out `O 0 l 1 I` |
| `exclude` | none | Up to 64 characters to leave out |

If no characters are left to choose from, the API returns `422`.

### `GET /generate_phrase`

Passphrases made of random words.

| Parameter | Default | Notes |
|---|---|---|
| `words` | 4 | 3-10 |
| `sep` | `-` | One character |
| `casing` | `title` | `lower`, `title`, `upper`, `random` |
| `digits` | 1 | 0-5 digits appended |
| `count` | 1 | 1-50 |

### `GET /generate_pin`

Numeric PINs.

| Parameter | Default | Notes |
|---|---|---|
| `length` | 6 | 4-12 |
| `count` | 1 | 1-50 |

### Other routes

- `/` is a short documentation page (`api/landing.html`).
- `/docs` is the interactive OpenAPI reference.

## Example

```bash
curl -H "X-API-Key: YOUR_KEY" "https://YOUR_DEPLOYMENT/generate?length=20&symbols=false"
```

## Run locally

From the project root. The code uses relative imports, so run it as the `api` package:

```bash
python -m pip install -r requirements.txt
export API_KEY=choose-a-key        # PowerShell: $env:API_KEY = "choose-a-key"
python -m uvicorn api.main:app --reload
```

Then open <http://127.0.0.1:8000>.

## Deploy on Vercel

`vercel.json` rewrites every path to `api/main.py`. Set the `API_KEY` environment variable in the Vercel project settings (Settings, then Environment Variables) and redeploy. If `API_KEY` is not set, every generator request is rejected.

## Project layout

```
api/
  main.py        FastAPI app and routes
  generator.py   Password, passphrase and PIN generation
  config.py      Limits, character sets, API key setting
  wordlist.py    Word list for passphrases
  landing.html   Documentation page served at /
vercel.json      Routes all requests to api/main.py
requirements.txt Pinned dependencies
```

## Notes

- Entropy for `/generate` is `length x log2(pool size)`. Guaranteeing one character from each enabled set makes this a slight overestimate.
- Responses from the `/generate*` routes are sent with `Cache-Control: no-store`.

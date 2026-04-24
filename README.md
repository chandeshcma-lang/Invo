# Invo — Invoice PDF to Excel (Self-Hosted)

Convert invoice PDF table data into downloadable Excel files from a browser UI.

## Features
- Upload PDF in browser.
- Extract machine-readable tables.
- Download `.xlsx` file.
- 20MB upload limit.
- Health endpoint for deployment checks: `/health`.

## Next steps to execute this

### 1) Run locally (fastest)
```bash
./scripts/run_local.sh
```

Then open:
- App: `http://localhost:8000`
- Health check: `http://localhost:8000/health`

### 2) Run with Docker
```bash
./scripts/run_docker.sh
```

Then open:
- App: `http://localhost:8000`
- Health check: `http://localhost:8000/health`

### 3) Deploy publicly on Render
1. Push this repo to your GitHub account.
2. In Render, select **New + → Blueprint**.
3. Pick this repo.
4. Render reads `render.yaml` and deploys.
5. After deploy, test:
   - `https://<your-service>.onrender.com/health`
   - `https://<your-service>.onrender.com/`

### 4) Validate PDF to Excel conversion
1. Open the app URL.
2. Upload one machine-readable invoice PDF.
3. Click **Convert to Excel**.
4. Confirm a file named like `<input>_converted.xlsx` downloads.

## Manual run commands

### Local Python mode
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Docker mode
```bash
docker compose up --build
```

## Temporary public URL (no cloud account)
```bash
python app.py
ssh -R 80:localhost:8000 nokey@localhost.run
```

## Notes
- Works best with machine-readable PDFs.
- Scanned/image-only PDFs often need OCR first.

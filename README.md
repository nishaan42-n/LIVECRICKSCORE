# Cricbuzz LiveStats

Flask dashboard starter with SQLite CRUD/SQL analytics and RapidAPI endpoints for live, upcoming, and recent matches.

## Setup (Windows / VS Code)
1. Extract this ZIP to a folder such as `D:\Cricbuzz_LiveStats_Project`.
2. Copy `.env.example` to `.env`. Add a **new** RapidAPI key from your RapidAPI dashboard. Do not share it or commit `.env`.
3. Open the folder in VS Code. In PowerShell run:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
4. Test API access:
   ```powershell
   python test_api.py
   ```
5. Start the dashboard:
   ```powershell
   python app.py
   ```
6. Open `http://127.0.0.1:5000`.

Alternatively, run `start_windows.bat` (Windows). If PowerShell blocks activation, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe test_api.py`.

## API endpoints
- `GET /matches/live`
- `GET /matches/upcoming`
- `GET /matches/recent`

API host header must be `crickbuzz-official-apis.p.rapidapi.com`. The client loads `.env` from the project root regardless of the current working directory.

## Troubleshooting
- `RAPIDAPI_KEY is missing`: make sure file is named exactly `.env` (not `.env.txt`), located beside `app.py`, and contains `RAPIDAPI_KEY=your_new_key` with no surrounding quotes.
- HTTP 401/403: check the selected RapidAPI application, subscription, key, and endpoint permissions.
- HTTP 429: wait for the rate limit reset or check your plan quota. Code cannot bypass provider limits.
- Keep API keys out of screenshots, source control, and chat. Rotate any key that was exposed.

## Scope notes
The project includes a local SQLite database and SQL analytics for match, player, innings, bowling, and partnership records. The live/upcoming API endpoints do not automatically populate the analytics database. Add or import source records before expecting historical statistics; empty query results mean the local database has no matching data. Existing databases are upgraded when the app starts without deleting player or match records.

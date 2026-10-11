# JalGuard AI — beginner starter

This is a working frontend-first MVP for Environmental Hacks. It has a responsive dashboard, weather trend, synthetic anomaly demo, evidence-based investigation screen, and what-if simulator.

## Data honesty
The bundled weather values are fallback/demo values. Run `python scripts/fetch_weather.py` to fetch real Open-Meteo historical data. Sensor rows are explicitly synthetic—not BattLeDIM measurements and not Pune incidents. Review any downloaded dataset's schema, date coverage, and licence before making claims.

## Requirements
- Node.js 20+ (LTS recommended)
- Python 3.10+ (optional, for weather script)
- VS Code, Git, GitHub account

## Run it locally (beginner steps)
1. Extract the ZIP.
2. Open the extracted `jalguard-ai-starter` folder in VS Code.
3. Click Terminal > New Terminal.
4. Run `cd frontend`
5. Run `npm install`
6. Run `npm run dev`
7. Open the localhost link printed in the terminal, usually `http://localhost:5173`.
8. Leave the terminal running. Stop the server with Ctrl+C.

## Fetch real weather (optional)
From the project root, run:
`python -m pip install -r requirements.txt`
then:
`python scripts/fetch_weather.py`

## Deploy to AWS Amplify Hosting
1. Push this folder to a public GitHub repository.
2. In AWS Console, open AWS Amplify and choose Deploy/Host web app.
3. Connect GitHub and select this repository.
4. Set the app root directory to `frontend`.
5. Build command: `npm run build`; output directory: `dist`.
6. Deploy and test the HTTPS URL in a private/incognito browser.
7. Check AWS billing and budget alerts. This starter needs no database, EC2, NAT Gateway, or hosted LLM.

## GitHub push (from project root)
`git init`
`git add .`
`git commit -m "Build JalGuard AI starter"`
`git branch -M main`
`git remote add origin https://github.com/YOUR-USERNAME/jalguard-ai.git`
`git push -u origin main`

Replace the URL with your own repository URL.

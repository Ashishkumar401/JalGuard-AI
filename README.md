# JalGuard AI

Live demo project- https://main.d3tvq4hm8oszdm.amplifyapp.com/

Explore how weather and water-network sensor readings can help an analyst investigate a possible anomaly. The React dashboard pairs a Pune weather view with synthetic sensor scenarios. A separate FastAPI service scores a supplied sensor reading using an experimental classifier.

## Explore the project

| Start here | What to look for |
| --- | --- |
| [Investigation logic](frontend/src/investigationEngine.js) | How the dashboard assembles evidence for a scenario |
| [Pune map](frontend/src/PuneFloodMap.jsx) | The geographic view used in the dashboard |
| [Prediction API](api.py) | Feature validation, model inference and the event probability returned to the caller |
| [Holdout results](baseline_file_holdout_results.csv) | Recorded evaluation results for the baseline experiment |

## Run the dashboard

From the repository root, with Node.js 20 or later installed:

```sh
cd frontend
npm ci
npm run dev
```

Open the local URL printed by Vite. Explore a synthetic anomaly, inspect its evidence and change the scenario in the simulator. To build the static site, run `npm run build` inside `frontend`. The build output is `dist`.

## Interpreting the data

The dashboard ships with fallback weather values. To refresh historical weather, install the Python dependencies from the root with `python -m pip install -r requirements.txt`, then run `python scripts/fetch_weather.py`. The example sensor records are synthetic. The classifier predicts research-dataset labels and has not been validated on a live water network. [Data sources and limitations](data/README.md)

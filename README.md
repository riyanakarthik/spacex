# SpaceX Launch Records Dashboard

An interactive Dash dashboard for exploring SpaceX launch outcomes by launch site and payload mass. The project focuses on clean data storytelling with a lightweight Python stack and is organized to be easy for recruiters, reviewers, and collaborators to run locally.

## Features

- Launch-site filter with an "All Launch Sites" overview
- Pie chart showing successful launches by site or success/failure breakdown for a selected site
- Payload range slider for narrowing the analysis window
- Scatter plot showing how payload mass relates to launch outcomes
- Clear in-app error handling if the dataset is missing or malformed
- Smoke tests to verify the app imports and the dataset loads correctly

## Tech Stack

- Python
- Dash
- Pandas
- Plotly
- Pytest

## Dataset and Attribution

The dashboard uses the `spacex_launch_dash.csv` dataset distributed as part of the IBM Applied Data Science Capstone materials. The included download helper pulls the file from IBM's public course-hosted dataset endpoint:

- Source file: `data/spacex_launch_dash.csv`
- Download script: `scripts/download_spacex_data.py`

## How to Run Locally

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Recommended Python version: 3.9+

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the dashboard:

```bash
python spacex_dash_app.py
```

4. Open the local URL shown in the terminal, usually `http://127.0.0.1:8050/`.

### Optional: Re-download the Dataset

If you remove the CSV or want to refresh it, run:

```bash
python scripts/download_spacex_data.py
```

### Optional: Enable Dash Debug Mode

Debug mode is controlled through an environment variable instead of being hardcoded:

```bash
DASH_DEBUG=1 python spacex_dash_app.py
```

## Running Tests

```bash
pytest
```

## Screenshots

Add project screenshots to the `screenshots/` folder and reference them here.

- Dashboard overview: `screenshots/dashboard-overview.png`
- Filtered site view: `screenshots/site-filter-view.png`

## Project Structure

```text
spacex/
├── archive/
│   ├── applied-ds-capstone-coursera.pdf
│   ├── firstchild.py
│   └── firstpython.py
├── data/
│   └── spacex_launch_dash.csv
├── notebooks/
│   ├── SpaceX_Machine Learning Prediction_Part_5 (1).ipynb
│   ├── edadataviz.ipynb
│   ├── jupyter-labs-eda-sql-coursera_sqllite.ipynb
│   ├── jupyter-labs-spacex-data-collection-api.ipynb
│   ├── jupyter-labs-webscraping.ipynb
│   ├── lab_jupyter_launch_site_location.ipynb
│   └── labs-jupyter-spacex-Data wrangling.ipynb
├── screenshots/
├── scripts/
│   └── download_spacex_data.py
├── tests/
│   └── test_smoke.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── spacex_dash_app.py
```

## Notes

- The main application lives in `spacex_dash_app.py`.
- Legacy notebooks and earlier course artifacts are preserved outside the root workflow so the repo stays focused on the dashboard project.

## Future Improvements

- Add additional filters for booster version, orbit, or launch year
- Deploy the app to a public hosting platform
- Add CI to run tests automatically on push
- Add richer annotations and summary metrics above the charts

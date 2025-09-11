# Copilot Instructions for Data_Science Workspace

## Overview
This workspace contains a variety of data science, machine learning, and web scraping projects, including Jupyter notebooks, Flask web apps, and data analysis scripts. The structure is modular, with each major project in its own subdirectory. Notable projects include a Flask-based review scraper and several exploratory data analysis (EDA) notebooks.

## Key Components & Architecture
- **api_tutorial/**: Python scripts for MongoDB and Flask API demos.
- **EDA/**: Jupyter notebooks for exploratory data analysis, using pandas, numpy, matplotlib, and seaborn.
- **Pandas/**: Notebooks and CSVs for pandas and numpy practice.
- **Statistics/**: Notebooks for statistical tests (t-test, ANOVA, correlation) with step-by-step markdown explanations.
- **Project_Flask_Python/ReviewFlask/ReviewFlask/**: Flask web app for scraping product reviews from Flipkart, saving to CSV, and displaying results in a styled HTML table.
  - `app.py`: Main Flask app, entry point for web scraping and UI.
  - `templates/`: Jinja2 HTML templates for search and results pages.
  - `requirements.txt`: Python dependencies for deployment and local dev.
  - `.github/workflows/main_scapper.yml`: GitHub Actions workflow for CI/CD to Azure Web App.

## Developer Workflows
- **Flask App (ReviewFlask)**:
  - Run locally: `python app.py` (ensure dependencies from `requirements.txt` are installed)
  - Deploy: Push to `main` branch triggers GitHub Actions workflow for Azure deployment
  - Main entry: `app.py` (uses environment variable `PORT`, defaults to 8000)
- **Jupyter Notebooks**:
  - Use for EDA, statistics, and pandas/numpy practice
  - Markdown explanations are placed before each code cell for clarity
- **CI/CD**:
  - Workflow file: `.github/workflows/main_scapper.yml`
  - Installs dependencies, runs optional tests, uploads artifact, and deploys to Azure

## Project-Specific Conventions
- **Web Scraping**:
  - User-Agent headers are set for all HTTP requests to avoid blocks
  - Scraped reviews are saved as CSV files named after the search query
  - Results are rendered using Jinja2 templates with DataTables for interactive tables
- **Notebooks**:
  - Markdown cells explain each code cell (what, why, formulas, graphing logic)
  - Use `%matplotlib inline` for inline plotting
- **Directory Structure**:
  - Each project is self-contained; avoid cross-project imports
  - Data files (CSVs, JSON) are stored alongside notebooks/scripts

## Integration & Dependencies
- **External Services**:
  - Azure Web App for Flask deployment (secrets managed via GitHub Actions)
- **Python Packages**:
  - See `requirements.txt` in each project for dependencies
  - Flask, Flask-Cors, requests, beautifulsoup4, pandas, numpy, matplotlib, seaborn, pymongo, etc.

## Examples
- To add a new Flask route, edit `app.py` and add a corresponding template in `templates/`.
- To add a new notebook, place it in the relevant directory (e.g., `EDA/`, `Statistics/`).
- To update CI/CD, edit `.github/workflows/main_scapper.yml`.

## Tips for AI Agents
- Always check for project-specific requirements in `requirements.txt` before running or deploying code.
- When editing notebooks, preserve the markdown/code cell structure for clarity.
- For web scraping, ensure headers mimic a real browser and handle exceptions gracefully.
- Use the modular directory structure to keep new scripts and data organized.

# Render Deployment Setup

This repository is ready for a Render Blueprint deployment once it is pushed to a Git remote.

## What is already prepared

- `render.yaml` defines two web services:
  - `mdl-ynor-api`
  - `mdl-ynor-dashboard`
- `requirements.txt` now resolves to an existing dependency file.
- The dashboard reads `YNOR_API_BASE_URL`.

## What you need to do next

1. Create a GitHub, GitLab, or Bitbucket repository.
2. Push this local repository to that remote.
3. In Render, create a new Blueprint from the repository.
4. After the services are created, verify the dashboard service has:
   - `YNOR_API_BASE_URL=https://mdl-ynor-api.onrender.com`

## Local sanity check

```powershell
uvicorn api_app:app --host 0.0.0.0 --port 8492
streamlit run 03_C_MOTEURS_ET_DEPLOIEMENT/01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/streamlit_dashboard.py
```

## Notes

- The API exposes corpus search, file preview, and node navigation.
- The dashboard is designed to consume the API and present a browsable corpus UI.

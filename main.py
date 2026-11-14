# -*- coding: utf-8 -*-
"""Streamlit App Root Entrypoint for Streamlit Cloud Deployment.
Enables seamless zero-config deployment on Streamlit Community Cloud (where default entrypoint is main.py).
"""
import os
import sys
from pathlib import Path
import runpy

# Ensure DEMO_MODE defaults to true for Streamlit Cloud deployment
if "DEMO_MODE" not in os.environ:
    os.environ["DEMO_MODE"] = "true"

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"
BACKEND_DIR = ROOT_DIR / "backend"
APP_DIR = BACKEND_DIR / "app"

for p in [str(FRONTEND_DIR), str(ROOT_DIR), str(BACKEND_DIR), str(APP_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

dashboard_script = FRONTEND_DIR / "dashboard.py"
runpy.run_path(str(dashboard_script), run_name="__main__")

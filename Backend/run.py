#!/usr/bin/env python3
"""
Script to run the FastAPI application.
This handles the import path correctly for running the app.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    # Use import string for proper reload support
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

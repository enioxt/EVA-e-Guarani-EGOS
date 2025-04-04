# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    .\venv\Scripts\Activate.ps1
}

# Install test dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing -v

# Open coverage report in browser
Start-Process ".\htmlcov\index.html"

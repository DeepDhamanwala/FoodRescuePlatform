# Testing Guide

## Backend Tests (Python/pytest)

The backend uses pytest for testing. Since the backend requires Python 3.11 and your system has Python 3.14, you have two options:

### Option 1: Run tests in Docker (Recommended)
```bash
./run-backend-tests.sh
```

This script runs tests in a Python 3.11 container with access to the database and Redis services.

### Option 2: Install Python 3.11 locally
If you want to run tests locally outside Docker:
```bash
# Install Python 3.11 (method depends on your OS)
# Then:
cd backend
poetry env use python3.11
poetry install
poetry run pytest -v
```

## Frontend Tests (JavaScript/vitest)

The frontend uses vitest for testing.

```bash
cd frontend
npm run test              # Run tests in watch mode
npm run test -- --run     # Run tests once
npm run test:coverage     # Run tests with coverage
```

### Test Files
- Frontend tests go in `src/` with `.test.tsx` or `.spec.tsx` extensions
- Backend tests go in `tests/` with `test_*.py` naming

## Current Status
- ✅ Frontend test infrastructure configured (vitest, @testing-library/react)
- ✅ Backend test infrastructure exists (pytest, pytest-asyncio)
- ⚠️ Backend tests require fixtures to be implemented (see `tests/fixtures/seed.py`)
- ⚠️ Integration tests exist but need fixture implementation to run

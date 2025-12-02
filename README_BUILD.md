Build and Run
--------------

This project provides simple Make targets and a build script to create a runnable artifact.

Prerequisites
- Python 3.8+ installed

Common commands
- Create a virtualenv and install dependencies:

  ```bash
  make install
  ```

- Build a runnable zipapp (creates `dist/flux_depth_generator.pyz`):

  ```bash
  make build
  ```

- Run the project locally (inside the virtualenv created by `make install`):

  ```bash
  source .venv/bin/activate
  # Preferred: run the Streamlit server
  streamlit run app.py
  # Or (less common) run directly with Python
  # python app.py
  ```

- Run the built zipapp directly (no venv required, but dependencies must be available):

  ```bash
  python dist/flux_depth_generator.pyz
  ```

Notes
- The build produces a zipapp that uses `app:main` as the entry point. The top-level `app.py` defines a `main()` function which starts the Streamlit app.
- For development, prefer `make install` and `make run` so dependencies are isolated in `.venv`.

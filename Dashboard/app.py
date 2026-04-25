from pathlib import Path
import runpy


APP_MAIN = Path(__file__).resolve().parents[1] / "app" / "main.py"

runpy.run_path(str(APP_MAIN), run_name="__main__")

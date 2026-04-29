from pathlib import Path
import sys

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.pipeline import DEFAULT_T1_PATH, DEFAULT_T2_PATH, OUTPUT_DIR, load_metrics, run_analysis


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}

app = FastAPI(title="GeoVision API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _save_upload(upload: UploadFile, target_path: Path) -> None:
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG, JPEG, TIF, and TIFF satellite images are supported.",
        )

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("wb") as file:
        file.write(upload.file.read())


def _with_urls(metrics):
    if not metrics:
        return None

    normalized = dict(metrics)
    paths = normalized.get("paths", {})
    normalized["urls"] = {
        key: f"/api/files/{Path(value).as_posix()}"
        for key, value in paths.items()
        if key in {"t1", "t2", "detect_t1", "detect_t2", "fusion", "heatmap"}
    }
    return normalized


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "GeoVision API"}


@app.get("/api/metrics")
def metrics():
    return {"metrics": _with_urls(load_metrics())}


@app.post("/api/analyze")
def analyze(
    t1: UploadFile = File(...),
    t2: UploadFile = File(...),
    confidence: float = Form(0.6),
    iou_threshold: float = Form(0.3),
):
    if not 0.1 <= confidence <= 0.95:
        raise HTTPException(status_code=400, detail="Confidence must be between 0.10 and 0.95.")
    if not 0.1 <= iou_threshold <= 0.8:
        raise HTTPException(status_code=400, detail="Matching sensitivity must be between 0.10 and 0.80.")

    _save_upload(t1, DEFAULT_T1_PATH)
    _save_upload(t2, DEFAULT_T2_PATH)

    try:
        result = run_analysis(
            DEFAULT_T1_PATH,
            DEFAULT_T2_PATH,
            confidence=confidence,
            iou_threshold=iou_threshold,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc

    return {"metrics": _with_urls(result)}


@app.get("/api/files/{relative_path:path}")
def files(relative_path: str):
    requested_path = (PROJECT_ROOT / relative_path).resolve()
    output_root = OUTPUT_DIR.resolve()
    data_root = (PROJECT_ROOT / "data").resolve()

    if not (
        requested_path == output_root
        or requested_path == data_root
        or output_root in requested_path.parents
        or data_root in requested_path.parents
    ):
        raise HTTPException(status_code=403, detail="File access is restricted to generated outputs.")

    if not requested_path.exists() or not requested_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(requested_path)

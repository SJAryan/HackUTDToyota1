# extract_toyota.py
import os, json
from dotenv import load_dotenv
from typing import Dict, Any

# Firecrawl import (support both variants)
try:
    from firecrawl import Firecrawl
    FCClient = Firecrawl
except Exception:
    from firecrawl.firecrawl import FirecrawlApp as FCClient  # type: ignore

load_dotenv()
API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY missing in .env")

app = FCClient(api_key=API_KEY)

ALL_VEHICLES_URL = "https://www.toyota.com/all-vehicles/"
OUT_DIR = "data"
OUT_PATH = os.path.join(OUT_DIR, "vehicle_listings.json")

# ---------- helpers ----------
def obj_to_dict(x: Any) -> Dict[str, Any]:
    """Best-effort convert Firecrawl SDK result (dict or Pydantic model) to plain dict."""
    if isinstance(x, dict):
        return x
    # pydantic v2
    for m in ("model_dump", "dict"):
        if hasattr(x, m):
            try:
                return getattr(x, m)()
            except Exception:
                pass
    # last resort: collect public attrs
    d = {}
    for a in dir(x):
        if a.startswith("_"):
            continue
        try:
            v = getattr(x, a)
        except Exception:
            continue
        if callable(v):
            continue
        d[a] = v
    return d


def pick(d: Dict[str, Any], *keys: str) -> Any:
    """Return the first present key from dict-like."""
    for k in keys:
        if isinstance(d, dict) and k in d:
            return d[k]
    return None

# ---------- main function ----------
def extract_all_models():
    print(f"🔎 Scraping {ALL_VEHICLES_URL} for all models...")

    # A single, powerful prompt to get all models at once
    prompt = (
        "Extract all car models listed on the page. "
        "Return ONLY a single JSON object with a key 'models'. "
        "'models' should be an array of objects. Each object should have: "
        "'model_name' (string) and 'url' (string, the full absolute URL to the model page)."
    )
    
    fmts = [{"type": "json", "prompt": prompt}]

    try:
        # This is the ONLY API call you need
        raw_scrape_data = app.scrape(ALL_VEHICLES_URL, formats=fmts)
        
        # Convert Pydantic model (if any) to a plain dict
        raw_data = obj_to_dict(raw_scrape_data)

        # Handle different possible return structures
        data = pick(raw_data, "data", "json")
        if 'json' in data: # Check if 'json' is nested inside 'data'
            data = pick(data, "json")
        
        if not data or 'models' not in data or not isinstance(data.get('models'), list):
            print("❌ AI prompt failed. 'models' array not found in JSON.")
            print(f"Received data: {json.dumps(data, indent=2)}")
            return

        models = data['models']
        
        # Save the result
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(models, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 ✅ Success! Saved {len(models)} models to {OUT_PATH}")
        print("Here's a sample:")
        for model in models[:5]:
            print(f"  - {model.get('model_name')}: {model.get('url')}")

    except Exception as e:
        print(f"❌ An error occurred during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    extract_all_models()
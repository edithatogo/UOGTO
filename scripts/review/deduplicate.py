import json
import os
import re
import sys

RAW_FILE = "data/raw/search_results.json"
OUT_DIR = "data/processed"
OUT_FILE = os.path.join(OUT_DIR, "deduplicated_results.json")

def normalize_title(title):
    if not title:
        return ""
    # Lowercase, remove non-alphanumeric, and strip excess whitespace
    normalized = title.lower()
    normalized = re.sub(r"[^a-z0-9]", "", normalized)
    return normalized

def deduplicate(records):
    seen_dois = set()
    seen_titles = set()
    deduped = []
    
    for r in records:
        doi = r.get("doi")
        title = r.get("title", "")
        norm_title = normalize_title(title)
        
        # Check if already seen
        if doi:
            # Normalize DOI (e.g. resolve lower/upper case difference)
            clean_doi = doi.strip().lower()
            if clean_doi in seen_dois:
                continue
            seen_dois.add(clean_doi)
            
        if norm_title:
            if norm_title in seen_titles:
                continue
            seen_titles.add(norm_title)
            
        deduped.append(r)
        
    return deduped

def main():
    print("Starting record deduplication...")
    if not os.path.exists(RAW_FILE):
        print(f"Raw search results not found at {RAW_FILE}. Please run query script first.", file=sys.stderr)
        sys.exit(1)
        
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    print(f"Total raw records loaded: {len(records)}")
    deduped = deduplicate(records)
    print(f"Deduplicated records remaining: {len(deduped)} (removed {len(records) - len(deduped)} duplicates)")
    
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2)
        
    print(f"Saved deduplicated records to {OUT_FILE}")

if __name__ == "__main__":
    main()

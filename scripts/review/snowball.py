import urllib.request
import urllib.parse
import json
import os
import sys

INPUT_FILE = "data/processed/screened_results.json"
OUTPUT_FILE = "data/processed/snowballed_results.json"

def fetch_url(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "UOGTO-Scoping-Review-Agent/1.0 (mailto:uogto@example.org)"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def fetch_citations(work_id, direction="referenced_works", limit=5):
    # work_id example: "https://openalex.org/W2112345"
    if not work_id:
        return []
    clean_id = work_id.replace("https://openalex.org/", "")
    
    if direction == "referenced_works":
        url = f"https://api.openalex.org/works/{clean_id}"
        data = fetch_url(url)
        if not data:
            return []
        try:
            res = json.loads(data.decode("utf-8"))
            # Fetch details for referenced work IDs
            ref_ids = res.get("referenced_works", [])[:limit]
            results = []
            for ref_id in ref_ids:
                ref_clean = ref_id.replace("https://openalex.org/", "")
                ref_data = fetch_url(f"https://api.openalex.org/works/{ref_clean}")
                if ref_data:
                    work = json.loads(ref_data.decode("utf-8"))
                    results.append({
                        "source": "openalex-snowball",
                        "id": work.get("id"),
                        "doi": work.get("doi"),
                        "title": work.get("title"),
                        "abstract": None,
                        "authors": [a.get("author", {}).get("display_name") for a in work.get("authorships", [])],
                        "year": work.get("publication_year"),
                        "url": work.get("doi") or work.get("id")
                    })
            return results
        except Exception:
            return []
    return []

def main():
    print("Executing backward citation snowballing...")
    if not os.path.exists(INPUT_FILE):
        print(f"Screened results file not found at {INPUT_FILE}.", file=sys.stderr)
        sys.exit(1)
        
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    print(f"Loaded {len(records)} screened seed records.")
    
    # Run snowballing on top 2 records to keep speed high and avoid rate limits
    expanded = list(records)
    for r in records[:2]:
        openalex_id = r.get("id")
        if openalex_id and "openalex" in openalex_id:
            print(f"Fetching references for: {r.get('title')}")
            refs = fetch_citations(openalex_id, limit=2)
            print(f"Found {len(refs)} references.")
            expanded.extend(refs)
            
    # Deduplicate expanded list
    seen = set()
    unique_expanded = []
    for item in expanded:
        title = item.get("title", "").strip().lower()
        if title not in seen:
            seen.add(title)
            unique_expanded.append(item)
            
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_expanded, f, indent=2)
        
    print(f"Snowballing complete. Total unique records: {len(unique_expanded)} (saved to {OUTPUT_FILE})")

if __name__ == "__main__":
    main()

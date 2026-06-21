import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os
import sys

RAW_DATA_DIR = "data/raw"

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

def query_openalex(query_str, limit=50):
    print("Querying OpenAlex...")
    escaped = urllib.parse.quote(query_str)
    url = f"https://api.openalex.org/works?search={escaped}&per_page={limit}"
    data = fetch_url(url)
    if not data:
        return []
    
    try:
        res = json.loads(data.decode("utf-8"))
        results = []
        for work in res.get("results", []):
            results.append({
                "source": "openalex",
                "id": work.get("id"),
                "doi": work.get("doi"),
                "title": work.get("title"),
                "abstract": work.get("abstract"), # OpenAlex uses inverted index, we will parse in downstream
                "authors": [a.get("author", {}).get("display_name") for a in work.get("authorships", [])],
                "year": work.get("publication_year"),
                "url": work.get("doi") or work.get("id")
            })
        return results
    except Exception as e:
        print(f"OpenAlex parse error: {e}", file=sys.stderr)
        return []

def query_europepmc(query_str, limit=50):
    print("Querying Europe PMC...")
    escaped = urllib.parse.quote(query_str)
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={escaped}&format=json&pageSize={limit}"
    data = fetch_url(url)
    if not data:
        return []
    
    try:
        res = json.loads(data.decode("utf-8"))
        results = []
        for paper in res.get("resultList", {}).get("result", []):
            results.append({
                "source": "europepmc",
                "id": paper.get("id"),
                "doi": paper.get("doi"),
                "title": paper.get("title"),
                "abstract": paper.get("abstractText"),
                "authors": [a.get("fullName") for a in paper.get("authorList", {}).get("author", [])],
                "year": paper.get("pubYear"),
                "url": f"https://europepmc.org/article/MED/{paper.get('id')}"
            })
        return results
    except Exception as e:
        print(f"Europe PMC parse error: {e}", file=sys.stderr)
        return []

def query_arxiv(query_str, limit=50):
    print("Querying arXiv...")
    # Map simple query terms for arXiv
    escaped = urllib.parse.quote(query_str)
    url = f"http://export.arxiv.org/api/query?search_query=all:{escaped}&max_results={limit}"
    data = fetch_url(url)
    if not data:
        return []
    
    try:
        root = ET.fromstring(data)
        results = []
        # Namespaces
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            id_val = entry.find("atom:id", ns)
            published = entry.find("atom:published", ns)
            
            authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            year = published.text[:4] if published is not None else None
            
            results.append({
                "source": "arxiv",
                "id": id_val.text if id_val is not None else None,
                "doi": None,
                "title": title.text.strip().replace("\n", " ") if title is not None else None,
                "abstract": summary.text.strip() if summary is not None else None,
                "authors": authors,
                "year": year,
                "url": id_val.text if id_val is not None else None
            })
        return results
    except Exception as e:
        print(f"arXiv parse error: {e}", file=sys.stderr)
        return []

def query_crossref(query_str, limit=50):
    print("Querying Crossref...")
    escaped = urllib.parse.quote(query_str)
    url = f"https://api.crossref.org/works?query={escaped}&rows={limit}"
    data = fetch_url(url)
    if not data:
        return []
    
    try:
        res = json.loads(data.decode("utf-8"))
        results = []
        for item in res.get("message", {}).get("items", []):
            title = item.get("title", [None])[0]
            year = item.get("published-print", {}).get("date-parts", [[None]])[0][0]
            if not year:
                year = item.get("published-online", {}).get("date-parts", [[None]])[0][0]
            
            results.append({
                "source": "crossref",
                "id": item.get("DOI"),
                "doi": item.get("DOI"),
                "title": title,
                "abstract": item.get("abstract"),
                "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in item.get("author", [])],
                "year": year,
                "url": item.get("URL")
            })
        return results
    except Exception as e:
        print(f"Crossref parse error: {e}", file=sys.stderr)
        return []

def main():
    query_term = '"game theory" AND (payoff OR utility)'
    limit = 10
    
    # Allow override via command line
    if len(sys.argv) > 1:
        query_term = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
        except ValueError:
            pass
            
    print(f"Starting literature search for: '{query_term}' (limit={limit} per database)")
    
    all_results = []
    all_results.extend(query_openalex(query_term, limit))
    all_results.extend(query_europepmc(query_term, limit))
    all_results.extend(query_arxiv(query_term, limit))
    all_results.extend(query_crossref(query_term, limit))
    
    # Save results
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    out_path = os.path.join(RAW_DATA_DIR, "search_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
        
    print(f"Successfully downloaded {len(all_results)} papers to {out_path}")

if __name__ == "__main__":
    main()

import os
import glob
from rdflib import Graph
from pyshacl import validate as shacl_validate

def generate_html_report(output_path="validation_report.html"):
    print("Generating HTML SHACL Validation report...")
    
    # 1. Load ontology files
    g = Graph()
    ttl_files = sorted(glob.glob("ontologies/**/*.ttl", recursive=True))
    for ttl in ttl_files:
        g.parse(ttl, format="turtle")
            
    # 2. Parse SHACL files
    shacl_g = Graph()
    shacl_files = sorted(glob.glob("shapes/*.ttl"))
    for shacl in shacl_files:
        shacl_g.parse(shacl, format="turtle")

    # 3. Validate examples with SHACL
    example_files = sorted(glob.glob("examples/*"))
    
    rows = ""
    for ex in example_files:
        ex_g = Graph()
        fmt = "turtle" if ex.endswith(".ttl") else "json-ld"
        ex_g.parse(ex, format=fmt)
            
        combined = g + ex_g
        conforms, results_graph, results_text = shacl_validate(
            combined,
            shacl_graph=shacl_g,
            ont_graph=g,
            inference='rdfs'
        )
        
        status_color = "#28a745" if conforms else "#dc3545"
        status_text = "Conforms" if conforms else "Violation"
        details = "All shapes matched perfectly." if conforms else results_text.replace('\n', '<br>')
        
        rows += f"""
        <tr>
            <td>{os.path.basename(ex)}</td>
            <td>{fmt}</td>
            <td style="color: white; background-color: {status_color}; font-weight: bold; text-align: center;">{status_text}</td>
            <td><code>{details}</code></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>UOGTO SHACL Validation Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; margin: 40px; background-color: #f6f8fa; color: #24292e; }}
        h1 {{ border-bottom: 1px solid #e1e4e8; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; background: white; border: 1px solid #e1e4e8; }}
        th, td {{ border: 1px solid #e1e4e8; padding: 12px; text-align: left; }}
        th {{ background-color: #f6f8fa; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>UOGTO SHACL Validation Report</h1>
    <p>This report documents the ontological validation results for example game instances checked against constraints defined in the UOGTO repository shapes directory.</p>
    <table>
        <thead>
            <tr>
                <th>Example File</th>
                <th>Format</th>
                <th>Status</th>
                <th>Details / Violation Logs</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Validation report written to: {output_path}")

if __name__ == "__main__":
    generate_html_report()

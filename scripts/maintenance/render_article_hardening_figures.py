"""Render article-hardening PRISMA figures as SVG and PDF assets."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / "docs" / "article-hardening" / "figures"

FIGURE_SPECS = [
    {
        "stem": "prisma-2020-source-discovery-flow",
        "title": "PRISMA 2020-style source discovery flow",
        "caption": "Search routes, identified records, normalization, inventory capture, inclusion, and negative-evidence recording for UOGTO source discovery.",
        "boxes": [
            ("Search routes recorded\nin search-log.jsonl\nn=7", 70, 95),
            ("Records identified\nacross all routes\nn=39", 70, 215),
            ("Records normalized\nfor screening\nn=39", 70, 335),
            ("Source candidates in\nsource-extension-inventory.json\nn=39", 405, 335),
            ("Included source-family\nentries\nn=39", 740, 335),
            ("Negative-evidence route\nrecorded separately\nn=1", 405, 95),
        ],
        "arrows": [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5)],
        "dashed": {(0, 5)},
    },
    {
        "stem": "prisma-2020-screening-flow",
        "title": "PRISMA 2020-style screening flow",
        "caption": "Screening, inclusion, exclusion, and negative-evidence disposition for the UOGTO article-hardening source register.",
        "boxes": [
            ("Candidate sources in\nsource-extension-inventory.json\nn=39", 70, 120),
            ("Screened against\ninclusion criteria\nn=39", 405, 120),
            ("Included in evidence\npackage\nn=39", 740, 120),
            ("Excluded after\nscreening\nn=0", 740, 305),
            ("Negative-evidence search\nroute recorded separately\nn=1", 405, 305),
        ],
        "arrows": [(0, 1), (1, 2), (1, 3), (0, 4)],
        "dashed": {(0, 4)},
    },
]

WIDTH = 1040
HEIGHT = 560
BOX_W = 230
BOX_H = 82
BLUE = "#0072B2"
GREEN = "#009E73"
GOLD = "#E69F00"
RED = "#D55E00"
SLATE = "#334155"
LIGHT = "#F8FAFC"


def svg_text_lines(text: str, x: int, y: int, size: int = 15, fill: str = SLATE) -> str:
    lines = text.split("\n")
    spans = []
    for idx, line in enumerate(lines):
        spans.append(f'<tspan x="{x}" dy="{0 if idx == 0 else size + 4}">{line}</tspan>')
    return f'<text x="{x}" y="{y}" font-size="{size}" font-family="Arial,Helvetica,sans-serif" fill="{fill}">' + "".join(spans) + "</text>"


def render_svg(spec: dict) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{spec["title"]}</title>',
        f'<desc id="desc">{spec["caption"]}</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="42" y="42" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="700" fill="{SLATE}">{spec["title"]}</text>',
        f'<text x="42" y="72" font-family="Arial,Helvetica,sans-serif" font-size="14" fill="#475569">{spec["caption"]}</text>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#475569"/></marker></defs>',
    ]
    centers = []
    for idx, (label, x, y) in enumerate(spec["boxes"]):
        fill = GREEN if "Included" in label else (RED if "Excluded" in label else (GOLD if "Negative" in label else LIGHT))
        stroke = GREEN if fill == GREEN else (RED if fill == RED else (GOLD if fill == GOLD else BLUE))
        text_fill = "#ffffff" if fill in {GREEN, RED, GOLD} else SLATE
        parts.append(f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        parts.append(svg_text_lines(label, x + 16, y + 27, 14, text_fill))
        centers.append((x + BOX_W / 2, y + BOX_H / 2))
    for left, right in spec["arrows"]:
        x1, y1 = centers[left]
        x2, y2 = centers[right]
        dash = ' stroke-dasharray="7 5"' if (left, right) in spec["dashed"] else ""
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"{dash}/>'.replace('" stroke-dasharray', ' stroke-dasharray'))
    parts.append(f'<text x="42" y="520" font-family="Arial,Helvetica,sans-serif" font-size="13" fill="#64748B">PDF export is generated from the same structured figure specification for PDFLaTeX-safe manuscript packaging.</text>')
    parts.append("</svg>\n")
    return "\n".join(parts)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def pdf_stream(spec: dict) -> str:
    cmds = ["1 1 1 rg 0 0 1040 560 re f", "0.2 0.25 0.32 rg /F1 20 Tf 42 520 Td ({}) Tj".format(pdf_escape(spec["title"]))]
    cmds.append("/F1 10 Tf 42 492 Td ({}) Tj".format(pdf_escape(spec["caption"][:130])))
    for label, x, y in spec["boxes"]:
        pdf_y = HEIGHT - y - BOX_H
        cmds.append("0.95 0.97 0.99 rg {} {} {} {} re f".format(x, pdf_y, BOX_W, BOX_H))
        cmds.append("0.0 0.45 0.70 RG {} {} {} {} re S".format(x, pdf_y, BOX_W, BOX_H))
        lines = label.split("\n")
        for i, line in enumerate(lines):
            cmds.append("0.1 0.15 0.2 rg /F1 11 Tf {} {} Td ({}) Tj".format(x + 14, pdf_y + BOX_H - 26 - i * 16, pdf_escape(line)))
    for left, right in spec["arrows"]:
        x1 = spec["boxes"][left][1] + BOX_W / 2
        y1 = HEIGHT - (spec["boxes"][left][2] + BOX_H / 2)
        x2 = spec["boxes"][right][1] + BOX_W / 2
        y2 = HEIGHT - (spec["boxes"][right][2] + BOX_H / 2)
        cmds.append("0.3 0.36 0.44 RG 2 w {} {} m {} {} l S".format(x1, y1, x2, y2))
    return "BT\n" + "\n".join([c for c in cmds if " re " not in c and " m " not in c]) + "\nET\n" + "\n".join([c for c in cmds if " re " in c or " m " in c])


def write_pdf(path: Path, spec: dict) -> None:
    stream = pdf_stream(spec).encode("latin-1", errors="replace")
    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 1040 560] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>")
    objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("ascii") + obj + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode("ascii")
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode("ascii")
    out += f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    path.write_bytes(out)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    for spec in FIGURE_SPECS:
        svg_path = FIGURES / f"{spec['stem']}.svg"
        pdf_path = FIGURES / f"{spec['stem']}.pdf"
        svg_path.write_text(render_svg(spec), encoding="utf-8")
        write_pdf(pdf_path, spec)
    readme = FIGURES / "README.md"
    readme.write_text(
        "# Figures\n\n"
        "This directory holds article-hardening figures, including PRISMA 2020-style flow diagrams for source discovery and screening.\n\n"
        "- `prisma-2020-source-discovery-flow.md`\n"
        "- `prisma-2020-source-discovery-flow.svg`\n"
        "- `prisma-2020-source-discovery-flow.pdf`\n"
        "- `prisma-2020-screening-flow.md`\n"
        "- `prisma-2020-screening-flow.svg`\n"
        "- `prisma-2020-screening-flow.pdf`\n\n"
        "The SVG and PDF exports are generated from `scripts/maintenance/render_article_hardening_figures.py`. The PDF files are intended as PDFLaTeX-compatible manuscript assets.\n",
        encoding="utf-8",
    )
    print("Rendered 2 PRISMA figure SVG/PDF pairs.")


if __name__ == "__main__":
    main()

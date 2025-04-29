import markdown2, uuid
from pathlib import Path
from datetime import date
from typing import List, Dict

def itinerary_to_md(trip_name: str,
                    start: date,
                    days: List[Dict]) -> str:
    """
    days = [
      {"date": date(2025,5,1),
       "items":[{"time":"10:00","place":"Café Frischhut","transport":"Walk"}, ...]},
      ...
    ]
    """
    md = [f"# 🧳 {trip_name}", ""]
    md.append(f"**Start – End:** {start} – {start + len(days)-1}  \n")
    for d in days:
        md += ["---", f"## 📅 {d['date']}"]
        for it in d["items"]:
            md += [f"### {it['time']}  \n📍 **{it['place']}**  ",
                   f"🚗 _{it['transport']}_  ", ""]
    return "\n".join(md)

def save_md(md: str, out_dir="reports") -> Path:
    Path(out_dir).mkdir(exist_ok=True)
    file_path = Path(out_dir) / f"{uuid.uuid4().hex[:8]}.md"
    file_path.write_text(md, encoding="utf-8")
    return file_path

# PDF interface
def md_to_pdf(md_file: Path) -> Path:
    try:
        from weasyprint import HTML
    except ImportError:
        raise RuntimeError("WeasyPrint not installed; please run `pip install weasyprint` first")
    html = markdown2.markdown(md_file.read_text(encoding="utf-8"))
    pdf_path = md_file.with_suffix(".pdf")
    HTML(string=html).write_pdf(str(pdf_path))
    return pdf_path

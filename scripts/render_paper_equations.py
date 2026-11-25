"""Render the five equations used by the paper from explicitly specified LaTeX.
Generated PNGs are intended for embedding in Google Docs; original LaTeX is
kept below for reproducibility.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextParser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper_equations"
OUT.mkdir(exist_ok=True)

equations = [
    ("eq01_ghi_persistence.png", r"$\widehat{\mathrm{GHI}}_{t+5} = \mathrm{GHI}_{t}$"),
    ("eq02_pv_power.png", r"$P(V) = V \times I(V)$"),
    ("eq03_gmpp.png", r"$V_{\mathrm{GMPP}} = \mathrm{arg\,max}_{V}\,P(V)$"),
    ("eq04_shading.png", r"$G_{j}(t+h) = s_{j}\times\widehat{G}(t+h)$"),
    ("eq05_efficiency.png", r"$\eta_{\mathrm{MPPT}} = \frac{\sum_{k} P_{\mathrm{tracked},k}}{\sum_{k} P_{\mathrm{GMPP},k}}\times100\%$"),
]
plt.rcParams.update({"mathtext.fontset": "stix", "font.family":"STIXGeneral"})
MathTextParser("agg")
manifest=[]
for name, latex in equations:
    fig=plt.figure(figsize=(6, 1.0 if "efficiency" not in name else 1.5),dpi=220, facecolor="white")
    fig.text(0.5, 0.5, latex, fontsize=20, ha="center", va="center", color="black")
    file=OUT/name
    fig.savefig(file, dpi=220, bbox_inches="tight", pad_inches=0.10, facecolor="white")
    plt.close(fig)
    from PIL import Image
    with Image.open(file) as im:
        w,h=im.size
    manifest.append({"name":name,"latex":latex,"width_px":w,"height_px":h})
    print(name,w,h)
(OUT/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")

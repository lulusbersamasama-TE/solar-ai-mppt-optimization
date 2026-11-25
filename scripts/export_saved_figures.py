"""Extract the exact rendered PNG outputs from the saved Notebook 04 (no recomputation)."""
import base64
import json
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
notebook = repo / "notebooks" / "04_verification_and_sensitivity.ipynb"
obj = json.loads(notebook.read_text(encoding="utf-8"))
matches = {
    "verification_voltage_vs_power_loss.png": "fig_01_voltage_vs_power_loss.png",
    "verification_transient_forecast.png": "fig_02_transient_forecast.png",
    "verification_po_sensitivity_heatmap.png": "fig_03_po_sensitivity_heatmap.png",
}
indices={6:"fig_01_voltage_vs_power_loss.png",10:"fig_02_transient_forecast.png",12:"fig_03_po_sensitivity_heatmap.png"}
dest=repo/"paper_figures"
dest.mkdir(exist_ok=True)
for idx,name in indices.items():
    cell=obj["cells"][idx]
    outputs=[o for o in cell.get("outputs",[]) if "image/png" in o.get("data",{})]
    assert len(outputs)==1, f"Expected one PNG in cell {idx}"
    raw=outputs[0]["data"]["image/png"]
    data=base64.b64decode("".join(raw) if isinstance(raw,list) else raw)
    assert data[:8]==b"\x89PNG\r\n\x1a\n", "Invalid PNG"
    path=dest/name
    path.write_bytes(data)
    print(path.relative_to(repo),len(data),"bytes")

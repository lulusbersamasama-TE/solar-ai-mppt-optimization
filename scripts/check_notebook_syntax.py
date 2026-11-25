"""Static checks: notebook JSON and Python syntax. Does NOT execute data-science experiments."""
import ast
import json
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
paths = sorted((repo / "notebooks").glob("*.ipynb"))
assert len(paths) >= 4, "Expected four research notebooks"
issues = []
for path in paths:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook.get("nbformat") == 4, f"Invalid nbformat: {path.name}"
    code_count = 0
    for i, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        code_count += 1
        source = cell["source"]
        code = "".join(source) if isinstance(source, list) else source
        try:
            ast.parse(code, filename=f"{path.name}:cell{i}")
        except SyntaxError as exc:
            issues.append(str(exc))
    print(f"{path.name}: {code_count} syntactically valid code cells")
if issues:
    raise SystemExit("Static notebook failures:\n" + "\n".join(issues))
print("NOTE: Data-dependent and numerical verification requires Google Colab Run all.")

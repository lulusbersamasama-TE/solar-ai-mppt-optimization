"""Small synthetic numerical smoke tests of the controller function extracted
from Notebook 04. This DOES NOT evaluate trained models, user datasets,
converter dynamics or real MPPT performance.
"""
import ast
import json
from pathlib import Path

import numpy as np

notebook = Path(__file__).resolve().parents[1] / "notebooks" / "04_verification_and_sensitivity.ipynb"
cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
func = None
for cell in cells:
    if cell["cell_type"] != "code":
        continue
    code = cell["source"]
    code = "".join(code) if isinstance(code, list) else code
    tree = ast.parse(code)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "static_controller_run":
            func = node
            break
    if func is not None:
        break
assert func is not None, "Controller under test is missing"

# A small artificial concave P-V curve, used ONLY to test numerical logic.
# Measurements are evaluated at current V, not after a hidden update.
V = np.linspace(0., 41.4, 415)

def current_and_power(cid, voltage):
    p = max(0., 100. - (float(voltage)-25.)**2)
    return None, p

namespace = {"np":np,"V":V,"current_and_power":current_and_power}
ast.fix_missing_locations(func)
module = ast.Module(body=[func],type_ignores=[])
exec(compile(module,str(notebook),"exec"),namespace)
controller = namespace["static_controller_run"]

po_p, po_v = controller(1,"po",start_v=27,voltage_step=1,nsteps=10)
ai_p, ai_v = controller(1,"ai",reference_v=23.,start_v=27,voltage_step=1,nsteps=10)
assert len(po_p)==len(ai_p)==len(po_v)==len(ai_v)==10
assert po_v[0]==ai_v[0]==27., "Both algorithms must be measured at start V"
assert po_p[0]==ai_p[0]==96., "Both algorithms must log same starting power"
assert np.all(np.abs(np.diff(po_v)) <= 1.+1e-12)
assert np.all(np.abs(np.diff(ai_v)) <= 1.+1e-12)
assert ai_v[1]==26. and ai_v[4]==23., "AI must move toward target by <=1V"
assert po_v[1]==28. and po_v[2]==27., "P&O must reverse after measured loss"
assert np.all(po_p>=0) and np.all(ai_p>=0)
print("PASS: controller starting measurement parity, bounded voltage step,")
print("      P&O reversal logic, AI target following, nonnegative toy power.")
print("NOTE: synthetic smoke test only; original PV test requires Colab datasets.")

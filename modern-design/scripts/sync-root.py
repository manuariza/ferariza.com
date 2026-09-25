"""Mirror staged public files at repository root, preserving the editable source."""
from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[2]
for source in (root/'_site').iterdir():
    if source.name == 'modern-design':
        continue  # This deployment-only redirect must not overwrite editable source.
    target = root/source.name
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        shutil.copy2(source, target)

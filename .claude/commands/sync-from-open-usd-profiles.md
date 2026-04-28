# sync-from-open-usd-profiles

Sync implementation from `C:\sources\open-usd-profiles\omni\usd_profiles` into this repo's `src\nvidia_usd_profiles\`.

## What this does

Copies all Python source files (except root-level `__init__.py`, `__main__.py`, `_repo_tool.py`, `_config.py`) and applies this rename:

| From | To |
|------|----|
| `from omni.usd_profiles` | `from nvidia_usd_profiles` |
| `omni.usd_profiles` (catch-all) | `nvidia_usd_profiles` |

Also copies:
- `C:\sources\open-usd-profiles\tests\` (test files + resources) → `tests/`, except `test_config.py`
- `C:\sources\open-usd-profiles\CHANGELOG.md` → `CHANGELOG.md`
- `C:\sources\open-usd-profiles\VERSION` → `VERSION`

**Not copied** (intentionally):
- `__init__.py` — this repo has its own, using `importlib.metadata` for version
- `__main__.py` — keep as-is
- `_repo_tool.py` / `_config.py` — repo-tool infrastructure specific to open-usd-profiles; not applicable here
- `test_config.py` — tests `_config.py`/`_repo_tool.py` which are not synced

**Manually maintained** (not overwritten by this script):
- `src/nvidia_usd_profiles/__init__.py` — uses `importlib.metadata.version("nvidia-usd-profiles")`
- `src/nvidia_usd_profiles/__main__.py` — keep as-is

## Steps

1. Create a new branch: `git checkout -b feat/sync-from-open-usd-profiles`

2. Run the migration script below in a Python shell from the repo root.

3. Copy `CHANGELOG.md` and `VERSION`:
   ```bash
   cp C:/sources/open-usd-profiles/CHANGELOG.md CHANGELOG.md
   cp C:/sources/open-usd-profiles/VERSION VERSION
   ```

4. Update `pyproject.toml` version to match the value in `VERSION`.

5. Run `/test` to verify the wheel builds and tests pass.

6. Commit and push, then open an MR to `main`.

## Migration script

```python
from pathlib import Path
import shutil

SRC = Path("C:/sources/open-usd-profiles/omni/usd_profiles")
SRC_TESTS = Path("C:/sources/open-usd-profiles/tests")
DST = Path("src/nvidia_usd_profiles")  # relative to repo root

def transform(content: str) -> str:
    content = content.replace("from omni.usd_profiles", "from nvidia_usd_profiles")
    # catch-all for any remaining occurrences (docstrings, string literals, etc.)
    content = content.replace("omni.usd_profiles", "nvidia_usd_profiles")
    return content

ROOT_SKIP = {"__init__.py", "__main__.py", "_repo_tool.py", "_config.py"}
TEST_SKIP = {"test_config.py"}

def sync_tree(src_dir: Path, dst_dir: Path, is_root: bool = False) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    for item in sorted(src_dir.iterdir()):
        if item.is_dir():
            sync_tree(item, dst_dir / item.name, is_root=False)
        elif item.suffix == ".py" and (not is_root or item.name not in ROOT_SKIP):
            (dst_dir / item.name).write_text(transform(item.read_text(encoding="utf-8")), encoding="utf-8")
        elif item.suffix != ".py":
            shutil.copy2(item, dst_dir / item.name)

# --- core source files and subpackages ---
sync_tree(SRC, DST, is_root=True)

# --- top-level tests and resources ---
tests_root = Path("tests")
for f in sorted(SRC_TESTS.glob("*.py")):
    if f.name not in TEST_SKIP:
        (tests_root / f.name).write_text(transform(f.read_text(encoding="utf-8")), encoding="utf-8")
resources_dst = tests_root / "resources"
if resources_dst.exists():
    shutil.rmtree(resources_dst)
shutil.copytree(SRC_TESTS / "resources", resources_dst)

print("Sync complete.")
```

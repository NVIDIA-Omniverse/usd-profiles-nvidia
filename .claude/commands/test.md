Build the wheel and run the test suite locally.

1. Build the wheel: run `./repo.sh uv -- build -o dist` on Linux/macOS or `.\repo.bat uv -- build -o dist` on Windows
2. Clear stale cached wheels: run `./repo.sh uv -- cache clean` (or `.\repo.bat` on Windows)
3. Find the built wheel in `dist/` — it matches `usd_profiles_nvidia-*.whl`. On Linux use `ls dist/usd_profiles_nvidia-*.whl | tail -1`; on Windows use `Get-ChildItem dist\usd_profiles_nvidia-*.whl | Select-Object -Last 1 -ExpandProperty Name`
4. Run the tests: `./repo.sh uv -- run --no-project --with "dist/<wheel-filename>[sphinx]" python -m unittest discover -s tests -v` (or `.\repo.bat` on Windows)

Report the results. If the build fails, stop and show the error. If tests fail, show which tests failed and why.

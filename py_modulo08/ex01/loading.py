from __future__ import annotations

import importlib
import sys
from typing import Optional, Tuple


def try_import(module_name: str) -> Tuple[bool, Optional[object], Optional[str], Optional[str]]: # noqa
    try:
        mod = importlib.import_module(module_name)
    except Exception as exc:
        return False, None, None, f"{type(exc).__name__}: {exc}"

    version = getattr(mod, "__version__", None)
    if version is not None and not isinstance(version, str):
        version = str(version)

    return True, mod, version, None


def dependency_report() -> dict[str, Tuple[bool, Optional[str], Optional[str]]]: # noqa
    report: dict[str, Tuple[bool, Optional[str], Optional[str]]] = {}
    for name in ["pandas", "numpy", "matplotlib", "requests"]:
        ok, _mod, ver, err = try_import(name)
        report[name] = (ok, ver, err)
    return report


def print_install_instructions(missing: list[str]) -> None:
    print("Missing dependencies:")
    for m in missing:
        print(f"- {m}")

    print()
    print("Install with pip:")
    print("pip install -r requirements.txt")
    print()
    print("Install with Poetry:")
    print("poetry install")
    print("poetry run python loading.py")


def run_analysis() -> None:
    ok_pd, pd, _ver_pd, err_pd = try_import("pandas")
    ok_np, np, _ver_np, err_np = try_import("numpy")
    ok_mpl, _mpl, _ver_mpl, err_mpl = try_import("matplotlib")

    if not ok_pd:
        raise RuntimeError(f"pandas not available. {err_pd}")
    if not ok_np:
        raise RuntimeError(f"numpy not available. {err_np}")
    if not ok_mpl:
        raise RuntimeError(f"matplotlib not available. {err_mpl}")

    if pd is None or np is None:
        raise RuntimeError("Unexpected import state.")

    import matplotlib.pyplot as plt

    n = 1000
    rng = np.random.default_rng(42)

    times = np.arange(n)
    values = rng.normal(loc=0.0, scale=1.0, size=n).cumsum()

    df = pd.DataFrame({"t": times, "signal": values})
    df["rolling_mean"] = df["signal"].rolling(window=30, min_periods=1).mean() # noqa
    df["signal_abs"] = df["signal"].abs()

    plt.figure()
    plt.plot(df["t"], df["signal"], label="signal")
    plt.plot(df["t"], df["rolling_mean"], label="rolling_mean_30")
    plt.title("Matrix data analysis")
    plt.xlabel("t")
    plt.ylabel("signal")
    plt.legend()

    out_path = "matrix_analysis.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Processing {n} data points...")
    print("Generating visualization...\n")
    print(f"Analysis complete! \nResults saved to: {out_path}")


def main() -> None:
    print("\nLOADING STATUS: Loading programs...")
    print()

    print("Checking dependencies:")
    report = dependency_report()
    missing: list[str] = []

    for name in ["pandas", "requests", "matplotlib", "numpy"]:
        ok, ver, err = report[name]
        if ok:
            v = ver if ver is not None else "unknown version"
            if name == "pandas":
                msg = "Data manipulation ready"
            elif name == "numpy":
                msg = "Numerical computing ready"
            elif name == "matplotlib":
                msg = "Visualization ready"
            else:
                msg = "Network access ready"
            print(f"[OK] {name} ({v}) - {msg}")
        else:
            print(f"[MISSING] {name}")
            if err:
                print(f"  reason: {err}")
            missing.append(name)

    if missing:
        print()
        print_install_instructions(missing)
        sys.exit(1)

    print()
    print("Analyzing Matrix data...")
    try:
        run_analysis()
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(2)


if __name__ == "__main__":
    main()

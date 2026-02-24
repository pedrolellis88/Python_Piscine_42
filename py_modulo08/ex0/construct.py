import os
import site
import sys


def is_venv() -> bool:
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def venv_name() -> str:
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path:
        return os.path.basename(venv_path) or venv_path
    return "unknown"


def safe_get_site_packages() -> list[str]:
    paths: list[str] = []
    try:
        for p in site.getsitepackages():
            if isinstance(p, str):
                paths.append(p)
    except Exception:
        pass

    try:
        user_site = site.getusersitepackages()
        if isinstance(user_site, str):
            paths.append(user_site)
    except Exception:
        pass

    seen = set()
    unique: list[str] = []
    for p in paths:
        if p not in seen:
            unique.append(p)
            seen.add(p)
    return unique


def guess_global_site_packages() -> str:
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    ver = f"python{sys.version_info.major}.{sys.version_info.minor}"

    unix_path = os.path.join(base_prefix, "lib", ver, "site-packages")

    return unix_path


def main() -> None:
    inside = is_venv()
    print()
    if inside:
        print("MATRIX STATUS: Welcome to the construct")
    else:
        print("MATRIX STATUS: You're still plugged in")

    print()
    print(f"Current Python: {sys.executable}")

    if inside:
        name = venv_name()
        venv_path = os.environ.get("VIRTUAL_ENV", "not set")
        print(f"Virtual Environment: {name}")
        print(f"Environment Path: {venv_path}")
        print("\nSUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting the global system.")
        print("\nPackage installation path:")
        print(guess_global_site_packages())
    else:
        print("Virtual Environment: None detected")
        print("\nWARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("To enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("source matrix_env/bin/activate  # On Unix")
        print("matrix_env\\Scripts\\activate    # On Windows")
        print("\nThen run this program again.")

    print()


if __name__ == "__main__":
    main()

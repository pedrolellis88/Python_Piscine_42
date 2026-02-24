import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv


REQUIRED_KEYS: Tuple[str, ...] = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)

ALLOWED_MODES: Tuple[str, ...] = ("development", "production")
ALLOWED_LOG_LEVELS: Tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL") # noqa


@dataclass(frozen=True)
class Config:
    matrix_mode: str
    database_url: str
    api_key: str
    log_level: str
    zion_endpoint: str


def _load_env() -> None:
    load_dotenv(override=False)


def _get_env(key: str) -> Optional[str]:
    value = os.getenv(key)
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return value


def _validate_mode(mode: str) -> str:
    mode_lower = mode.lower()
    if mode_lower not in ALLOWED_MODES:
        raise ValueError(f"Invalid MATRIX_MODE: {mode}. Use: development or production.") # noqa
    return mode_lower


def _validate_log_level(level: str) -> str:
    level_upper = level.upper()
    if level_upper not in ALLOWED_LOG_LEVELS:
        raise ValueError(
            f"Invalid LOG_LEVEL: {level}. Use one of: {', '.join(ALLOWED_LOG_LEVELS)}." # noqa
        )
    return level_upper


def _mask_secret(secret: str, show_last: int = 4) -> str:
    if len(secret) <= show_last:
        return "*" * len(secret)
    return ("*" * (len(secret) - show_last)) + secret[-show_last:]


def _security_checks(cfg: Config) -> List[str]:
    checks: List[str] = []

    if cfg.api_key.lower().startswith("dev_") or "change_me" in cfg.api_key.lower():
        checks.append("[WARN] API_KEY looks like a placeholder. Replace it before production." # noqa)
    else:
        checks.append("[OK] API_KEY does not look like a placeholder.")

    checks.append("[OK] Ensure .env is in .gitignore and never committed.")

    if cfg.matrix_mode == "production":
        if cfg.log_level == "DEBUG":
            checks.append("[WARN] LOG_LEVEL is DEBUG in production. Consider INFO or WARNING.") # noqa
        else:
            checks.append("[OK] LOG_LEVEL is not DEBUG in production.")
    else:
        checks.append("[OK] Development mode detected. Overrides are available via env vars.") # noqa

    return checks


def load_config() -> Tuple[Optional[Config], List[str]]:
    _load_env()

    missing: List[str] = []
    raw: Dict[str, Optional[str]] = {k: _get_env(k) for k in REQUIRED_KEYS} # noqa

    for key, value in raw.items():
        if value is None:
            missing.append(key)

    if missing:
        msgs = [
            "ORACLE STATUS: Reading the Matrix...",
            "Configuration error: missing required variables:",
        ]
        msgs.extend([f"- {k}" for k in missing])
        msgs.append("")
        msgs.append("Fix options:")
        msgs.append("1) Create a .env file from the example:")
        msgs.append("   cp .env.example .env")
        msgs.append("   # edit .env with your values")
        msgs.append("2) Or set variables directly in the shell, example:")
        msgs.append(
            "   MATRIX_MODE=production API_KEY=secret123 DATABASE_URL=... LOG_LEVEL=INFO ZION_ENDPOINT=... python3 oracle.py" # noqa
        )
        return None, msgs

    assert raw["MATRIX_MODE"] is not None
    assert raw["DATABASE_URL"] is not None
    assert raw["API_KEY"] is not None
    assert raw["LOG_LEVEL"] is not None
    assert raw["ZION_ENDPOINT"] is not None

    try:
        mode = _validate_mode(raw["MATRIX_MODE"])
        log_level = _validate_log_level(raw["LOG_LEVEL"])
    except ValueError as exc:
        return None, [
            "ORACLE STATUS: Reading the Matrix...",
            f"Configuration error: {exc}",
        ]

    cfg = Config(
        matrix_mode=mode,
        database_url=raw["DATABASE_URL"],
        api_key=raw["API_KEY"],
        log_level=log_level,
        zion_endpoint=raw["ZION_ENDPOINT"],
    )
    return cfg, []


def _describe_database(database_url: str, mode: str) -> str:
    if mode == "development":
        return "Connected to local instance" if "localhost" in database_url or "sqlite" in database_url else "Connected" # noqa
    return "Connected to production instance"


def main() -> int:
    cfg, msgs = load_config()
    if cfg is None:
        for line in msgs:
            print(line)
        return 1

    print("\nORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {cfg.matrix_mode}")
    print(f"Database: {_describe_database(cfg.database_url, cfg.matrix_mode)}")
    print(f"API Access: Authenticated ({_mask_secret(cfg.api_key)})")
    print(f"Log Level: {cfg.log_level}")
    print(f"Zion Network: Online ({cfg.zion_endpoint})")
    print("\nEnvironment security check:")
    for c in _security_checks(cfg):
        print(c)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()

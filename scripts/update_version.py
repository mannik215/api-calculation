"""
Скрипт автоматического увеличения версии приложения.

Использование:

    python scripts/update_version.py

Пример:

    VERSION содержит 1.0.0

После запуска:

    VERSION содержит 1.0.1

Скрипт предназначен для запуска из Jenkins Pipeline.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


VERSION_FILE = PROJECT_ROOT / "VERSION"


def read_version() -> str:
    """
    Читает текущую версию приложения из файла VERSION.
    """

    if not VERSION_FILE.exists():
        raise FileNotFoundError(
            f"Version file not found: {VERSION_FILE}"
        )

    version = VERSION_FILE.read_text(
        encoding="utf-8"
    ).strip()

    return version


def validate_version(version: str) -> tuple[int, int, int]:
    """
    Проверяет формат версии и преобразует её части в числа.

    Ожидаемый формат:

        MAJOR.MINOR.PATCH

    Например:

        1.0.5
    """

    parts = version.split(".")

    if len(parts) != 3:
        raise ValueError(
            f"Invalid version '{version}'. "
            "Expected format: MAJOR.MINOR.PATCH"
        )

    try:
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])

    except ValueError as exc:
        raise ValueError(
            f"Invalid version '{version}'. "
            "Version components must be integers."
        ) from exc

    if major < 0 or minor < 0 or patch < 0:
        raise ValueError(
            "Version components cannot be negative."
        )

    return major, minor, patch


def increment_patch(version: str) -> str:
    """
    Увеличивает PATCH-компонент версии на единицу.

    1.0.0 -> 1.0.1
    1.4.9 -> 1.4.10
    """

    major, minor, patch = validate_version(version)

    patch += 1

    return f"{major}.{minor}.{patch}"


def save_version(version: str) -> None:
    """
    Сохраняет новую версию в файл VERSION.
    """

    VERSION_FILE.write_text(
        version + "\n",
        encoding="utf-8",
    )


def main() -> None:
    """
    Основная последовательность работы скрипта.
    """

    current_version = read_version()

    new_version = increment_patch(current_version)

    save_version(new_version)

    print(f"Old version: {current_version}")
    print(f"New version: {new_version}")

if __name__ == "__main__":
    main()
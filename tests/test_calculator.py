"""
Unit-тесты бизнес-логики калькулятора.

Jenkins будет запускать эти тесты перед сборкой
Docker-образа.

Если хотя бы один assert не выполнится,
pytest вернёт ненулевой exit code.

Jenkins увидит это и остановит pipeline.
"""

import pytest

from app.services.calculator import calculate


def test_add():
    """Проверяем операцию сложения."""

    result = calculate(2, 3, "add")

    assert result == 5


def test_subtract():
    """Проверяем операцию вычитания."""

    result = calculate(10, 4, "subtract")

    assert result == 6


def test_multiply():
    """Проверяем умножение."""

    result = calculate(5, 4, "multiply")

    assert result == 20


def test_divide():
    """Проверяем обычное деление."""

    result = calculate(10, 2, "divide")

    assert result == 5


def test_division_by_zero():
    """
    Проверяем защиту от деления на ноль.

    Ожидаем, что calculate() выбросит ValueError.
    """

    with pytest.raises(
        ValueError,
        match="Division by zero is not allowed",
    ):
        calculate(10, 0, "divide")


def test_unknown_operation():
    """
    Проверяем неизвестную операцию.

    Это дополнительная защита бизнес-логики,
    даже несмотря на то, что API также использует Enum.
    """

    with pytest.raises(ValueError):
        calculate(10, 5, "hack")
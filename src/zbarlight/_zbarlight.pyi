import typing

SymbologyValue: typing.TypeAlias = int
SymbologiesType: typing.TypeAlias = dict[str, SymbologyValue]

Symbologies: SymbologiesType

def zbar_code_scanner(
    symbologies: list[SymbologyValue],
    raw: bytes,
    width: int,
    height: int,
) -> list[bytes] | None: ...

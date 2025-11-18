def es_par(numero: int) -> bool:
    return numero % 2 == 0

def es_impar(numero: int) -> bool:
    return not es_par(numero)

def es_positivo(numero: int) -> bool:
    return numero >= 0

def es_negativo(numero: int) -> bool:
    return not es_positivo(numero)

if __name__ == "__main__":
    assert es_par(2) is True, "2 es par"
    assert es_par(3) is False, "3 es impar"
    assert es_impar(5) is True, "5 es impar"
    assert es_impar(8) is False, "8 es par"
    assert es_negativo(-4) is True, "-4 es negativo"
    assert es_negativo(5) is False, "5 es positivo"
    assert es_positivo(9) is True, "9 es positivo"
    assert es_positivo(-2) is False, "-2 es negativo"
    
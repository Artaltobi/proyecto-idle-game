# Manejo simple de recursos para la fábrica de medias

DINERO_INICIAL = 10

# Recursos de la fábrica
dinero = DINERO_INICIAL
medias = 0       # producto intermedio
cajas = 0        # producto final (se vende)

# Encargados (auto-clickers)
encargado_tejedor = False
encargado_terminado = False
encargado_vendedor = False


def pagar(monto):
    """Intenta pagar un monto. Devuelve True si alcanzó la plata."""
    global dinero
    if dinero >= monto:
        dinero -= monto
        return True
    return False


def producir_media():
    """Suma 1 media tejida."""
    global medias
    medias += 1


def producir_caja():
    """Convierte 1 media en 1 caja, si hay stock."""
    global medias, cajas
    if medias > 0:
        medias -= 1
        cajas += 1
        return True
    return False


def vender(monto):
    """Vende 1 caja y suma dinero."""
    global cajas, dinero
    if cajas > 0:
        cajas -= 1
        dinero += monto
        return True
    return False


def reset():
    """Reinicia toda la economía de la fábrica de medias."""
    global dinero, medias, cajas
    global encargado_tejedor, encargado_terminado, encargado_vendedor

    dinero = DINERO_INICIAL
    medias = 0
    cajas = 0

    encargado_tejedor = False
    encargado_terminado = False
    encargado_vendedor = False

def cargar_desde_save(datos_fabrica):
    """Carga el estado económico desde un dict del save."""
    global dinero, medias, cajas
    global encargado_tejedor, encargado_terminado, encargado_vendedor

    dinero = datos_fabrica.get("dinero", DINERO_INICIAL)
    medias = datos_fabrica.get("medias", 0)
    cajas = datos_fabrica.get("cajas", 0)

    encargado_tejedor = datos_fabrica.get("encargado_tejedor", False)
    encargado_terminado = datos_fabrica.get("encargado_terminado", False)
    encargado_vendedor = datos_fabrica.get("encargado_vendedor", False)


def volcar_a_save():
    """Devuelve un dict con el estado económico actual para guardar en el save."""
    return {
        "dinero": dinero,
        "medias": medias,
        "cajas": cajas,
        "encargado_tejedor": encargado_tejedor,
        "encargado_terminado": encargado_terminado,
        "encargado_vendedor": encargado_vendedor,
    }

# screens/economia.py
# manejo simple de recursos

DINERO_INICIAL = 10000

dinero = DINERO_INICIAL
medias = 0
cajas = 0

# encargados
encargado_tejedor = False
encargado_terminado = False
encargado_vendedor = False


def pagar(monto):
    global dinero
    if dinero >= monto:
        dinero -= monto
        return True
    return False


def producir_media():
    global medias
    medias += 1
    # habilita terminado indirectamente


def producir_caja():
    global medias, cajas
    if medias > 0:
        medias -= 1
        cajas += 1
        return True
    return False


def vender(monto):
    global cajas, dinero
    if cajas > 0:
        cajas -= 1
        dinero += monto
        return True
    return False


def reset():
    global dinero, medias, cajas
    global encargado_tejedor, encargado_terminado, encargado_vendedor
    dinero = DINERO_INICIAL
    medias = 0
    cajas = 0
    encargado_tejedor = False
    encargado_terminado = False
    encargado_vendedor = False

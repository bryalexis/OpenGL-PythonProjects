"""
    Ecuaciones de la recta del gran señor Volcán y(x)
    Cuesta Izquierda    y = (5/8)*(x-4900)
    Crater              y = 2500
    Cuesta Derecha      y = (-5/4)*(x-13100)
"""
def enCuestaIzquierda(x,y):
    return (x >= 4900 and x < 8900) and (y <= (5/8)*(x-4900))

def enCrater(x,y):
    return (x >= 8900 and x <= 11100) and (y <= 2500)

def enCuestaDerecha(x,y):
    return (x > 11100 and x <= 13100) and (y <= (-5/4)*(x-13100))

def esCB_CuestaIzq(x_R,x,y):
    return enCuestaIzquierda(x_R,y) and (not enCuestaIzquierda(x,y))

def esCB_CuestaDer(x_L,x,y):
    return enCuestaDerecha(x_L,y) and (not enCuestaDerecha(x,y))

def esCB_Crater(y_B,x,y):
    return enCrater(x,y_B) and (not enCrater(x,y))

def dentroDelVolcan(x,y):
    return enCuestaIzquierda(x,y) or enCuestaDerecha(x,y) or enCrater(x,y)

def fueraDelVolcan(x,y):
    return not dentroDelVolcan(x,y)

def shouldDisappear(i,j,h):
    if fueraDelVolcan(i*h,j*h):
        return False
    elif enCuestaIzquierda(i*h,j*h):
        return enCuestaIzquierda((i-1)*h,j*h) and enCuestaIzquierda(i*h,(j+1)*h) and enCuestaIzquierda((i-1)*h,(j+1)*h)
    elif enCuestaDerecha(i*h,j*h):
        return enCuestaDerecha((i+1)*h,j*h) and enCuestaDerecha(i*h,(j+1)*h) and enCuestaDerecha((i+1)*h,(j+1)*h)
    else:
        return not (fueraDelVolcan((i+1)*h,j*h) or fueraDelVolcan((i-1)*h,j*h) or fueraDelVolcan(i*h,(j+1)*h))
    
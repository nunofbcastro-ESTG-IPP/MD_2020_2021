
def readInt(mensagem):
    error=1
    while error == 1:
        try:
            number = int(input(str(mensagem)))
            error=0
        except:
            error=1
    return number

def moduloPositive(value, mod):
    modulo=value%mod
    while(modulo<0):
        modulo=modulo+mod
    return modulo

def getPosition(alfabeto, letter):
    for i in range(len(alfabeto)):
        if alfabeto[i].capitalize() == letter.capitalize():
            return i
    return -1

def extended_euclid_gcd(a, b):#Retirada do site: https://www.rookieslab.com/posts/extended-euclid-algorithm-to-find-gcd-bezouts-coefficients-python-cpp-code
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r//r 
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t
    return [old_r, old_s, old_t] #old_r=mdc(a,b),  old_s=coeficiente de a, old_t=coeficiente de b,

def desencripta():
    alfabeto=['A' ,'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', '.', ',', '!']
    mult=readInt("Valor a multiplicar na encriptacao:")
    soma=readInt("Valor a somar na encriptacao:")
    [mdc, coeficienteA, coeficienteB]=extended_euclid_gcd(mult, len(alfabeto))
    if mdc==1: #verificar se e possivel fazer a inversa
        soma=soma*coeficienteA
        frase=str(input("Frase Encriptada:"))
        desencriptada=""
        desencriptadaN=""
        for i in frase:
            p=getPosition(alfabeto, i)
            if p != -1 :
                desencriptada=desencriptada+alfabeto[moduloPositive(p*coeficienteA-soma, len(alfabeto))]
                desencriptadaN=desencriptadaN+str(p)+" "
            else :
                desencriptada=desencriptada+i
                desencriptadaN=desencriptadaN+i
        print("Frase Desencriptada: "+desencriptada)
        print(desencriptadaN)
    else: 
        print("Nao e possivel desencriptar")

desencripta()
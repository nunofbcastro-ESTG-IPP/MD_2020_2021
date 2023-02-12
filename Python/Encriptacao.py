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

def mdc(a, b):#Retirada do site: https://www.rookieslab.com/posts/extended-euclid-algorithm-to-find-gcd-bezouts-coefficients-python-cpp-code
    temp=0
    while(b > 0):
        temp = b
        b = a % b
        a = temp
    
    return a

def encripta():
    alfabeto=['A' ,'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', '.', ',', '!']
    mult=readInt("Valor a multiplicar:")
    if mdc(len(alfabeto), mult) == 1:
        soma=readInt("Valor a somar:")
        frase=str(input("Frase:"))
        encriptada=""
        encriptadaN=""
        for i in frase:
            p=getPosition(alfabeto, i)
            if p != -1 :
                encriptada=encriptada+alfabeto[moduloPositive(soma+p*mult, len(alfabeto))]
                encriptadaN=encriptadaN+str(p)+" "
            else :
                encriptada=encriptada+i
                encriptadaN=encriptadaN+i
        print("Frase Encriptada: "+encriptada)
        print(encriptadaN)
    else:
        print("Nao e possivel encriptar")

encripta()
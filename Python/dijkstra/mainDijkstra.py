from dijkstraspf import *

def lerInt(min, mensagem, errorMensage):
    number=min-1
    while number < min:
        try:
            number = int(input(str(mensagem)))
        except:
            number=min-1
    return number

def pesquisaArray(valor, array):
    for valorArray in array:
        if valorArray == valor:
            return True
    return False

def lerString(mensagem, naoLer, igual):
    valor=""
    while len(valor)<=0:
        valor=str(input(str(mensagem)))
        if(naoLer!=None):
            if pesquisaArray(valor, naoLer):
                valor=""
        if(igual!=None and valor!=""):
            if pesquisaArray(valor, igual) == False:
                valor=""
    return valor

def lerFloat(min, paraLer, mensagem, errorMensage):
    number=min-1
    while number < min:
        try:
            number = input(str(mensagem))
            number = float(number)
        except:
            if number == paraLer :
                number=min
                return None
            number=min-1
    return number

def dijktra():
    grafo=[]
    vertices=[]
    for i in range(lerInt(2, "Number Vertices:", "Valor invalido")):
        vertices.append(lerString("Vertice "+str(i+1)+":", vertices, None))
    for i in range(0,len(vertices)-1):
        for j in range(i+1,len(vertices)):
            number=lerFloat(0, "Nao tem", "Peso "+vertices[i]+" "+vertices[j]+":",  "Valor invalido")
            if number!=None:
                grafo.append([])
                grafo[len(grafo)-1].append(vertices[i])
                grafo[len(grafo)-1].append(vertices[j])
                grafo[len(grafo)-1].append(number)
    verticeIncial=lerString("Vertice incial:", None, vertices)
    verticeFinal=lerString("Vertice final:", [verticeIncial], vertices)
    caminho = dijkstra_spf(grafo, verticeFinal)[verticeIncial].allpaths()
    caminho=caminho[0]
    peso=0.0
    for i in range(0,len(caminho)-1):
        for j in range(0,len(grafo)):
            if caminho[i] == grafo[j][0] and caminho[i+1] == grafo[j][1] or caminho[i+1] == grafo[j][0] and caminho[i] == grafo[j][1]:
                peso=peso+grafo[j][2]
    
    print("Caminho:"+str(caminho))
    print("Custo final: "+str(round(peso,2)))

dijktra()
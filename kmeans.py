import random
def chooseRandom(k,lista):
	#Escolhe os k pontos iniciais aleatoriamente
	return [lista[i] for i in random.sample(range(0,len(lista)-1), k)]
def d(A,B):
	# Distancia entre dois pontos A e B
	s = 0
	if len(A) == len(B): 
		for i in range(len(A)):
			s += (A[i]-B[i])**2
	return s**0.5
def centroToProb(centro,lista,atual):
	distPontoCentro = [d(ponto,centro)**2 for ponto in lista]
	probCentro = [dist/sum(distPontoCentro ) for dist in distPontoCentro]
	for x in range(len(atual)):
		if probCentro[x] > atual[x]:
			probCentro[x] = atual[x]
	return probCentro
def choosePlus(k,lista):
	centros = [lista[random.randint(0,len(lista)-1)]]
	probCentro = centroToProb(centros[0],lista,[])
	for i in range(1,k):
		centros.append(random.choices(lista, weights=probCentro, k=1)[0])
		probCentro = centroToProb(centros[i],lista,probCentro)
	return centros
def kmeans(lista,centros, elbow = 0):
	a = 1
	k = len(centros)
	while a:
		listaClust = [0 for i in range(len(lista))]
		# Procurando qual o centro mais próximo para cada ponto
		for i in range(len(lista)):			
			menor = float('inf')
			for j in range(k):
				dista = d(lista[i],centros[j])
				if dista < menor:
					listaClust[i] = j
					menor = dista
		#Calculando qual será o novo Centro
		tempCentros = [[0 for i in range(len(lista[0]))] for g in range(k)]
		qtdPontos = [0 for i in range(k)]
		for i in range(k):
			for j in range(len(lista)):
				if listaClust[j] == i:
					qtdPontos[i] +=1
					for g in range(len(lista[0])):
						tempCentros[i][g]+= lista[j][g]
		tempCentros = [[tempCentros[g][i]/qtdPontos[g] for i in range(len(lista[0]))] for g in range(k)]
		if centros == tempCentros:
			a = 0
		else:
			centros= tempCentros
		
	if 	elbow:
		return ([(lista[i], listaClust[i]) for i in range(len(lista))],centros)
	else:
		return [(lista[i], listaClust[i]) for i in range(len(lista))]
def kElbow(lista, centro = 'P', interval = range(1,10)):
	if centro == 'P':
		fCentro = choosePlus
	elif centro == 'R':
		fCentro = chooseRandom
	else:
		print('Método de achar o centro não válido.')
		return 0
	distancias = []
	for k in interval:
		resultados,centros = kmeans(lista,fCentro(k,lista), 1)
		wcss = 0 
		for i in resultados:
			wcss += (d(i[0],centros[i[1]])**2)
		distancias.append(wcss)
	return distancias
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

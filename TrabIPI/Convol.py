import numpy as np
import cv2

def convImg(Im, masc):

	M,N = Im.shape
	m,n = masc.shape

	#so funciona para mascaras com dimensoes impar
	a = (m-1)/2
	b = (n-1)/2

	nova = np.zeros((M,N)) #imagem de saida
	# Percorrendo
	# linhas da imagem
	for x in range(int(a),int(M)-int(a)):
		# Colunas da imagem
		for y in range(int(b),int(N)-int(b)): 
			# Linha da mascara
			for s in range (int(-a), int(a+1)): 
				# Coluna da mascara
				for t in range(int(-b),int(b+1)): 
					nova[x][y] += masc[s+int(a)][t+int(b)] * Im[x+s][y+t]

	nova = np.round(nova)
	nova = nova.astype(np.uint8)
	return nova

def gauss(x, y, k, sigma):
	return k*np.exp(-(x**2 + y**2))/(2*sigma**2)
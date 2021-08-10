import numpy as np 
import cv2     
import math

#Im: imagem original; dim: nova dimensao
#amplia/reduz por vizinho mais proximo
def redVizProx(Im, dim):
    r_in, c_in = Im.shape
    #fator de escala: linha
    s_r = r_in/float(dim[0]) 
    #fator de escala: colun
    s_c = c_in/float(dim[1]) 

    #criando a matriz da nova imagem
    novaImagem = np.zeros(dim, dtype='uint8')

    for x in range(dim[0]):
        for y in range(dim[1]):
            #coordenadas do subpixel
            rf = x*s_r
            rc = y*s_c
            r = round(rf)
            c = round(rc)

            # retira subpixel da imagem original
            if r < 0:
                r = 0
            if c < 0:
                c = 0   
            if r >= r_in:
                r = r_in - 1
            if c >= c_in:
                c = c_in - 1
            
            novaImagem[x][y] = Im[r][c]

    return novaImagem

# amplia/reduz por interpolacao bilinear
def redBilin(Im, dim):
    r_in, c_in = Im.shape

    sr = r_in/float(dim[0])
    sc = c_in/float(dim[1])

    #criando a nova imagem
    Im_nova = np.zeros(dim, dtype='uint8')
    for x in range(dim[0]):
        for y in range(dim[1]): 
            rf = x*sr
            cf = y*sc

            r0 = int(math.floor(rf))
            c0 = int(math.floor(cf))
            
            if r0 < 0:
                r0 = 0
            if c0 < 0:
                c0 = 0   
            if r0 >= r_in-1:
                r0 = r_in - 2
            if c0 >= c_in-1:
                c0 = c_in - 2
            
            deltaR  = rf - r0
            deltaC = cf - c0
            
            Im_nova[x][y] = Im[r0][c0]*(1-deltaR)*(1-deltaC)+ \
                            Im[r0+1][c0]*deltaR*(1-deltaC)  + \
                            Im[r0][c0+1]*(1-deltaR)*deltaC  + \
                            Im[r0+1][c0+1]*deltaR*deltaC

    return Im_nova

# redimensionamento por Resize
def zoom(ImgOrig,cont):
    img = ImgOrig
    #cv2.imshow("Original", ImgOrig)
    largura = img.shape[1]
    altura = img.shape[0]
    proporcao = float(altura/largura)
    largura_nova = largura
    largura_nova += cont
    altura_nova = int(largura_nova*proporcao)

    tamanho_novo = (largura_nova, altura_nova)
    print('Novo tamanho: ',tamanho_novo)

    img_redimensionada = cv2.resize(img,tamanho_novo, interpolation = cv2.INTER_AREA)
    #cv2.imshow('Zoom', img_redimensionada)
    #cv2.waitKey(0)

    return img_redimensionada
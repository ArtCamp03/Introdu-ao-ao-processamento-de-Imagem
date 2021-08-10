''''
UNIVERSIDADE FEDERAL DE MATO GROSSO
BACHARELADO EM CIENCIA DA COMPUTAÇÃO
Disciplina: Introduçao ao Processamento de Imagem
Alunos: Artur R Campos e Douglas Monaro
'''
from tkinter import *
from tkinter import filedialog
import subprocess
import cv2
from PIL import ImageTk, Image
import numpy as np
from numpy.lib.type_check import imag
import Redi_Cor as rc
import Convol as cv

#criando Menu
class sistema():
        #--------------------MENU---------------------

    def __init__(self, master=None):
        self.frame = Frame(master)
        self.frame.pack()

        #--------------------Arquivo---------------------

        self.menu=Menu(master)
        self.menuArquivo=Menu(self.menu,tearoff=0)
        self.menuArquivo.add_command(label="Abrir imagem",command=self.Abri_Arqv)
        self.menuArquivo.add_command(label="Salvar imagem",command=self.Salva_Img)
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label="Cancelar",command=self.Cancelar)
        self.menuArquivo.add_command(label="Fechar",command=master.quit)
        self.menu.add_cascade(label="Arquivo",menu=self.menuArquivo)

        #--------------------Suavizaçao---------------------

        self.menuSuaviza=Menu(self.menu,tearoff=0)
        self.menuSuaviza.add_command(label="Média",command=self.Suaviza_Media)
        self.menuSuaviza.add_command(label="Gaussiano",command=self.Suaviza_Gaus)
        self.menuSuaviza.add_command(label="Negativa",command=self.negativo)
        self.menu.add_cascade(label="Suavizar",menu=self.menuSuaviza)

        #--------------------Aguçamento---------------------

        self.menuSuaviza=Menu(self.menu,tearoff=0)
        self.menuSuaviza.add_command(label="Laplaciano",command=self.Agu_Laplace)
        self.menu.add_cascade(label="Agucamento",menu=self.menuSuaviza)

        #--------------------Reamostragem---------------------

        self.menuSuaviza=Menu(self.menu,tearoff=0)
        self.menuSuaviza.add_command(label="Vizinho Proximo",command=self.Reamostr_VizProx)
        self.menuSuaviza.add_command(label="Interpolação",command=self.Reamostr_InterPola)
        self.menu.add_cascade(label="Reamostragem",menu=self.menuSuaviza)

        #--------------------Frequencia---------------------

        self.menuSuaviza=Menu(self.menu,tearoff=0)
        self.menuSuaviza.add_command(label="Fourier",command=self.Frequencia)
        self.menu.add_cascade(label="Frequencia",menu=self.menuSuaviza)

        master.config(menu=self.menu)

        # Frame contendo imagem original
        self.FrameImg = Frame(master)
        self.FrameImg.pack(side = TOP, fill=BOTH,expand=1)

        #canvas na janela principal
        self.canvas = Canvas(self.FrameImg, borderwidth = 1,background='black')
        self.canvas.pack(side = TOP, fill=BOTH,expand=1)

        # Frame onde ficara ajustes dos filtros
        self.FrameAjsut = Frame(self.frame,width=850,height=70)
        self.FrameAjsut.pack(side = TOP)

        #----------- suavizaçao -------------

        self.sigma = Label(self.FrameAjsut, text="Suavizaçao:")
        self.sigma.place(x=50,y=0)
        self.sigma = Label(self.FrameAjsut, text="Sigma:")
        self.sigma.place(x=1,y=20)
        self.mascS = Entry(self.FrameAjsut, width="5")
        self.mascS.place(x=50,y=20)
        self.K = Label(self.FrameAjsut, text="k:")
        self.K.place(x=1,y=45)
        self.mascK = Entry(self.FrameAjsut, width="5")
        self.mascK.place(x=50,y=45)

        self.filtroX = Label(self.FrameAjsut, text="Filtro: X")
        self.filtroX.place(x=90,y=20)
        self.mascX1 = Entry(self.FrameAjsut, width="5")
        self.mascX1.place(x=140,y=20)
        self.y = Label(self.FrameAjsut, text="Y:")
        self.y.place(x=90, y=45)
        self.mascy1 = Entry(self.FrameAjsut, width="5")
        self.mascy1.place(x=140, y=45)

        #----------- Reamostragem -------------

        self.Reamstr = Label(self.FrameAjsut, text="Reamostragem: ")
        self.Reamstr.place(x=230,y=0)
        self.posiX = Label(self.FrameAjsut, text="X: ")
        self.posiX.place(x=200, y=20)
        self.entraX = Entry(self.FrameAjsut, width="5")
        self.entraX.place(x=220,y=20)
        self.posiY = Label(self.FrameAjsut, text="Y: ")
        self.posiY.place(x=200, y=45)
        self.entraY = Entry(self.FrameAjsut, width="5")
        self.entraY.place(x=220, y=45)

        #----------- ZOOM -------------

        self.Zoom = Label(self.FrameAjsut, text="Zoom:")
        self.Zoom.place(x=350,y=0)
        self.zoomIn = Button(self.FrameAjsut,height=1, text="Zoom +",command=self.ZoomIn)
        self.zoomIn.place(x=350,y=25)
        self.zoomOut = Button(self.FrameAjsut,height=1, text="Zoom -",command=self.ZoomOut)
        self.zoomOut.place(x=420,y=25)

    # Abre Arquivo selecionado
    def Abri_Arqv(self):
        self.canvas.filename = filedialog.askopenfilename(
            initialdir="Downloads",
            title="Selecione uma imagem",
            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")),
        )
        self.ImgEntrada = Image.open(self.canvas.filename)
        # Inicializa proporçao da imagem
        self.img = self.ImgEntrada.resize((650,420),Image.ANTIALIAS)
        self.img2 = cv2.imread(self.canvas.filename, cv2.IMREAD_GRAYSCALE)
        self.imgTrata = cv2.imread(self.canvas.filename)
        self.imgSaida = self.imgTrata.copy()

        self.canvasImage(self.img)

        ''' 
        print('endereco:',self.canvas.filename)
        print('img:',self.img)
        print('img2:',self.img2)
        print('imgTrata:',self.imgTrata)
        print('imgSaida:',self.imgSaida)
        '''

    def Cancelar(self):
        cv2.destroyAllWindows()
        self.imgTrata = ""
        self.canvas.delete("all")
        self.canvas2.delete("all")
    
    # salva nova imagem
    def Salva_Img(self):
        cv2.imwrite("NewImg.jpg", self.imgTrata)

    #-----------------FILTROS----------------------
    def Suaviza_Media(self):
        print('**** Suavizacao Media *****')

        # valores de entrada
        self.X1 = self.mascX1.get()
        self.Y1 = self.mascy1.get()
        self.x_int = int(self.X1)
        self.y_int = int(self.Y1)

        self.imgTrata = boxfilter(self.imgTrata, self.x_int, self.y_int)

    def Suaviza_Gaus(self):
        print('**** Suavizacao Gaus *****')

        # valores de entrada
        self.X1 = self.mascX1.get()
        self.Y1 = self.mascy1.get()
        self.x_int = int(self.X1)
        self.y_int = int(self.Y1)       

        self.Sigma = self.mascS.get()
        self.K = self.mascK.get()
        self.sigma_int = int(self.Sigma)
        self.k_int = int(self.K)

        self.imgTrata = filtroGaussiano(self.imgTrata, self.sigma_int, self.k_int, self.x_int, self.y_int)
 
    def negativo(self):
        print('**** Negativa *****')
        self.imgTrata = negativa(self.imgTrata)

    def Agu_Laplace(self):
        print('**** Agucamento Laplaciano *****')
        # converte a imagem para escalas de cinza
        self.imgTrata =laplaceFiltro(self.imgTrata)
                    
    def Reamostr_VizProx(self):
        print('**** Reamostragem Vizinho mais Proximo *****')
        # recupera o valor que esta na entrada
        self.X2 = self.entraX.get()
        self.Y2 = self.entraY.get()

        print('X2',self.X2)
        print('Y2',self.Y2)

        self.x_int = int(self.X2)
        self.y_int = int(self.Y2)
        
        self.imgTrata = vizinhoProximo(self.imgTrata, self.x_int, self.y_int)

    def Reamostr_InterPola(self):
        print('**** Reamostragem Interpolacao *****')
        # recupera o valor que esta na entrada
        self.X2 = self.entraX.get()
        self.Y2 = self.entraY.get()

        print('X2',self.X2)
        print('Y2',self.Y2)

        self.x_int = int(self.X2)
        self.y_int = int(self.Y2)

        self.imgTrata = interpolaBi(self.imgTrata, self.x_int, self.y_int)

    def Frequencia(self):
        print('**** Frequencia *****')
        self.imgTrata = fourier(self.img2)

    # Salva alteraçao da imagem
    def salvarArquivo(self):
        print('**** Imagem Alterada *****')
        cv2.imwrite('ImgAlterada.jpg', self.imgSaida)
    
    def canvasImage(self, imagem):
        self.canvas.image = ImageTk.PhotoImage(imagem)
        self.canvas.create_image(450,300, image = self.canvas.image, anchor= CENTER)

    # Funçao Zoom    
    def ZoomIn(self):
        print('Aumentar imagem')

        largura = self.img2.shape[1]
        altura = self.img2.shape[0]
        tamanho = (largura, altura)
        #print('tamanho: ',tamanho)
        #di = (largura,altura)
        new_img = rc.zoom(self.img2,50)
        self.img2 = new_img

        cv2.waitKey(1)
        cv2.imshow('Zoom +', new_img)

    def ZoomOut(self):
        print('Diminuir imagem')

        largura = self.img2.shape[1]
        altura = self.img2.shape[0]
        tamanho = (largura, altura)
        print('tamanho: ',tamanho)
        #di = (largura,altura)

        new_img = rc.zoom(self.img2,-50)
        self.img2 = new_img
        
        cv2.waitKey(1)
        cv2.imshow('Zoom -', new_img)

#Suavizacao----------- ---------------------------------------------------
# Box Filter
def boxfilter(imagem, x, y):
    fator = x * y

    masc = ((1.0/fator) * np.ones((x,y)))

    b,g,r = cv2.split(imagem)            

    imgB = cv.convImg(b, masc)
    imgG = cv.convImg(g, masc)
    imgR = cv.convImg(r, masc)
    
    imgB = np.round(imgB)
    imgG = np.round(imgG)
    imgR = np.round(imgR)
    
    imgB = imgB.astype(np.uint8)
    imgG = imgG.astype(np.uint8)
    imgR = imgR.astype(np.uint8)

    # canais de cores B,G,R
    imgSaida = cv2.merge((imgB,imgG,imgR))
    
    imagem = imgSaida

    cv2.imshow('Mascara de Media',imgSaida)
    cv2.waitKey(0) 
    return imgSaida 
    
def filtroGaussiano(imagem, S, K, x, y):
    i = x
    j = y

    gaussMasc = np.zeros((i,j))

    l,c = gaussMasc.shape

    fatorL = (l-1)/2
    fatorC = (c-1)/2

    for i in range(l):
        for j in range(c):
            gaussMasc[i][j] = cv.gauss(x-fatorL, y-fatorC, S, K)

    soma = np.sum(gaussMasc)

    gaussMasc = (1/soma)*gaussMasc
    b,g,r = cv2.split(imagem)

    imgB = cv.convImg(b, gaussMasc)
    imgG = cv.convImg(g, gaussMasc)
    imgR = cv.convImg(r, gaussMasc)

    imgB = np.round(imgB)
    imgG = np.round(imgG)
    imgR = np.round(imgR)

    imgB = imgB.astype(np.uint8)
    imgG = imgG.astype(np.uint8)
    imgR = imgR.astype(np.uint8)

    # canais de cores B,G,R
    imgSaida = cv2.merge((imgB,imgG,imgR))

    imagem = imgSaida

    cv2.imshow('Mascara Gaussiana',imgSaida)
    cv2.waitKey(0)
    return imgSaida

def negativa(imagem):
    saida = 255-imagem
    cv2.imshow('Negativa', saida)
    cv2.waitKey(0)
    return saida

#Aguçamento------------------------------------------------------------------------------------------
def laplaceFiltro(imagem):

    img = imagem
    #separa os canais de cores
    b,g,r = cv2.split(img)        
    laplace = np.ones((3,3))

    laplace[1][1] = -8.0
    
    imgB = cv.convImg(b,laplace)
    imgG = cv.convImg(g,laplace)
    imgR = cv.convImg(r,laplace)

    lap1 = cv2.merge((imgB,imgG,imgR))

    imgSaida = img.astype(np.float32) - lap1.astype(np.float32)

    minimo = np.min(lap1)
    lap1 = lap1 - minimo
    maximo = np.max(lap1)
    lap1 = (255.0/maximo)*lap1
    lap1 = np.round(lap1)
    lap1 = lap1.astype(np.uint8)

    imgSaida[imgSaida<0] = 0.0
    imgSaida[imgSaida>255] = 255
    imgSaida = np.round(imgSaida)
    imgOut = imgSaida.astype(np.uint8)

    cv2.imshow('laplaciana',lap1)
    cv2.waitKey(0)
    cv2.imshow('Img out',imgOut)
    cv2.waitKey(0)
    return imgSaida

#Reamostragem -------------------------------------------------------------------------------
def vizinhoProximo(imagem, x, y):
    n_dim = [x, y]
    b,g,r = cv2.split(imagem)
    imgB = rc.redVizProx(b,n_dim)
    imgG = rc.redVizProx(g,n_dim)
    imgR = rc.redVizProx(r,n_dim)

    imgSaida = cv2.merge((imgB,imgG,imgR)) # junta os canais de cores (bgr -> ordem correta)
    imgTrata = imgSaida

    cv2.imshow('Reamostragem',imgTrata)
    cv2.waitKey(0)
    return imgTrata

#Interpolacao bilinear---------------------------------------------------------------------------------------
def interpolaBi(imagem, x, y):

    n_dim = [x, y]
    b,g,r = cv2.split(imagem)
    imgB = rc.redBilin(b,n_dim)
    imgG = rc.redBilin(g,n_dim)
    imgR = rc.redBilin(r,n_dim)

    # junta os canais de cores (bgr -> ordem correta)
    imgNova = cv2.merge((imgB,imgG,imgR)) 
    imgSaida = imgNova

    cv2.imshow('Interpolaçao',imgSaida)
    cv2.waitKey(0)
    return imgSaida

#Dominio de Frequencia --------------------------------------------------------------------------------------
def fourier(imagem):
    M,N = imagem.shape
    f = (1.0/(15.0*15.0)) * np.ones((15,15))
    m,n = f.shape
    f = np.pad(f,(((M-m+1)//2,(M-m)//2),((N-n+1)//2,(N-n)//2)),'constant')
    f = np.fft.ifftshift(f)
    I = np.fft.fft2(imagem)
    F = np.fft.fft2(f)
    C = I * F
    saida = np.fft.ifft2(C)
    saida = np.real(saida)
    saida = saida.astype(np.uint8)

    cv2.imshow('Frequencia - Fourier', saida)
    cv2.waitKey(0)
    return saida

def main():
    # Criando a instancia
    app = Tk()
    
    # Criando o titulo da Janela
    app.title("My photoshop")
    
    # Tamanho da janela
     # LxA+E+T
    app.geometry('850x600+20+20')
    
    # cor de fundo
    app['bg'] = '#BEBEBE'
    
    #inicializa objeto
    sistema(app)

    #Criando a janela
    app.mainloop()

if __name__ == "__main__":
    main()

    convSepImg
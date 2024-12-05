# -*- coding: utf-8 -*-

import numpy as np

class Imagem: 
    def __init__(self,arqEntrada):

        self.working = True
        self.arqEntrada = arqEntrada #Não alterar essa linha
        
        self.matrix = None
        self.dimension = None
        self.maxPixelValue = 0
        self.type = ''
        self.width = 0
        self.height = 0

        self.extract_image_data()

        

    def extract_image_data(self):
        
        try:
            arq = open(self.arqEntrada, 'r')

        except:
            #print('O caminho do arquivo inserido não existe.')
            self.working = False
            return None

        imgString = arq.read().replace('\n', ' ')
        
        imgList = imgString.split(' ')

        popped = 0
        
        for i in range(len(imgList)):
        
            realIndex = i-popped

            if imgList[realIndex]=='':
                imgList.pop(realIndex)
                popped += 1
            
            elif imgList[realIndex].isnumeric():
                imgList[realIndex]=int(imgList[realIndex])
        
        
        self.type = imgList[0]
        self.width = int(imgList[1])
        self.height = int(imgList[2])
        
        self.maxPixelValue = int(imgList[3])

        imgList = imgList[4:]

        index = 0
        if self.type == 'P2':
            
            self.dimension = (self.height, self.width)
            self.matrix = np.zeros(self.dimension, np.int64)

            for i in range(self.height):
                for j in range(self.width):
                    self.matrix[i, j] = imgList[index]
                    index += 1

        elif self.type == 'P3':
            
            self.dimension = (self.height, self.width*3)
            self.matrix = np.zeros(self.dimension, np.int64)

            for i in range(self.height):
                for j in range(self.width):
                    self.matrix[i, (j*3):(j*3)+3] = imgList[index*3:index*3+3]
                    index += 1

        #print(self.matrix)

        arq.close()
    
    def matrix_to_image_data(self, matrix, arqSaida, width, height):

        matrixList = matrix.tolist()

        with open(arqSaida, 'w+') as arq:
            
            arq.write(str(self.type)+'\n')
            arq.write(str(width)+' '+str(height)+'\n')
            arq.write(str(self.maxPixelValue)+'\n')

            for line in matrixList:
                for element in line:
                    arq.write(str(element)+' ')
                arq.write('\n')
                
            arq.close()
            
            
# Classe ImagemPGM herda a classe Imagem
class ImagemPGM(Imagem):

    def __init__(self,arqEntrada):

        super().__init__(arqEntrada) #Não alterar essa linha
        
        if self.type != 'P2': 
            #print('A estrutura do arquivo não corresponde à classe invocada.')
            self.working=False
        

    def brilho(self,arqSaida,valor):
        
        if not self.working:
            return False
    
        result_matrix = np.zeros(self.dimension, np.int64)

        for i in range(self.height):
            for j in range(self.width):
                newPixelValue = self.matrix[i,j]+valor if self.matrix[i,j]+valor<self.maxPixelValue else self.maxPixelValue
                result_matrix[i, j]= newPixelValue

        #print(result_matrix)

        self.matrix_to_image_data(result_matrix, arqSaida, self.width, self.height)

        return True

 
    def espelha(self,arqSaida):

        if not self.working:
            return False
    
        result_matrix = np.zeros(self.dimension, np.int64)

        for i in range(self.height):
            for j in range(self.width):

                result_matrix[i, j]= self.matrix[i,self.width-j-1]

        #print(result_matrix)

        self.matrix_to_image_data(result_matrix, arqSaida, self.width, self.height)

        return True

    

    ## Podem ser criados outros métodos


# Classe ImagemPGM herda a classe Imagem
class ImagemPPM(Imagem):

    def __init__(self,arqEntrada):

        super().__init__(arqEntrada) #Não alterar essa linha

        if self.type != 'P3': 
            #print('A estrutura do arquivo não corresponde à classe invocada.')
            self.working=False


    def espelha(self,arqSaida):

        if not self.working:
            return False
    
        result_matrix = np.zeros(self.dimension, np.int64)

        for i in range(self.height):
            for j in range(self.width):

                result_matrix[i, j*3:(j*3)+3]= self.matrix[i,(self.width-j-1)*3:((self.width-j-1)*3)+3]

        #print(result_matrix)

        self.matrix_to_image_data(result_matrix, arqSaida, self.width, self.height)

        return True

    def rotaciona90(self,arqSaida):
        if not self.working:
            return False
    
        result_matrix = np.zeros((self.width, self.height*3), np.int64)

        print(self.matrix)
        for i in range(self.height):
            for j in range(self.width):

                result_matrix[2-j, (i*3):(i*3)+3] = self.matrix[i, j*3:(j*3)+3]

        print(result_matrix)

        self.matrix_to_image_data(result_matrix, arqSaida, self.height, self.width)

        return True

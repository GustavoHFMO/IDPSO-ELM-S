#-*- coding: utf-8 -*-
'''
Created on 13 de fev de 2017

@author: gusta
'''

class Metricas_deteccao():
    '''
    Classe para instanciar as metricas de deteccao  
    '''
    
    pass

    def resultados_com_taxa_deteccao(self, lista):
        '''
        Metodo para computar os falsos_alarmes, atrasos e a porcentagem de falta de deteccao para o artigo FEDD
        :param lista: lista com os indices de todas as deteccoes encontradas
        :return: retorna uma lista com os seguintes valores [falsos_alarmes, atrasos, porcentagem_falta_deteccao] 
        '''
        
        det1 = 2000
        det2 = 5000
        det3 = 8000
        
        deteccoes = 0
        deteccoes_verdadeiras = [False] * 3
        auxiliar = [False] * 3
        
        
        falsos_alarmes = 0
        atrasos = 0
        falta_deteccao = 0
        
        increment = 1
        
        for x, i in enumerate(lista):
            
            #condicoes para computar os atrasos e falsos alarmes
            if(i >= 0 and i < det1):
                falsos_alarmes += increment
            
            elif(i >= det1 and i < det2):
                deteccoes += increment
                
                if(auxiliar[0] == False):
                    atrasos = atrasos + i-det1
                
                auxiliar[0] = True  
                
                if(deteccoes_verdadeiras[0] == True):
                    falsos_alarmes += increment
            
                if(auxiliar[0] == True):
                    deteccoes_verdadeiras[0] = True
             
            elif(i >= det2 and i < det3):
                deteccoes += increment
                
                if(auxiliar[1] == False):
                    atrasos = atrasos + i-det2
                
                auxiliar[1] = True  
                
                if(deteccoes_verdadeiras[1] == True):
                    falsos_alarmes += increment
            
                if(auxiliar[1] == True):
                    deteccoes_verdadeiras[1] = True   
            
            
            elif(i >= det3):
                deteccoes += increment
                
                if(auxiliar[2] == False):
                    atrasos = atrasos + i-det3
                
                auxiliar[2] = True  
                
                if(deteccoes_verdadeiras[2] == True):
                    falsos_alarmes += increment
            
                if(auxiliar[2] == True):
                    deteccoes_verdadeiras[2] = True
            
            else:
                falta_deteccao += increment
                atrasos = atrasos + det3-det2
            
            
            
        #condicoes para computar as faltas de deteccoes e os atrasos
        if(deteccoes_verdadeiras[0] == False):
            falta_deteccao += increment
            #atrasos = atrasos + det2-det1
        if(deteccoes_verdadeiras[1] == False):
            falta_deteccao += increment
            #atrasos = atrasos + det3-det2
        if(deteccoes_verdadeiras[2] == False):
            falta_deteccao += increment
            #atrasos = atrasos + 11000-det3
            
        falta_deteccao = float(falta_deteccao)
        geral = float(3)
        porcentagem_falta_deteccao = falta_deteccao/geral       
        
        return falsos_alarmes, atrasos, porcentagem_falta_deteccao

    def resultados_dow_drift(self, lista, n):
        '''
        Metodo para computar os falsos_alarmes, atrasos e a porcentagem de falta de deteccao da serie Down Jones Industrial Average
        :param lista: lista com os indices de todas as deteccoes encontradas
        :return: retorna uma lista com os seguintes valores [falsos_alarmes, atrasos, porcentagem_falta_deteccao] 
        '''
        
        atrasos_lista = [183, 203, 224]
        deteccoes = [124 - n,
                    307 - n, 
                    510 - n] 
        
        falsos_alarmes = 0
        atrasos = 0
        increment = 1
        auxiliar = [False] * len(deteccoes)
        
        for i in range(len(lista)):
            # x < 124
            if(lista[i] < deteccoes[0]):
                falsos_alarmes += increment

            # x >= 124 e x < 307     
            elif(lista[i] >= deteccoes[0] and lista[i] < deteccoes[1]):      
                
                if(auxiliar[0] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[0] == False):
                    atrasos = atrasos + lista[i] - deteccoes[0]
                    auxiliar[0] = True
                   
                
            # x >= 307 e x < 510
            elif(lista[i] >= deteccoes[1] and lista[i] < deteccoes[2]):      
                
                if(auxiliar[1] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[1] == False):
                    atrasos = atrasos + lista[i] - deteccoes[1]
                    auxiliar[1] = True
                   
            # x >= 510
            elif(lista[i] >= deteccoes[2]):      
                
                if(auxiliar[2] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[2] == False):
                    atrasos = atrasos + lista[i] - deteccoes[2]
                    auxiliar[2] = True
                    
            
        for i in range(len(auxiliar)):
            if(auxiliar[i] == False):
                atrasos += atrasos_lista[i]
                    
        return falsos_alarmes, atrasos
    
    def resultados_sp_drift(self, lista, n):
        '''
        Metodo para computar os falsos_alarmes, atrasos e a porcentagem de falta de deteccao da serie Down Jones Industrial Average
        :param lista: lista com os indices de todas as deteccoes encontradas
        :return: retorna uma lista com os seguintes valores [falsos_alarmes, atrasos, porcentagem_falta_deteccao] 
        '''
        
        atrasos_lista = [60, 1207, 1111, 1293, 220]
        deteccoes = [448 - n,
                    508 - n, 
                    1715 - n,
                    2826 - n,
                    4119 - n] 
        
        falsos_alarmes = 0
        atrasos = 0
        increment = 1
        auxiliar = [False] * len(deteccoes)
        
        for i in range(len(lista)):
            
            #print("Detecção: ", lista[i])
            
            # x < 448
            if(lista[i] < deteccoes[0]):
                falsos_alarmes += increment

            # x >= 448 e x < 508     
            elif(lista[i] >= deteccoes[0] and lista[i] < deteccoes[1]):      
                
                if(auxiliar[0] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[0] == False):
                    atrasos = atrasos + lista[i] - deteccoes[0]
                    #print(lista[i], " - ", deteccoes[0], ": ")
                    #print("Atraso: ", lista[i] - deteccoes[0])
                    #print("Total: ", atrasos)
                    auxiliar[0] = True
                   
                
            # x >= 508 e x < 1715
            elif(lista[i] >= deteccoes[1] and lista[i] < deteccoes[2]):      
                
                if(auxiliar[1] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[1] == False):
                    atrasos = atrasos + lista[i] - deteccoes[1]
                    #print(lista[i], " - ", deteccoes[0], ": ")
                    #print("Atraso: ", lista[i] - deteccoes[0])
                    #print("Total: ", atrasos)
                    auxiliar[1] = True
                    
            
            # x >= 1715 e x < 2826      
            elif(lista[i] >= deteccoes[2] and lista[i] < deteccoes[3]):      
                
                if(auxiliar[2] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[2] == False):
                    atrasos = atrasos + lista[i] - deteccoes[2]
                    #print(lista[i], " - ", deteccoes[0], ": ")
                    #print("Atraso: ", lista[i] - deteccoes[0])
                    #print("Total: ", atrasos)
                    auxiliar[2] = True
            
            
            # x >= 2826 e x < 4119
            elif(lista[i] >= deteccoes[3] and lista[i] < deteccoes[4]):      
                
                if(auxiliar[3] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[3] == False):
                    atrasos = atrasos + lista[i] - deteccoes[3]
                    #print(lista[i], " - ", deteccoes[0], ": ")
                    #print("Atraso: ", lista[i] - deteccoes[0])
                    #print("Total: ", atrasos)
                    auxiliar[3] = True
                   
            # x >= 4119
            elif(lista[i] >= deteccoes[4]):      
                
                if(auxiliar[4] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[4] == False):
                    atrasos = atrasos + lista[i] - deteccoes[4]
                    #print(lista[i], " - ", deteccoes[0], ": ")
                    #print("Atraso: ", lista[i] - deteccoes[0])
                    #print("Total: ", atrasos)
                    auxiliar[4] = True
            
            
        # computando os atrasos
        for i in range(len(auxiliar)):
            if(auxiliar[i] == False):
                atrasos += atrasos_lista[i]
                    
        return falsos_alarmes, atrasos
    
    def resultados_cnt(self, lista, n):
        '''
        Metodo para computar os falsos_alarmes, atrasos para o artigo ICTAI
        :param lista: lista com os indices de todas as deteccoes encontradas
        :return: retorna uma lista com os seguintes valores [falsos_alarmes, atrasos, porcentagem_falta_deteccao] 
        '''
        
        atraso_maximo = 2000
        deteccoes = [2000 - n,
                    4000 - n, 
                    6000 - n, 
                    8000 - n, 
                    10000 - n, 
                    12000 - n, 
                    14000 - n, 
                    16000 - n, 
                    18000 - n] 
        
        falsos_alarmes = 0
        atrasos = 0
        increment = 1
        auxiliar = [False] * len(deteccoes)
        
        for i in range(len(lista)):
            # x < 5000
            if(lista[i] < deteccoes[0]):
                falsos_alarmes += increment

            # x >= 5000 e x < 10000     
            elif(lista[i] >= deteccoes[0] and lista[i] < deteccoes[1]):      
                
                if(auxiliar[0] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[0] == False):
                    atrasos = atrasos + lista[i] - deteccoes[0]
                    auxiliar[0] = True
                   
                
            # x >= 10000 e x < 15000
            elif(lista[i] >= deteccoes[1] and lista[i] < deteccoes[2]):      
                
                if(auxiliar[1] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[1] == False):
                    atrasos = atrasos + lista[i] - deteccoes[1]
                    auxiliar[1] = True
                   
            # x >= 15000 e x < 20000
            elif(lista[i] >= deteccoes[2] and lista[i] < deteccoes[3]):      
                
                if(auxiliar[2] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[2] == False):
                    atrasos = atrasos + lista[i] - deteccoes[2]
                    auxiliar[2] = True
                    
            # x >= 20000 e x < 25000
            elif(lista[i] >= deteccoes[3] and lista[i] < deteccoes[4]):      
                
                if(auxiliar[3] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[3] == False):
                    atrasos = atrasos + lista[i] - deteccoes[3]
                    auxiliar[3] = True
                   
            # x >= 25000 e x < 30000
            elif(lista[i] >= deteccoes[4] and lista[i] < deteccoes[5]):      
                
                if(auxiliar[4] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[4] == False):
                    atrasos = atrasos + lista[i] - deteccoes[4]
                    auxiliar[4] = True
                   
            # x >= 30000 e x < 35000
            elif(lista[i] >= deteccoes[5] and lista[i] < deteccoes[6]):      
                
                if(auxiliar[5] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[5] == False):
                    atrasos = atrasos + lista[i] - deteccoes[5]
                    auxiliar[5] = True
                   
            # x >= 35000 e x < 40000
            elif(lista[i] >= deteccoes[6] and lista[i] < deteccoes[7]):      
                
                if(auxiliar[6] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[6] == False):
                    atrasos = atrasos + lista[i] - deteccoes[6]
                    auxiliar[6] = True
                   
            # x >= 40000 e x < 45000
            elif(lista[i] >= deteccoes[7] and lista[i] < deteccoes[8]):      
                
                if(auxiliar[7] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[7] == False):
                    atrasos = atrasos + lista[i] - deteccoes[7]
                    auxiliar[7] = True
                   
            #x >= 45000
            elif(lista[i] >= deteccoes[8]):      
                
                if(auxiliar[8] == True):
                    falsos_alarmes += increment
                    
                if(auxiliar[8] == False):
                    atrasos = atrasos + lista[i] - deteccoes[8]
                    auxiliar[8] = True
                    
            
        for i in range(len(auxiliar)):
            if(auxiliar[i] == False):
                atrasos += atraso_maximo
                    
        return falsos_alarmes, atrasos
    
    def resultados(self, stream, lista, n):
        '''
        metodo para computar as metricas de deteccao de forma dinamica conforme o dataset passado
        :param: stream: vetor inteiro, contendo os dados da serie usada
        :param: lista: vetor inteiro, contendo as deteccoes encontradas
        :param: n: inteiro, contendo a quantidade de dados usados no treinamento
        :return: retorna as metricas falsos_alarmes, atrasos 
        '''
        
        if(len(stream)+n == 20000):
            return self.resultados_cnt(lista, n)
            
        elif((len(stream)+n == 753)):
            return self.resultados_dow_drift(lista, n)
            
        elif((len(stream)+n == 4229)):
            return self.resultados_sp_drift(lista, n)
        
        else:
            return self.resultados_cnt(lista, n)
        
def main():
    
    lista9 = [700, 1800, 3800, 5800, 7800, 9800, 11800, 13800, 15800, 17800]
    lista10 = [700, 800, 2800, 4800, 6800, 8800, 10800, 12800, 14800, 16800]
    #lista11 = [1140, 1898, 2562, 3900, 5800, 8776, 13031, 15130, 16038]

    
    lista11 = [1075, 1894, 2366, 2626, 4833, 7622, 13081, 15130, 16041, 16447]
    
    mt = Metricas_deteccao()
    [falsos_alarmes, atrasos] = mt.resultados(lista11, 200)
    
    print("Falsos Alarmes: ", falsos_alarmes)
    print("Atrasos na deteccao: ", atrasos)
    
    

if __name__ == "__main__":
    main()  
    
    
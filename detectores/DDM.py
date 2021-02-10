#-*- coding: utf-8 -*-
'''
Created on 10 de mar de 2017

@author: gusta
'''
from numpy import array
import numpy as np
import random
import copy

class DDM():
    def __init__(self, w, c):
        '''
        Método para criar um modelo do ECDD
        :param Lambda: float com o valor de lambda
        :param w: float com o nivel de alarme
        :param l: float com o nivel de deteccao
        '''
        self.w = w
        self.c = c
        self.media_min = 0
        self.desvio_min = 0
        self.nada = "Nada"
        self.alerta = "Alerta"
        self.mudanca = "Mudanca"
    
    def armazenar_conceito(self, media_min, desvio_min, erros):
        '''
        Este metodo tem por objetivo armazenar um conceito de um erro 
        :param media_min: media min dos erros
        :param desvio_min: desvio min dos erros
        '''
        self.media_min = media_min
        self.desvio_min = desvio_min
        self.erros = erros
    
    def monitorar(self, erro, t):
        '''
        Este metodo tem por objetivo monitorar um erro para saber se ele mudou de distribuicao
        :param erro: double com o erro para ser verificado
        :param t: instante de tempo
        '''
       
         
        nova_dist = copy.deepcopy(self.erros)
        nova_dist.append(erro)
        desvio = np.std(nova_dist)
        
        '''
        #calculando o desvio
        parte1 = (erro*(1-erro))
        parte2 = (parte1/(t))
        
        if(parte2 <= 0):
            parte2 = 0
                
        desvio = np.sqrt(parte2)
        '''
        
        #consultando as regras
        if(erro + desvio >= self.media_min + (self.desvio_min)):
            return self.mudanca
        elif(erro + desvio >= self.media_min + (self.w*self.desvio_min)):
            return self.alerta
        else:   
            return self.nada
    
def main():
    random.seed(1)
    dist1 = array([random.uniform(0,2) for i in range(100)])

    ecdd = DDM(2, 3)
    ecdd.armazenar_conceito(np.min(dist1), np.std(dist1))
    
    
    for e in range(100):
        if(e < 20):
            erro = random.uniform(0,2)
        if(e > 20):
            erro = random.uniform(1,2)
        if(e > 40):
            erro = random.uniform(2,3)
        if(e > 60):
            erro = random.uniform(0,2)
        if(e > 80):
            erro = random.uniform(2,4)
            
        print("[" , e , "]: " , erro)
        print(ecdd.monitorar(erro, e))
        
    
    
if __name__ == "__main__":
    main()
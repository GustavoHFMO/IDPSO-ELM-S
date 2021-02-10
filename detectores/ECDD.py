#-*- coding: utf-8 -*-
'''
Created on 10 de mar de 2017

@author: gusta
'''
from numpy import array
import numpy as np
import random


class ECDD():
    def __init__(self, Lambda, w, l):
        '''
        Método para criar um modelo do ECDD
        :param Lambda: float com o valor de lambda
        :param w: float com o nivel de alarme
        :param l: float com o nivel de deteccao
        '''
        self.Lambda = Lambda
        self.w = w
        self.l = l
        self.media_zero = 0
        self.desvio_zero = 0
        self.desvio_z = 0
        self.zt = 0
        self.nada = "Nada"
        self.alerta = "Alerta"
        self.mudanca = "Mudanca"
        self.sensor_mudanca = True
    
    def armazenar_conceito(self, MI0, SIGMA0):
        '''
        Este método tem por objetivo armazenar um conceito de um erro 
        :param MI0: média dos erros
        :param SIGMA0: desvio dos erros
        '''
        self.media_zero = MI0
        self.desvio_zero = SIGMA0
    
    def atualizar_ewma(self, erro, t):
        '''
        método para atualizar o ewma conforme o erro no tempo t
        :param erro: double com o erro para ser verificado
        :param t: instante de tempo
        '''
        
        #calculando a média movel
        if(t == 0):
            self.zt = (1-self.Lambda) * self.media_zero + self.Lambda * erro
        elif(self.sensor_mudanca == True):
            self.sensor_mudanca = False
            self.zt = (1-self.Lambda) * self.media_zero + self.Lambda * erro
        else:
            self.zt = (1-self.Lambda) * self.zt + self.Lambda * erro
        
        
        #calculando o desvio da média movel
        parte1 = (self.Lambda/(2-self.Lambda))
        parte2 = (1-self.Lambda)
        parte3 = (2*t)
        parte4 = (1 - (parte2**parte3))
        parte5 = (parte1 * parte4 * self.desvio_zero)
        self.desvio_z = np.sqrt(parte5)
    
    def monitorar(self):
        '''
        método para monitorar a condicao do detector
        '''
        
        #consultando as regras
        if(self.zt > self.media_zero + (self.l*self.desvio_z)):
            self.sensor_mudanca = True
            return self.mudanca
        elif(self.zt > self.media_zero + (self.w*self.desvio_z)):
            return self.alerta
        else:   
            return self.nada
    
    
def main():
    #simulando um conjunto de erros
    random.seed(1)
    dist1 = array([random.uniform(0,2) for i in range(100)])

    #instanciando o modelo de um ECDD
    ecdd = ECDD(0.2, 1, 1.5)
    
    #armazenando o conceito inicial, ou seja, a media e o seu desvio padrao
    ecdd.armazenar_conceito(np.mean(dist1), np.std(dist1))
    
    #simulando a deteccao de mudanca com o ecdd
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
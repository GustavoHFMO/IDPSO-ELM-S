#-*- coding: utf-8 -*-
'''
Created on 13 de fev de 2017
@author: gusta
'''

import numpy as np
from sklearn.metrics import mean_squared_error

class Metricas_previsao():
    '''
    Classe para instanciar as metricas de previsao  
    '''
    pass

    def mean_absolute_percentage_error(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica MAPE
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        if(type(y_true) == np.ndarray):
            
            erros = []
            for i in range(len(y_true)):
                
                if(y_pred[i:i+1] == 0):
                    y_pred[i:i+1] = 0.01
                    
                if(y_true[i:i+1] == 0):
                    y_true[i:i+1] = 0.01
            
                erro = np.abs((y_true[i:i+1] - y_pred[i:i+1]) / y_true[i:i+1]) * 100
                erros.append(erro)
                
            return np.mean(erros)
        
        else:
            y_true = np.asarray(y_true)
            y_pred = np.asarray(y_pred)
            
            if(y_pred == 0):
                y_pred = 0.01
            
            if(y_true == 0):
                y_true = 0.01
        
            mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
            
            return mape
    
    def mape(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica MAPE
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        y_true, y_pred = self.Correcao(y_true, y_pred)
        
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
            
        erros = []
        for i in range(len(y_true)):
            erro = np.abs((y_true[i:i+1] - y_pred[i:i+1]) / y_true[i:i+1])
            erros.append(erro)
        
        mape = np.mean(erros)  
        return mape
        
    def mse(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica MAPE
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        return mean_squared_error(y_true, y_pred)
    
    def arv(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica ARV
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        y_true, y_pred = self.Correcao(y_true, y_pred)
        
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
            
        media = np.mean(y_true)
        
        vetor_cima = []
        vetor_baixo = []
        
        for i in range(len(y_true)):
            cima = (y_pred[i:i+1]- y_true[i:i+1])**2
            baixo = (y_pred[i:i+1] - media)**2
            vetor_cima.append(cima)
            vetor_baixo.append(baixo)
            
        cima_final = np.sum(vetor_cima)
        baixo_final = np.sum(vetor_baixo)
        
        arv = (cima_final/baixo_final)/len(y_pred)
                
        return arv

    def pocid(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica POCID
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        y_true, y_pred = self.Correcao(y_true, y_pred)
        
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        
        D = []
        for i in range(1, len(y_true)):
            cima = (y_true[i:i+1] - y_true[i-1:i])
            baixo = (y_pred[i:i+1] - y_pred[i-1:i])
            erro = cima * baixo
            
            if(erro > 0):
                D.append(1)
            else:
                D.append(0)
                
        D_final = np.sum(D)
            
        pocid = 100 * (D_final/len(y_true)-1) 
        
        return pocid
    
    def hitRatio(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica POCID
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        y_true, y_pred = self.Correcao(y_true, y_pred)
        
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        
        D = []
        for i in range(1, len(y_true)):
            esquerda = (y_true[i:i+1] - y_true[i-1:i])
            direita = (y_pred[i:i+1] - y_pred[i-1:i])
            erro = esquerda * direita
            
            if(erro > 0):
                D.append(1)
            else:
                D.append(0)
                
        D_final = np.sum(D)
            
        pocid = D_final/(len(y_true)-1)  
        
        return pocid
    
    def smape(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica MAPE
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        y_true, y_pred = self.Correcao(y_true, y_pred)
        
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
            
        erros = []
        for i in range(len(y_true)):
            cima = np.abs(y_true[i:i+1] - y_pred[i:i+1])
            baixo = (np.abs(y_true[i:i+1]) + np.abs(y_pred[i:i+1]))/2
            erro =  cima/baixo
            erros.append(erro)
        
        mape = np.mean(erros)  
        return mape
    
    def theil(self, y_true, y_pred): 
        '''
        Metodo para computar a metrica theil
        :param y_true: lista com os dados reais
        :param y_pred: lista com as previsoes
        :return: retorna a metrica para o conjunto apresentado 
        '''
        
        y_true, y_pred = self.Correcao(y_true, y_pred)
        
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
            
        vetor_cima = []
        vetor_baixo = []
        for i in range(len(y_true)):
                
            if(i == 0):
                cima = (y_true[i:i+1] - y_pred[i:i+1])**2
                baixo = (y_true[i:i+1] - (y_true[i:i+1] + 0.001))**2
                vetor_cima.append(cima)
                vetor_baixo.append(baixo)
                    
            else:
                cima = (y_true[i:i+1] - y_pred[i:i+1])**2
                baixo = (y_true[i:i+1] - y_pred[i-1:i])**2
                vetor_cima.append(cima)
                vetor_baixo.append(baixo)
                
        cima_final = np.sum(vetor_cima)
        baixo_final = np.sum(vetor_baixo)
            
        theil = cima_final/baixo_final 
        
        return theil

    def Correcao(self, entrada, saida):
        '''
        método para corrigir possiveis divisoes com numeros zeros
        '''
        
        for i in range(len(entrada)):
            if(entrada[i] == 0):
                entrada[i] = 0.001
            if(saida[i] == 0):
                saida[i] = 0.001
                
        return entrada, saida
    
def main():
    y_true = [3, -0.5, 2, 7] 
    y_pred = [2.5, -0.3, 2, 8]
    
    mp = Metricas_previsao()
    mape = mp.mean_absolute_percentage_error(y_true, y_pred)
    
    print("MAPE:", mape)

if __name__ == "__main__":
    main()  
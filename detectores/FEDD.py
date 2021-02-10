#-*- coding: utf-8 -*-
'''
Created on 10 de mar de 2017

@author: gusta
'''

import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
from ferramentas.Importar_dataset import Datasets
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf


class FEDD():
    def __init__(self, Lambda, w, c):
        '''
        Método para criar um modelo do ECDD
        :param Lambda: float com o valor de lambda
        :param w: float com o nivel de alarme
        :param c float com o nivel de deteccao
        '''
        self.Lambda = Lambda
        self.w = w
        self.c = c
        self.vetor_caracteristicas_inicial = 0
        self.media_zero = 0
        self.desvio_zero = 0
        self.desvio_z = 0
        self.zt = 0
        self.below_warn = 0
        self.warn = 0
        self.nada = "Nada"
        self.alerta = "Alerta"
        self.mudanca = "Mudanca"
        self.sensor_mudanca = True
    
    def armazenar_conceito(self, vetor_caracteristicas_inicial, MI0, SIGMA0):
        '''
        Este metodo tem por objetivo armazenar um conceito de um erro 
        :param caracteristicas_iniciais: vetor de caracteristicas iniciais
        :param MI0: media dos erros
        :param SIGMA0: desvio dos erros
        '''
        self.vetor_caracteristicas_inicial = vetor_caracteristicas_inicial
        self.media_zero = MI0
        self.desvio_zero = SIGMA0
    
    def atualizar_ewma(self, erro, t):
        '''
        método para atualizar o ewma com o erro atual
        :param erro: double com o erro para ser verificado
        :param t: instante de tempo
        '''
        
        #calculando a m�dia movel
        if(t == 1):
            self.zt = (1-self.Lambda) * self.media_zero + self.Lambda * erro
        elif(self.sensor_mudanca == True):
            self.sensor_mudanca = False
            self.zt = (1-self.Lambda) * self.media_zero + self.Lambda * erro
        else:
            self.zt = (1-self.Lambda) * self.zt + self.Lambda * erro
        
        
        #calculando o desvio da m�dia movel
        parte1 = (self.Lambda/(2-self.Lambda))
        parte2 = (1-self.Lambda)
        parte3 = (2*t)
        parte4 = (1 - (parte2**parte3))
        parte5 = (parte1 * parte4 * self.desvio_zero)
        self.desvio_z = np.sqrt(parte5)
    
    def monitorar(self):
        '''
        Método para consultar a condicao de deteccao do FEDD
        '''
        
        #consultando as regras
        if(self.zt > self.media_zero + (self.c * self.desvio_z)):
            self.sensor_mudanca = True
            #self.below_warn = 0
            return self.mudanca
        
        elif(self.zt > self.media_zero + (self.w * self.desvio_z)):
            #self.below_warn += 1
            
            #if(self.below_warn == 10):
            #    self.below_warn = 0
            
            return self.alerta
        
        else:   
            return self.nada
        
    def teste_estacionariedade(self, timeseries):
        
        '''
        Este metodo tem por testar a estacionariedade de uma serie com o teste adfuller
        :param: timeseries: serie temporal, array
        :return: print com as estatisticas do teste
        '''
        
        #Determing rolling statistics
        timeseries = pd.DataFrame(timeseries)
        rolmean = timeseries.rolling(window=12, center=False).mean()
        rolstd = timeseries.rolling(window=12, center=False).std()
            
        #Perform Dickey-Fuller test:
        print('Results of Dickey-Fuller Test:')
        timeseries = timeseries[1:].values
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
        for key,value in dftest[4].items():
            dfoutput['Critical Value (%s)'%key] = value
        print(dfoutput)
        
    
        #Plot rolling statistics:
        orig = plt.plot(timeseries, color='blue',label='Original')
        mean = plt.plot(rolmean, color='red', label='Rolling Mean')
        std = plt.plot(rolstd, color='black', label = 'Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
        plt.show()
    
    def FE(self, serie_atual):
        '''
        Método para fazer a diferenciacao de uma serie_atual
        :param serie_atual: serie_atual real
        '''  
        
        #serie_df = pd.DataFrame(serie_atual)
        serie_diff = pd.Series(serie_atual)
        serie_diff = serie_diff - serie_diff.shift()
        serie_diff = serie_diff[1:]
        
        
        features = []
        
        #feature 1:
        auto_correlacao = acf(serie_diff, nlags=5)
        for i in auto_correlacao:
            features.append(i)
        
        #feature 2:
        parcial_atcorr = pacf(serie_diff, nlags=5)
        for i in parcial_atcorr:
            features.append(i)
        
        #feature 3:
        variancia = serie_diff.std()
        features.append(variancia)
        
        #feature 4:
        serie_skew = serie_diff.skew()
        features.append(serie_skew)

        #feature 5:
        serie_kurtosis = serie_diff.kurtosis()
        features.append(serie_kurtosis)
        
        #feature 6:
        turning_p = self.turningpoints(serie_diff)
        features.append(turning_p)
        
        #feature 7:
        
        #feature 8:
        
        
        return features
    
    def turningpoints(self, lst):
        dx = np.diff(lst)
        return np.sum(dx[1:] * dx[:-1] < 0)
    
    def computar_distancia(self, vetor1, vetor2):
        '''
        Método para computar a correlacao de pearson entre dois vetores
        :param vetor1: vetor de caracteristicas inicial
        :param vetor2: vetor de caracteristicas atual
        :return: distancia
        '''  
        
        #correlacao = pearsonr(vetor1, vetor2)
        #distancia = correlacao[0]
        
        distancia = cosine(vetor1, vetor2)
        
        return distancia
    
    
def main():
    dtst = Datasets()
    dataset = dtst.Leitura_dados(dtst.bases_linear_graduais(2, 30), excel=True)
    #particao = Particionar_series(dataset, [0.0, 0.0, 0.0], 0)
    #dataset = particao.Normalizar(dataset)
    
    fedd = FEDD(0.2, 0.75, 1)
    feature = fedd.FE(dataset[5300:5601], dataset[0:300])
    print(feature)
    
    
    
    
if __name__ == "__main__":
    main()
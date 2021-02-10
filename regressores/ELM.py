#-*- coding: utf-8 -*-
'''
Created on 31 de jan de 2017

@author: gusta
'''

import numpy as np
from sklearn.metrics import mean_absolute_error
from ferramentas.Particionar_series import Particionar_series
from ferramentas.Importar_dataset import Datasets
import matplotlib.pyplot as plt 

#criando o construtor da classe ELMRegressor
class ELMRegressor():
    def __init__(self, neuronios_escondidos = None):
        '''
        Construtor do algoritmo ELM
        :param neuronios_escondidos: quantidade de neuronios para a camada escondida
        '''
        self.neuronios_escondidos = neuronios_escondidos
        
        self.train_entradas = []
        self.train_saidas = []
        self.val_entradas = []
        self.val_saidas = []
        self.teste_entradas = []
        self.teste_saidas = []
        

    #treinamento do ELM

    def Treinar(self, Entradas, Saidas, pesos = None):
        '''
        Metodo para treinar a ELM por meio da pseudo-inversa
        :param Entradas: entradas para o treinamento da rede, esses dados sao uma matriz com uma quantidade de lags definida
        :param Saidas: saidas para o treinamento da rede, esses dados sao um vetor com as saidas correspodentes as entradas
        :return: retorna os pesos de saida da rede treinada
        '''
        
        #Entradas é uma lista de arrays com os padroes de entrada, matriz com os lags definidos 
        #Saidas é a saida, que possui a mesma quantidade de linhas que a matriz Entradas 
        #Entradas.shape[0] retorna a quantidade de linhas
        #Entradas.shape[1] retorna a quantidade de colunas
        
        #empilhando dois arrays de mesma dimensao
        #se for um array, a primeira coluna é dada pelos valores do array, enquanto que a segunda é cheia de numeros uns
        Entradas = np.column_stack([Entradas, np.ones([Entradas.shape[0], 1])])
        
        #definindo os pesos iniciais aleatoriamente
        #cria uma matriz com numeros aleatorios de tamanho linha x coluna
        #pesos iniciais correspondentes a entrada
        
        if(np.any(pesos) == None):
            self.pesos_iniciais = np.random.randn(Entradas.shape[1], self.neuronios_escondidos)
        else:
            self.pesos_iniciais = pesos
        
        #np.dot - multiplicação de matrizes
        #np.tan - tangente hiperbolica
        #np.linalg.pinv - pseudo inversa 
        
        # computacao a ativacao neuronios com a funcao hiperbolica
        G = np.tanh(Entradas.dot(self.pesos_iniciais))
        
        # computase a previsao para os dados de entrada
        self.pesos_saidas = np.linalg.pinv(G).dot(Saidas)
      
    def Predizer(self, Entradas):
        '''
        Metodo para realizar a previsao de acordo com um conjunto de entrada
        :param Entradas: padroes que serao usados para realizar a previsao
        :return: retorna a previsao para o conjunto de padroes inseridos
        '''
        
        #empilhando dois arrays em colunas, o primeiro é dado pelo array Entradas e a segunda coluna é feita de numeros 1
        Entradas = np.column_stack([Entradas, np.ones([Entradas.shape[0],1])])
        
        #computando pelos neuronios iniciais
        G = np.tanh(Entradas.dot(self.pesos_iniciais))
            
        #computando pelos neuronios de saida
        return G.dot(self.pesos_saidas)
    
    def PredizerPhaseAdjustment(self, Entradas):
        '''
        Metodo para realizar a previsao de acordo com um conjunto de entrada
        :param Entradas: padroes que serao usados para realizar a previsao
        :return: retorna a previsao para o conjunto de padroes inseridos
        '''
        
        # fazendo a previsao inicial
        previsao = self.Predizer(Entradas)
        
        # fazendo o ajuste de fase
        adjustment = np.column_stack([Entradas[:,1:], previsao])
        
        # previsao com o ajuste
        return self.Predizer(adjustment)
    
    def Otimizar_rede(self, neuronios_max, lista):
        '''
        Metodo para otimizar a arquitetura da ELM
        :param neuronios_max: quantidade maxima de neuronios que serao variados
        :param lista: esse parametro é uma lista com os seguintes dados [treinamento_entrada, treinamento_saida, validacao_entrada, validacao_saida]]
        '''
        
        BEST = []
        MAE_TEST_MINS = []
        
        #range (start, stop, step)
        for M in range(1, neuronios_max, 1):
            
            #variaveis para treinamento e teste
            #MAES_TRAIN = []
            MAES_TEST = []
            
            print("Training with %s neurons..."%M)
            
            #variando os pesos iniciais
            for i in range(10):
                #classe recebendo uma quantidade M de neuronios_max
                ELM = ELMRegressor(M)
                #ajustando o ELM para o conjunto de treinamento
                ELM.Treinar(lista[0], lista[1])
                #realizando a previsão para o treinamento
                prediction = ELM.Predizer(lista[0])
                #adicionando na lista o MAE do treinamento
                #MAES_TRAIN.append(mean_absolute_error(lista[1], prediction))
        
                #realizando a previsão para o teste
                prediction = ELM.Predizer(lista[2])
                #adicionando na lista o MAE do teste
                MAES_TEST.append(mean_absolute_error(lista[3], prediction))
                
            #salvando o menor MAE obtido no teste    
            MAE_TEST_MINS.append(np.mean(MAES_TEST))
            n_min = min(MAE_TEST_MINS)
            n_pos = MAE_TEST_MINS.index(n_min)
            self.neuronios_escondidos = n_pos
        
        #printando o menor erro obtido
        print("Minimum MAE ELM =", n_min)

    def Tratamento_dados(self, serie, divisao, lags):
        #dividindo a serie para particionar
        particao = Particionar_series(serie, divisao, lags)
        
        #tratamento dos dados
        [train_entrada, train_saida] = particao.Part_train()
        [val_entrada, val_saida] = particao.Part_val()
        [teste_entrada, teste_saida] = particao.Part_test()
        
        #transformação das listas em arrays
        self.train_entradas = np.asarray(train_entrada)
        self.train_saidas = np.asarray(train_saida)
        self.val_entradas = np.asarray(val_entrada)
        self.val_saidas = np.asarray(val_saida)
        self.teste_entradas = np.asarray(teste_entrada)
        self.teste_saidas = np.asarray(teste_saida)

def main():
    
    #load da serie
    import pandas as pd
    dataset = pd.read_csv("../series/WINJ19_M5_201903061300_201904051750.csv", header=None, sep='\t')[5][1:].values
    dataset = np.array(dataset, dtype=float)
    particao = Particionar_series(dataset, [0.0, 0.0, 0.0], 4, norm=True)
    
    # dividindo os dados entre treinamento e teste
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(particao.matriz_entrada, particao.vetor_saida, test_size=0.1, shuffle=False, stratify=None)
    
    # treinando da forma convencional
    ELM = ELMRegressor(10)
    ELM.Treinar(X_train, y_train)
    
    # realizando a previsao no teste da forma convencional
    previsao_teste = ELM.Predizer(X_test)
    MAE = mean_absolute_error(y_test, previsao_teste)
    print('ELM Prediction - Test MAE: ', MAE)
    plt.plot(previsao_teste, label="Prediction")
    
    # realizando a previsao no teste da forma convencional
    previsao_teste = ELM.PredizerPhaseAdjustment(X_test)
    MAE = mean_absolute_error(y_test, previsao_teste)
    print('ELM Prediction Adjusted - Test MAE: ', MAE)
    plt.plot(previsao_teste, label="Prediction Adjusted")
    
    # plotando os valores reais
    plt.plot(y_test, label="Real")
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    main()
    
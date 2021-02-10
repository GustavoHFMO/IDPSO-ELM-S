#-*- coding: utf-8 -*-
import numpy as np
import copy

def Janela_tempo(serie, janela):
    '''
    metodo que transforma um vetor em uma matriz com os dados de entrada e um vetor com as respectivas saidas 
    :param serie: serie temporal que sera remodelada
    :return: retorna duas variaveis, uma matriz com os dados de entrada e um vetor com os dados de saida: matriz_entrada, vetor_saida
    '''
    
    tamanho_matriz = len(serie) - janela 
    
    matriz_entrada = []
    for i in range(tamanho_matriz):
        matriz_entrada.append([0.0] * janela)
    
    vetor_saida = []
    for i in range(len(matriz_entrada)):
        matriz_entrada[i] = serie[i:i+janela]
        vetor_saida.append(serie[i+janela])
        
    return np.asarray(matriz_entrada), np.asarray(vetor_saida)

    
class Particionar_series:
    def __init__(self, serie=[0], divisao=[0,0,0], janela=5, norm=False):
        '''
        classe para manipular a serie temporal
        :param serie: vetor, com a serie temporal utilizada para treinamento 
        :param divisao: lista com porcentagens, da seguinte forma [pct_treinamento_entrada, pct_treinamento_saida, pct_validacao_entrada, pct_validacao_saida]
        :param janela: quantidade de lags usados para modelar os padroes de entrada da ELM
        '''
        
        self.min = 0
        self.max = 0
        self.serie = serie
        
        if(norm):
            self.serie = self.Normalizar(serie)
        
        self.janela = janela
        
        if(len(divisao) != 3):
            return "Erro no tamanho da particao!"
            
        self.pct_train = divisao[0]
        self.pct_val = divisao[1]
        self.pct_test = divisao[2]
       
        self.index_train = 0
        self.index_val = 0
        
        if(len(self.serie)>1):
            self.matriz_entrada, self.vetor_saida = Janela_tempo(self.serie, self.janela)
        
    def Part_train(self):
        '''
        metodo que retorna somente a parte de treinamento da serie temporal
        :return: retorna uma lista com: [entrada_train, saida_train]
        '''
        
        self.index_train = self.pct_train * len(self.vetor_saida)
        self.index_train = int(round(self.index_train))
        
        entrada_train = np.asarray(self.matriz_entrada[:self.index_train])
        saida_train = np.asarray(self.vetor_saida[:self.index_train])
        
        return entrada_train, saida_train
    
    def Part_val(self):
        '''
        metodo que retorna somente a parte de validacao da serie temporal
        :return: retorna uma lista com: [entrada_val, saida_val]
        '''
        
        self.index_val = self.pct_val * len(self.vetor_saida)
        self.index_val = int(round(self.index_val))
        self.index_val = self.index_train + self.index_val
        
        entrada_val = np.asarray(self.matriz_entrada[self.index_train:self.index_val])
        saida_val = np.asarray(self.vetor_saida[self.index_train:self.index_val])
        
        return entrada_val, saida_val
    
    def Part_test(self):
        '''
        metodo que retorna somente a parte de teste da serie temporal
        :return: retorna uma lista com: [entrada_teste, saida_teste]
        '''
          
        entrada_teste = np.asarray(self.matriz_entrada[self.index_val:])
        saida_teste = np.asarray(self.vetor_saida[self.index_val:])
        
        return entrada_teste, saida_teste
    
    def Normalizar(self, serie):
        '''
        metodo que normaliza a serie temporal em um intervalo de [0, 1] 
        :param serie: serie temporal que sera remodelada
        :return: retorna a serie normalizada 
        '''
        
        self.min = copy.deepcopy(np.min(serie))
        self.max = copy.deepcopy(np.max(serie))
        
        serie_norm = []
        for e in serie:
            valor = (e - self.min)/(self.max - self.min)
            serie_norm.append(valor)
        
        return serie_norm  
     
    def Desnormalizar(self, serie):
        '''
        metodo que retira a normalizacao da serie e a coloca em escala original 
        :param serie: serie temporal que sera remodelada
        :return: retorna a serie na escala original  
        '''

        serie_norm = []
        for e in serie:
            valor = e * (self.max - self.min) + self.min
            serie_norm.append(valor)

        return serie_norm  
        
def main():
    serie = [1, 2, 4, 7 ,11, 25, 30, 1, 2, 4, 7 ,11, 25, 30, 1, 2, 4, 7 ,11, 25, 30, 1, 2, 4, 7 ,11, 25, 30, 5]
    divisao = [0.6, 0.2, 0.2]
    
    particao = Particionar_series(serie, divisao, 4, norm=False)
    
    '''
    print(particao.serie)
    print(particao.min)
    print(particao.max)
    print(particao.Desnormalizar(particao.serie))
    print(serie)
    '''
    
    [train_entrada, train_saida] = particao.Part_train()
    [val_entrada, val_saida] = particao.Part_val()
    [test_entrada, test_saida] = particao.Part_test()
    
    print(train_entrada)
    print()
    print(val_entrada)
    print()
    print(test_entrada)
    
    print(train_saida)
    print()
    print(val_saida)
    print()
    print(test_saida)
    
    
if __name__ == "__main__":
    main()



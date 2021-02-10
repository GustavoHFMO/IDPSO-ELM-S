#-*- coding: utf-8 -*-
import random
import numpy as np
import copy
import pandas as pd
import matplotlib.pyplot as plt
from numpy import array
from ferramentas.Particionar_series import Particionar_series
from regressores.ELM import ELMRegressor
from sklearn.metrics import mean_absolute_error
from ferramentas.Importar_dataset import Datasets

#limites
mi = 100

#variaveis auxiliares
contador = 0
fitness = 0
grafico = []
lista_MSE = []

class Particulas():
    '''
    classe para criar as particulas
    '''
    pass

class IDPSO_ELM():
    def __init__(self, serie, divisao, janela, qtd_neuronios):
        '''
        Contrutor para o algoritmo de treinamento do ELM, o algoritmo utilizado e o IDPSO
        :param serie: vetor, com a serie temporal utilizada para treinamento 
        :param divisao: lista com porcentagens, da seguinte forma [pct_treinamento_entrada, pct_treinamento_saida, pct_validacao_entrada, pct_validacao_saida]
        :param janela: quantidade de lags usados para modelar os padroes de entrada da ELM
        :param qtd_neuronios: quantidade de neuronios da camada escondida da ELM
        '''
        
        #serie = vetor
        #divisao = lista com três porcentagens para divisao da serie
        #janela = quantidade de lags
        #qtd_neuronios = quantidade de neuronios
        
        #tratando os dados
        #dataset = [treinamento_entrada, treinamento_saida, validacao_entrada, valic_saida, teste_entrada, teste_saida]
        dataset = self.Tratamento_Dados(serie, divisao, janela)
        
        self.dataset = dataset
        self.qtd_neuronios = qtd_neuronios
        self.best_elm = []
        
        #default IDPSO
        self.linhas = self.dataset[0].shape[1] + 1
        self.numero_dimensoes =  self.linhas * qtd_neuronios
        
        self.iteracoes = 1000
        self.numero_particulas = 30
        self.inercia = 0.5
        self.inercia_final = 0.3
        self.c1 = 2.4
        self.c2 = 1.4
        self.crit_parada = 50
        self.particulas = []
        self.gbest = []
        
        self.particulas_ordenadas = [0] * self.numero_particulas
        self.sensores = [0] * self.numero_particulas
        
        self.tx_espalhar = 0
        
    def Parametros_IDPSO(self, iteracoes, numero_particulas, inercia_inicial, inercia_final, c1, c2, Xmax, crit_parada):
        '''
        Metodo para alterar os parametros basicos do IDPSO 
        :param iteracoes: quantidade de geracoes para o treinamento 
        :param numero_particulas: quantidade de particulas usadas para treinamento
        :param inercia: inercial inicial para treinamento
        :param inercia_final: inercia final para variacao
        :param c1: coeficiente cognitivo
        :param c2: coeficiente pessoal
        :param crit_parada: criterio de parada para limitar a repeticao nao melhora do gbest
        '''
        
        self.iteracoes = iteracoes
        self.numero_particulas = numero_particulas
        self.inercia_inicial = inercia_inicial
        self.inercia_final = inercia_final
        self.c1 = c1
        self.c2 = c2
        self.crit_parada = crit_parada
        
        self.particulas_ordenadas = [0] * self.numero_particulas
        self.sensores = [0] * self.numero_particulas
        
        self.xmax = Xmax
        self.xmin = -Xmax
        self.posMax = Xmax
        self.posMin = self.xmin
    
    def Tratamento_Dados(self, serie, divisao, janela):
        '''
        Metodo para dividir a serie temporal em treinamento e validacao 
        :param serie: vetor, com a serie temporal utilizada para treinamento 
        :param divisao: lista com porcentagens, da seguinte forma [pct_treinamento_entrada, pct_treinamento_saida, pct_validacao_entrada, pct_validacao_saida]
        :param janela: quantidade de lags usados para modelar os padroes de entrada da ELM
        :return: retorna uma lista com os seguintes dados [treinamento_entrada, treinamento_saida, validacao_entrada, validacao_saida]
        '''
        
        #tratamento dos dados
        particao = Particionar_series(serie, divisao, janela)
        [train_entrada, train_saida] = particao.Part_train()
        [val_entrada, val_saida] = particao.Part_val()
        [test_entrada, test_saida] = particao.Part_test()
        
        #inserindo os dados em uma lista
        lista_dados = []
        lista_dados.append(train_entrada)
        lista_dados.append(train_saida)
        lista_dados.append(val_entrada)
        lista_dados.append(val_saida)
        lista_dados.append(test_entrada)
        lista_dados.append(test_saida)
        
        #retornando o valor
        return lista_dados
      
    def Criar_Particula(self):
        '''
        Metodo para criar todas as particulas do enxame de forma aleatoria 
        '''
        
        global contador, fitness, grafico, lista_MSE
        contador = 0
        fitness = 0
        grafico = []
        lista_MSE = []
        
        for i in range(self.numero_particulas):
            p = Particulas()
            p.posicao = np.random.randn(1, self.numero_dimensoes)
            p.posicao = p.posicao[0]
            p.fitness = self.Funcao(p.posicao)
            p.velocidade = array([0.0 for i in range(self.numero_dimensoes)])
            p.best = p.posicao
            p.fit_best = p.fitness
            p.c1 = self.c1
            p.c2 = self.c2
            p.inercia = self.inercia
            p.phi = 0
            self.particulas.append(p)
        
        self.gbest = self.particulas[0]
        
    def Funcao(self, posicao):
        '''
        Metodo para calcular a funcao objetivo do IDPSO, nesse caso a funcao e a previsao de um ELM 
        :param posicao: posicao seria os pesos da camada de entrada e os bias da rede ELM 
        :return: retorna o MSE obtido da previsao de uma ELM
        '''
        
        # instanciando um modelo ELM
        ELM = ELMRegressor(self.qtd_neuronios)
        
        # modelando a dimensao das particulas para serem usadas 
        posicao = posicao.reshape(self.linhas, self.qtd_neuronios)
        
        # ELM treinando com a entrada e a saida do conjunto de treinamento e tambem com os pesos da particula 
        ELM.Treinar(self.dataset[0], self.dataset[1], posicao)
        
        # Realizando a previsao para o conjunto de validacao
        prediction_val = ELM.Predizer(self.dataset[2])
        
        # computando o erro do conjunto de validacao
        MAE_val = mean_absolute_error(self.dataset[3], prediction_val)
        
        # retornando o erro do conjunto de validacao - forma de evitar o overfitting
        return MAE_val
    
    def Fitness(self):
        '''
        Metodo para computar o fitness de todas as particulas 
        '''
        
        for i in self.particulas:   
            i.fitness = self.Funcao(i.posicao)
        
    def Velocidade(self):
        '''
        Metodo para computar a velocidade de todas as particulas 
        '''
        
        calculo_c1 = 0
        calculo_c2 = 0
        
        for i in self.particulas:
            for j in range(len(i.posicao)):
                calculo_c1 = (i.best[j] - i.posicao[j])
                calculo_c2 = (self.gbest.posicao[j] - i.posicao[j])
                
                influecia_inercia = (i.inercia * i.velocidade[j])
                influencia_cognitiva = ((i.c1 * random.random()) * calculo_c1)
                influecia_social = ((i.c2 * random.random()) * calculo_c2)
              
                i.velocidade[j] = influecia_inercia + influencia_cognitiva + influecia_social
                
                if (i.velocidade[j] >= self.xmax):
                    i.velocidade[j] = self.xmax
                elif(i.velocidade[j] <= self.xmin):
                    i.velocidade[j] = self.xmin
              
    def Atualizar_particulas(self):
        '''
        Metodo para atualizar a posicao de todas as particulas 
        '''
        
        for i in self.particulas:
            for j in range(len(i.posicao)):
                i.posicao[j] = i.posicao[j] + i.velocidade[j]
                
                if (i.posicao[j] >= self.posMax):
                    i.posicao[j] = self.posMax
                elif(i.posicao[j] <= self.posMin):
                    i.posicao[j] = self.posMin

    def Atualizar_parametros(self, iteracao):
        '''
        Metodo para atualizar os parametros: inercia, c1 e c2 
        '''
        
        for i in self.particulas:
            parte1 = 0
            parte2 = 0
            
            for j in range(len(i.posicao)):
                parte1 = parte1 + self.gbest.posicao[j] - i.posicao[j]
                parte2 = parte2 + i.best[j] - i.posicao[j]
                
                if(parte1 == 0):
                    parte1 = 1
                if(parte2 == 0):
                    parte2 = 1
                    
            i.phi = abs(parte1/parte2)
            
        for i in self.particulas:
            ln = np.log(i.phi)
            calculo = i.phi * (iteracao - ((1 + ln) * self.iteracoes) / mi)
            i.inercia = ((self.inercia - self.inercia_final) / (1 + np.exp(calculo))) + self.inercia_final
            i.c1 = self.c1 * (i.phi ** (-1))
            i.c2 = self.c2 * i.phi
       
    def Pbest(self):
        '''
        Metodo para computar os pbests das particulas  
        '''
        
        for i in self.particulas:
            if(i.fit_best >= i.fitness):
                i.best = i.posicao
                i.fit_best = i.fitness

    def Gbest(self):
        '''
        Metodo para computar o gbest do enxame  
        '''
        
        for i in self.particulas:
            if(i.fitness <= self.gbest.fitness):
                self.gbest = copy.deepcopy(i)
    
    def Criterio_parada(self, i):
        '''
        Metodo para computar os criterios de parada, tanto o GL5 como o para nao melhora da melhor solucao
        :param i: atual geracao
        :return: retorna a indice da ultima geracao para parar o algoritmo  
        '''
        
        global contador, fitness, lista_MSE
        
        if(i == 0):
            fitness = copy.deepcopy(self.gbest.fitness)
            return i
        
        else:
            
            if(contador == self.crit_parada):
                #print("[%d] Sem melhora: " % (i) + " : ", self.gbest.fitness)
                return self.iteracoes
            
            if(fitness == self.gbest.fitness):
                contador+=1
                return i
            
            else:
                fitness = copy.deepcopy(self.gbest.fitness)
                contador = 0
                return i
    
    def Grafico_Convergencia(self, fitness, i):
        '''
        Metodo para apresentar o grafico de convergencia
        :param fitness: fitness da melhor particula da geracao
        :param i: atual geracao
        '''
        
        global grafico
        
        grafico.append(fitness)
        
        if(i == self.iteracoes):
            plt.plot(grafico)
            plt.title('Gráfico de Convergência')
            plt.show()
            
    def Predizer(self, Entradas, num_sensor = None, Saidas = None, grafico = None):
        '''
        Metodo para realizar a previsao com a melhor particula (ELM) do enxame e apresentar o grafico de previsao
        :param Entradas: padroes de entrada para realizar a previsao
        :param Saidas: padroes de saida para computar o MSE
        :param grafico: variavel booleana para ativar ou desativar o grafico de previsao
        :return: Retorna a predicao para as entradas apresentadas. Se as entradas e saidas sao apresentadas o MSE e retornado
        '''
        
        # se o numero do sensor não é passado então a predição é feita com o gbest
        if(num_sensor == None):
        
            #retorna somente a previsao
            if(Saidas == None):
                prediction = self.best_elm.Predizer(Entradas)
                return prediction
            else:
                prediction = self.best_elm.Predizer(Entradas)
                MSE = mean_absolute_error(Saidas, prediction)
                print('\n MSE: %.2f' %MSE)
    
                #apresentar grafico
                if(grafico == True):
                    plt.plot(Saidas, label = 'Real', color = 'Blue')
                    plt.plot(prediction, label = 'Previsão', color = 'Red')
                    plt.title('MSE: %2f' %MSE)
                    plt.legend()
                    plt.tight_layout()
                    plt.show()
                
                return MSE
        
        else:
            # realizando a previsao com o sensor passado
            prediction = self.sensores[num_sensor].Predizer(Entradas)
            return prediction
        
    def Realizar_Previsao(self, Entradas):
        '''
        Metodo para realizar a previsao com a melhor particula (ELM) do enxame
        :param Entradas: padroes de entrada para realizar a previsao
        :return: Retorna a predicao para as entradas apresentadas
        '''
        
        return self.best_elm.Predizer(Entradas)
    
    def Ordenar_particulas(self):
        '''
        Metodo para ordenar as particulas por menor fitness  
        '''
        
        self.particulas_ordenadas = copy.deepcopy(self.particulas)
        
        for i in range(0, len(self.particulas_ordenadas)-1):
            imin = i
            for j in range(i+1, len(self.particulas_ordenadas)):
                if(self.particulas_ordenadas[j].fitness < self.particulas_ordenadas[imin].fitness):
                    imin = j
            aux = self.particulas_ordenadas[imin]
            self.particulas_ordenadas[imin]  = self.particulas_ordenadas[i]
            self.particulas_ordenadas[i] = aux
            
            
        '''
        # codigo para saber se as particulas estão ordenadas
        acuracias = []
        for i in range(len(self.particulas_ordenadas)):
            acuracias.append(self.particulas_ordenadas[i].fitness)
            
        plt.plot(acuracias)
        plt.show()
        '''
             
    def Obter_sensores(self):
        '''
        Metodo para obter os sensores (particulas) ordenados 
        '''
        
        self.Ordenar_particulas()
        
        for x, i in enumerate(self.particulas_ordenadas):
            ELM = ELMRegressor(self.qtd_neuronios)
            posicao = i.posicao.reshape(self.linhas, self.qtd_neuronios)
            ELM.Treinar(self.dataset[0], self.dataset[1], posicao)
            self.sensores[x] = ELM
            
        self.best_elm = self.sensores[0]
        
    def Treinar(self):
        '''
        Metodo para treinar a rede ELM com o IDPSO 
        '''
        
        self.Criar_Particula()       
        
        i = 0
        while(i < self.iteracoes):
            i = i + 1
            
            self.Fitness()
            self.Gbest()
            self.Pbest()
            self.Velocidade()
            self.Atualizar_parametros(i)
            self.Atualizar_particulas()
            i = self.Criterio_parada(i)
            
            #print("[%d]" % (i) + " : ", self.gbest.fitness)
            #self.Grafico_Convergencia(self.gbest.fitness, i)
        
        self.Obter_sensores()
        self.Melhor_ELM()
        
    def Melhor_ELM(self):
        '''
        método para retornar o melhor ELM
        '''
        
        ELM = ELMRegressor(self.qtd_neuronios)
        posicao = self.gbest.posicao.reshape(self.linhas, self.qtd_neuronios)
        ELM.Treinar(self.dataset[0], self.dataset[1], posicao)
            
        self.best_elm = ELM
        
    def Espalhar_particulas(self):
        '''
        método para apagar as informações de parte do enxame, essa parte é definida por uma porcentagem: self.tx_espalhar
        '''
        
        qtd = len(self.particulas)
        tx = int(qtd * self.tx_espalhar) 
        #print("taxa:", tx)
        escolhidos = []
        
        for i in range(tx):
            
            j = self.Gerar_numero(qtd-1, escolhidos)
            escolhidos.append(j)
            #print("indices gerados: [", j, "]")
        
            self.particulas[j].posicao = np.random.randn(1, self.numero_dimensoes)
            self.particulas[j].posicao = self.particulas[j].posicao[0]
            self.particulas[j].fitness = self.Funcao(self.particulas[j].posicao)
            self.particulas[j].velocidade = array([0.0 for i in range(self.numero_dimensoes)])
            self.particulas[j].best = self.particulas[j].posicao
            self.particulas[j].fit_best = self.particulas[j].fitness
            self.particulas[j].c1 = self.c1
            self.particulas[j].c2 = self.c2
            self.particulas[j].inercia = self.inercia
            self.particulas[j].phi = 0
            
        global contador
        contador = 0
    
    def Gerar_numero(self, qtd, escolhidos):
        '''
        Método para gerar um numero aleatorio de forma que os valores não se repitam
        '''
        
        j = np.random.randint(0, qtd)
        
        if(j in escolhidos):
            
            return self.Gerar_numero(qtd, escolhidos)
            
        else:
            return j
    
    def Retreinar(self):
        '''
        Metodo para retreinar um modelo 
        '''
        
        self.Espalhar_particulas()
        
        i = 0
        while(i < self.iteracoes):
            i = i + 1
            
            self.Fitness()
            self.Gbest()
            self.Pbest()
            self.Velocidade()
            self.Atualizar_parametros(i)
            self.Atualizar_particulas()
            i = self.Criterio_parada(i)
            
            #print("[%d]" % (i) + " : ", self.gbest.fitness)
            #self.Grafico_Convergencia(self.gbest.fitness, i)
        
        self.Obter_sensores()
    
    def Atualizar_bestmodel(self, novo):
        '''
        método para atualizar o melhor regressor do enxame
        '''
        #print("modelo novo: ", novo)
        #print("modelo antigo: ", self.best_elm)
        #print("comparacao antes da copia: ", (self.best_elm == novo))
        self.best_elm = novo
        #print("comparacao depois da copia: ", (self.best_elm == novo))
        #print("modelo atualizado: ", self.best_elm)
        
        
        #print("esperar")
        
def main():
    
    high = 2
    low = 3
    dataset = pd.read_csv("../series/WIN$N_Daily_201601040000_201905300000.csv", header=None, sep='\t')[low][1:].values
    dataset = np.array(dataset, dtype=float)
    #dataset = np.append(dataset, 98225)
    dataset = np.append(dataset, 96870)
    particao = Particionar_series(dataset, [0.0, 0.0, 0.0], 0)
    serie = particao.Normalizar(dataset)
    
    divisao_dataset = [0.6, 0.3, 0.1]
    qtd_neuronios = 10
    janela_tempo = 4
    
    previsoes = []
    for i in range(30):
        print(i)
             
        ################################### IDPSO-ELM ##########################################
        modelo = IDPSO_ELM(serie, divisao_dataset, janela_tempo, qtd_neuronios)
        modelo.Parametros_IDPSO(100, 15, 0.8, 0.4, 2, 2, 0.3, 20)
        modelo.Treinar()  
        
        ##### previsao de amanha #####
        ultimo_padrao = modelo.dataset[4][-1]
        ultimo_padrao = np.append(ultimo_padrao, modelo.dataset[5][-1])
        ultimo_padrao = ultimo_padrao[1:]
        ultimo_padrao = ultimo_padrao.reshape((1,janela_tempo))
        
        previsao_amanha = modelo.Predizer(ultimo_padrao)
        previsoes.append(previsao_amanha)
        ########################################################################################
        
    media = [np.mean(previsoes)]
    mediana = [np.median(previsoes)]
    
    print("IDPSO-ELM: (media) ", particao.Desnormalizar(media))
    print("IDPSO-ELM: (mediana) ", particao.Desnormalizar(mediana))

    #plt.plot(particao.Desnormalizar(modelo.Predizer(modelo.dataset[4])), label='Predicted')
    #plt.plot(particao.Desnormalizar(modelo.dataset[5]), label='Ground Truth')
    #plt.legend()
    #plt.show()
    
    '''
    # treinando a rede com o conjunto de treinamento
    previsao_train = ELM.Predizer(ELM.dataset[0])
    MAE = mean_absolute_error(ELM.dataset[1], previsao_train)
    print('ELM - Train MAE: ', MAE)
    
    previsao_val = ELM.Predizer(ELM.dataset[2])
    MAE = mean_absolute_error(ELM.dataset[3], previsao_val)
    print('ELM - Val MAE: ', MAE)
    
    previsao_test = ELM.Predizer(ELM.dataset[4])
    MAE = mean_absolute_error(ELM.dataset[5], previsao_test)
    print('ELM - Test MAE: ', MAE)
    
    plt.plot(ELM.dataset[1])
    plt.plot(previsao_train)
    plt.show()
    
    plt.plot(ELM.dataset[3])
    plt.plot(previsao_val)
    plt.show()
    
    plt.plot(ELM.dataset[5])
    plt.plot(previsao_test)
    plt.show()
    '''
    
if __name__ == "__main__":
    main()
    



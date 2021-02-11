#-*- coding: utf-8 -*-
'''
Created on 6 de fev de 2017

By Gustavo Oliveira
Universidade Federal de Pernambuco, Recife, Brasil
E-mail: ghfmo@cin.ufpe.br

OLIVEIRA, Gustavo HFM et al. Time series forecasting in the presence of concept drift: A pso-based approach. 
In: 2017 IEEE 29th International Conference on Tools with Artificial Intelligence (ICTAI). 
IEEE, 2017. p. 239-246.
https://ieeexplore.ieee.org/document/8371949
'''

from ferramentas.Janela_deslizante import Janela
from ferramentas.Importar_dataset import Datasets
from ferramentas.Particionar_series import Particionar_series
from metricas.Metricas_deteccao import Metricas_deteccao
from regressores.ELM import ELMRegressor
from graficos.Graficos_execucao import Grafico
from detectores.FEDD import FEDD
import time
import numpy as np
from sklearn.metrics import mean_absolute_error

divisao_dataset = [0.8, 0.2, 0]

class ELM_FEDD():
    def __init__(self, dataset, n=300, lags=5, qtd_neuronios=10, Lambda=0.2, w=0.25, c=0.25):
        '''
        construtor do algoritmo que detecta a mudanca de ambiente por meio do comportamento das particulas
        :param dataset: serie temporal que o algoritmo vai executar
        :param qtd_train_inicial: quantidade de exemplos para o treinamento inicial
        :param tamanho_janela: tamanho da janela de caracteristicas para identificar a mudanca
        :param n: tamanho do n para reavaliar o metodo de deteccao
        :param lags: quantidade de lags para modelar as entradas da RNA
        :param qtd_neuronios: quantidade de neuronios escondidos da RNA
        :param limite: contador para verificar a mudanca
        '''
        
        self.dataset = dataset
        self.n = n
        self.lags = lags
        self.qtd_neuronios = qtd_neuronios
        
        self.Lambda = Lambda
        self.w = w
        self.c = c
        
        self.tecnica = "ELM-FEDD"
    
    def Executar(self, grafico = None):
        '''
        Metodo para executar o procedimento do algoritmo
        :param grafico: variavel booleana para ativar ou desativar o grafico
        :return: retorna 5 variaveis: [falsos_alarmes, atrasos, falta_deteccao, MAPE, tempo_execucao]
        '''

        ################################################################################################################################################
        ################################# CONFIGURACAO DO DATASET ######################################################################################
        ################################################################################################################################################
        
        #dividindo os dados da dataset dinamica para treinamento_inicial inicial e para uso do stream din�mico
        treinamento_inicial = self.dataset[0:self.n]
        stream = self.dataset[self.n:]
    
        ################################################################################################################################################
        ################################# PERIODO ESTATICO #############################################################################################
        ################################################################################################################################################
        
        #criando e treinando um enxame_vigente para realizar as previsoes
        ELM = ELMRegressor(self.qtd_neuronios)
        ELM.Tratamento_dados(treinamento_inicial, divisao_dataset, self.lags)
        ELM.Treinar(ELM.train_entradas, ELM.train_saidas)
        
        #ajustando com os dados finais do treinamento a janela de predicao
        janela_predicao = Janela()
        janela_predicao.Ajustar(ELM.train_entradas[len(ELM.train_entradas)-1:])
        predicao = ELM.Predizer(janela_predicao.dados)
        
        #janela com o atual conceito, tambem utilizada para armazenar os dados de retreinamento
        janela_caracteristicas = Janela()
        janela_caracteristicas.Ajustar(treinamento_inicial)
        
        #atualizar por fedd
        fedd = FEDD(self.Lambda, self.w, self.c)
        final = len(janela_caracteristicas.dados)
        qtd = 3
        vetor_caracteristicas_0 = fedd.FE(janela_caracteristicas.dados[:final-qtd])
        
        distancias_vetor = []
        for i in range(1, qtd):
            vetor_caracteristicas = fedd.FE(janela_caracteristicas.dados[i:final-qtd+i])
            distancia = fedd.computar_distancia(vetor_caracteristicas_0, vetor_caracteristicas)
            distancias_vetor.append(distancia)
            
        fedd.armazenar_conceito(vetor_caracteristicas_0, np.mean(distancias_vetor), np.std(distancias_vetor))
        
        ################################################################################################################################################
        ################################# PERIODO DINAMICO #############################################################################################
        ################################################################################################################################################
        
        #variavel para armazenar o erro do stream
        erro_stream = 0
        #variavel para armazenar as deteccoes
        deteccoes = []
        #variavel para armazenar os alarmes
        alarmes = []
        #variavel para armazenar o tempo inicial
        start_time = time.time()
        
        #vetor para armazenar a predicoes_vetor
        if(grafico == True):
            predicoes_vetor = [None] * len(stream)
            erro_stream_vetor = [None] * len(stream)
        
        #variavel auxiliar 
        mudanca_ocorreu = False
            
        #entrando no stream de dados
        for i in range(1, len(stream)):
            
            #computando o erro
            loss = mean_absolute_error(stream[i:i+1], predicao)
            erro_stream += loss
    
            #adicionando o novo dado a janela de predicao
            janela_predicao.Add_janela(stream[i])
                
            #realizando a nova predicao com a nova janela de predicao
            predicao = ELM.Predizer(janela_predicao.dados)

            #salvando o erro e a predição            
            if(grafico == True):                
                #salvando o erro 
                erro_stream_vetor[i] = loss
                #salvando a predicao
                predicoes_vetor[i] = predicao

            #entrando no loop para monitorar as caracteristicas
            if(mudanca_ocorreu == False):
                
                #atualizar a janela de caracteristicas do FEDD
                janela_caracteristicas.Add_janela(stream[i])
                    
                #realizando a diferenciacao no vetor de caracteristicas atuais
                vetor_caracteristicas_atual = fedd.FE(janela_caracteristicas.dados[0])    
                    
                #computar a distancia entre os vetores de caracteristicas
                distancia = fedd.computar_distancia(fedd.vetor_caracteristicas_inicial, vetor_caracteristicas_atual)   
                #distancias_vetor.append(distancia) 
                 
                #atualizando o media_zt e desvio_zt
                fedd.atualizar_ewma(distancia, i+1)
                #zt_vetor.append(fedd.zt)
                
                #monitorando o erro
                string_fedd = fedd.monitorar()
                
                #verificar se houve mudanca
                if(string_fedd == fedd.alerta):
                    if(grafico == True):
                        print("[%d] Alarme" % (i))
                    alarmes.append(i)
                
                if(string_fedd == fedd.mudanca):
                    if(grafico == True):
                        print("[%d] Detectou uma mudanca" % (i))
                    deteccoes.append(i)
                    
                    mudanca_ocorreu = True
            
            else:
                
                if(i < deteccoes[len(deteccoes)-1] + self.n):                    
                    #adicionando a nova instancia na janela de caracteristicas
                    janela_caracteristicas.Add_janela(stream[i])
                    
                else:
                    
                    #atualizando o enxame_vigente preditivo
                    ELM = ELMRegressor(self.qtd_neuronios)
                    ELM.Tratamento_dados(janela_caracteristicas.dados[0], divisao_dataset, self.lags)
                    ELM.Treinar(ELM.train_entradas, ELM.train_saidas)
                    
                    #ajustando a janela de previsao
                    janela_predicao = Janela()
                    janela_predicao.Ajustar(ELM.train_entradas[len(ELM.train_entradas)-1:])
                    predicao = ELM.Predizer(janela_predicao.dados)
                        
                    #atualizar por fedd
                    fedd = FEDD(self.Lambda, self.w, self.c)
                    final = len(janela_caracteristicas.dados[0])
                    qtd = 3
                    vetor_caracteristicas_0 = fedd.FE(janela_caracteristicas.dados[0][:final-qtd])
                    
                    distancias_vetor = []
                    for i in range(1, qtd):
                        vetor_caracteristicas = fedd.FE(janela_caracteristicas.dados[0][i:final-qtd+i])
                        distancia = fedd.computar_distancia(vetor_caracteristicas_0, vetor_caracteristicas)
                        distancias_vetor.append(distancia)
                        
                    fedd.armazenar_conceito(vetor_caracteristicas_0, np.mean(distancias_vetor), np.std(distancias_vetor))
                    
                    #variavel para voltar para o loop principal
                    mudanca_ocorreu = False
                            
        #variavel para armazenar o tempo final
        end_time = time.time()
        
        #computando as metricas de deteccao
        mt = Metricas_deteccao()
        [falsos_alarmes, atrasos] = mt.resultados(stream, deteccoes, self.n)
       
        #computando a acuracia da previsao ao longo do fluxo de dados
        MAE = erro_stream/len(stream)
        
        #computando o tempo de execucao
        tempo_execucao = (end_time-start_time)
        
        # variables to store 
        self.target = stream
        self.predictions = predicoes_vetor
        
        if(grafico == True):
            print(self.tecnica)
            print("Alarmes:")
            print(alarmes)
            print("Deteccoes:")
            print(deteccoes)
            print("Falsos Alarmes: ", falsos_alarmes)
            print("Atrasos: ", atrasos)
            print("MAE: ", MAE)
            print("Tempo de execucao: ", tempo_execucao)
        
        #plotando o grafico de erro
        if(grafico == True):
            g = Grafico()
            g.Plotar_graficos(stream, predicoes_vetor, deteccoes, alarmes, erro_stream_vetor, self.n, atrasos, falsos_alarmes, tempo_execucao, MAE, nome=self.tecnica)
                           
        #retorno do metodo
        return falsos_alarmes, atrasos, MAE, tempo_execucao
    
def main():
    
    #instanciando o dataset
    dtst = Datasets('dentro')
    dataset = dtst.Leitura_dados(dtst.bases_reais(3), csv=True)
    particao = Particionar_series(dataset, [0.0, 0.0, 0.0], 0)
    dataset = particao.Normalizar(dataset)    
                
    #instanciando o algoritmo com sensores
    n = 300
    lags = 5
    qtd_neuronios = 10 
    w = 0.25
    c = 0.25
    alg = ELM_FEDD(dataset, n, lags, qtd_neuronios, 0.2, w, c)
    
    #colhendo os resultados
    alg.Executar(grafico=True)
    
    
if __name__ == "__main__":
    main()  
    
        
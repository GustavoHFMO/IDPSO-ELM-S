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
from detectores.DDM import DDM
from regressores.ELM import ELMRegressor
from graficos.Graficos_execucao import Grafico
from sklearn.metrics import mean_absolute_error
import time
import numpy as np

divisao_dataset = [0.8, 0.2, 0]

class ELM_DDM():
    def __init__(self, dataset, n=300, lags=5, qtd_neuronios=10, w=8, c=8):
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
        
        self.w = w
        self.c = c
        
        self.tecnica = "ELM-DDM"
    
    def Computar_estatisticas_DDM_desvio(self, vetor_caracteristicas, lags, ELM):
        '''
        Metodo para computar a deteccao de mudanca do erro por meio do DDM com desvio padrão tradicional
        :param vetor_caracteristicas: vetor com uma amostra da serie temporal que sera avaliada para verificar a mudanca
        :param lags: quantidade de lags para modelar as entradas da RNA
        :param enxame: enxame utilizado para verificar a mudanca
        :return: retorna a media ou o comportamento do enxame em relacao ao vetor de caracteristicas
        '''
        #particionando o vetor de caracteristicas para usar para treinar 
        particao = Particionar_series(vetor_caracteristicas, divisao_dataset, lags)
        [caracteristicas_entrada, caracteristicas_saida] = particao.Part_train()
        
        #realizando as previsoes e armazenando as acuracias 
        predicao_caracteristica = ELM.Predizer(caracteristicas_entrada)
        
        erros = []
        
        for i in range(len(caracteristicas_saida)):
            erro = mean_absolute_error(caracteristicas_saida[i:i+1], predicao_caracteristica[i:i+1])
            erros.append(erro)
            
        return np.min(erros), np.std(erros), erros
    
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
        treinamento_inicial = self.dataset[0:self.n]        stream = self.dataset[self.n:]
    
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
        
        #atualizar por ECDD
        [erro_min, desvio_min, erros] = self.Computar_estatisticas_DDM_desvio(janela_caracteristicas.dados, self.lags, ELM)
        ddm = DDM(self.w, self.c)
        ddm.armazenar_conceito(erro_min, desvio_min, erros)
        
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

            if(grafico == True):                
                #salvando o erro 
                erro_stream_vetor[i] = loss
                #salvando a predicao
                predicoes_vetor[i] = predicao
                
            if(mudanca_ocorreu == False):
                    
                #monitorando o erro
                string_ddm = ddm.monitorar(loss, i)
                
                #verificar se houve mudanca
                if(string_ddm == ddm.alerta):
                    if(grafico == True):
                        print("[%d] Alarme" % (i))
                    alarmes.append(i)
                    
                #procedimento pos mudanca
                if(string_ddm == ddm.mudanca):
                    if(grafico == True):
                        print("[%d] Detectou uma mudanca" % (i))
                    deteccoes.append(i)
                    
                    #zerando a janela de treinamento
                    janela_caracteristicas.Zerar_Janela()
                
                    mudanca_ocorreu = True
            
            else:
                
                if(len(janela_caracteristicas.dados) < self.n):
                    
                    #adicionando a nova instancia na janela de caracteristicas
                    janela_caracteristicas.Increment_Add(stream[i])
                            
                else:
                    
                    #atualizando o enxame_vigente preditivo
                    ELM = ELMRegressor(self.qtd_neuronios)
                    ELM.Tratamento_dados(janela_caracteristicas.dados, divisao_dataset, self.lags)
                    ELM.Treinar(ELM.train_entradas, ELM.train_saidas)
                    
                    #ajustando a janela de previsao
                    janela_predicao = Janela()
                    janela_predicao.Ajustar(ELM.train_entradas[len(ELM.train_entradas)-1:])
                    predicao = ELM.Predizer(janela_predicao.dados)
                        
                    #atualizar por ECDD
                    [erro_min, desvio_min, erros] = self.Computar_estatisticas_DDM_desvio(janela_caracteristicas.dados, self.lags, ELM)
                    ddm = DDM(self.w, self.c)
                    ddm.armazenar_conceito(erro_min, desvio_min, erros)
                    
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
    w = 8
    c = 8
    alg = ELM_DDM(dataset, n, lags, qtd_neuronios, w, c)
    
    #colhendo os resultados
    alg.Executar(grafico=True)
    
    
if __name__ == "__main__":
    main()      
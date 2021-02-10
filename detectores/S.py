#-*- coding: utf-8 -*-
'''
Created on 10 de mar de 2017

@author: gusta
'''

from ferramentas.Particionar_series import Particionar_series
from sklearn.metrics import mean_absolute_error
from detectores.ECDD import ECDD
import numpy as np

class S():
    def __init__(self, qtd_sensores, w, c):
        '''
        Método para criar um modelo do ECDD
        :param Lambda: float com o valor de lambda
        :param w: float com o nivel de alarme
        :param l: float com o nivel de deteccao
        '''
        
        self.w = w
        self.c = c
        self.ativadores = [False] * qtd_sensores
        self.qtd_sensores = qtd_sensores
    
    def armazenar_conceito(self, dados, lags, enxame):
        '''
        Este metodo tem por objetivo armazenar o conceito de varios sensores 
        :param dados: dados referentes ao conceito
        :param lags: quantidade de lags para formatar os dados
        :param enxame: enxame com todos os sensores
        '''
        
        self.sensores_ecdds = []
        for i in range(len(enxame.sensores)):
            [media, desvio] = self.Computar_Media(dados, lags, enxame.sensores[i])
            ecdd = ECDD(0.2, self.w, self.c)
            ecdd.armazenar_conceito(media, desvio)
            self.sensores_ecdds.append(ecdd)
            
    def monitorar(self, erro, t, voto):
        '''
        Este metodo tem por objetivo monitorar um erro para saber se ele mudou de distribuicao
        :param erro: double com o erro para ser verificado
        :param t: instante de tempo
        :return: retorna verdadeiro caso haja uma mudança de conceito
        '''
        
        self.ativadores = [False] * self.qtd_sensores 
        for j in range(self.qtd_sensores):
            self.sensores_ecdds[j].atualizar_ewma(erro, t)
            string_ecdd = self.sensores_ecdds[j].monitorar()
                    
            if(string_ecdd == self.sensores_ecdds[j].mudanca):
                self.ativadores[j] = True
            else:
                self.ativadores[j] = False
                    
        if(voto):
            return self.condicao_voto(self.ativadores)
        else:
            return self.condicao_padrao(self.ativadores)
        
    def monitorar_gbest(self):
        '''
        Este metodo tem por objetivo monitorar somente a melhor particula do enxame
        :param erro: double com o erro para ser verificado
        :param t: instante de tempo
        '''
        # monitorar somente a melhor particula do enxame
        string_ecdd = self.sensores_ecdds[0].monitorar()
                
        # verificando se esta em estado de alerta
        if(string_ecdd == self.sensores_ecdds[0].alerta):
            return True
        
    def condicao_padrao(self, vetor):
        '''
        condicao padrão do método IDPSO-ELM-S, se todos concordarem retorna verdadeiro, caso não, falso
        :return: variavel booelana
        '''
        
        if(all(vetor)):
            return True
        else:
            return False
        
    def condicao_voto(self, vetor):
        '''
        condicao com voto majoritario, se mais de metade confirmar então há uma mudança, caso não, falso
        :return: variavel booelana
        '''
        
        if(vetor.count(True) > int(self.qtd_sensores/2)):
            return True
        else:
            return False
         
    def Computar_Media(self, vetor_caracteristicas, lags, sensor):
        '''
        Metodo para computar a deteccao de mudanca na serie temporal por meio do comportamento das particulas
        :param vetor_caracteristicas: vetor com uma amostra da serie temporal que sera avaliada para verificar a mudanca
        :param lags: quantidade de lags para modelar as entradas da RNA
        :param modelo: enxame utilizado para computar as estatisticas dos sensores
        :param sensor: particula utilizada como sensor
        :return: retorna a media e o desvio padrao do sensor para o vetor de caracteristicas: estatistica[media, desvio]
        '''

        particao = Particionar_series(vetor_caracteristicas, [1, 0, 0], lags)
        [caracteristicas_entrada, caracteristicas_saida] = particao.Part_train()
        predicao_caracteristica = sensor.Predizer(caracteristicas_entrada)
        
        #calculando a estatistica do sensor
        acuracias = []
        for i in range(len(caracteristicas_entrada)):
            erro = mean_absolute_error(caracteristicas_saida[i:i+1], predicao_caracteristica[i:i+1])
            acuracias.append(erro)
            
        estatistica = [0] * 2
        estatistica[0] = np.mean(acuracias)
        estatistica[1] = np.std(acuracias)
        
        return estatistica
    
def main():
    print("Sem nada")
    
    
if __name__ == "__main__":
    main()
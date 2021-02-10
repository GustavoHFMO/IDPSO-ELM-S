#-*- coding: utf-8 -*-
'''
Created on 10 de mar de 2017

@author: gusta
'''

from ferramentas.Particionar_series import Particionar_series
from detectores.ECDD import ECDD
from sklearn.metrics import mean_absolute_error
import numpy as np

class B():
    def __init__(self, limite, w, c):
        '''
        Método para criar um modelo do ECDD
        :param Lambda: float com o valor de lambda
        :param w: float com o nivel de alarme
        :param l: float com o nivel de deteccao
        '''
        
        self.limite = limite
        self.w = w
        self.c = c        
        self.media_zero = 0
        self.desvio_zero = 0
        self.contador = 0
        self.ecdd = ECDD(0.2, w, c)
    
    def armazenar_conceito(self, dados, lags, enxame):
        
        comportamento = self.Atualizar_comportamento_media(dados, lags, enxame)
        '''
        Este método tem por objetivo armazenar um conceito de um erro 
        :param MI0: média dos erros
        :param SIGMA0: desvio dos erros
        '''

        self.media_zero = comportamento[0]
        self.desvio_zero = comportamento[1]
        self.ecdd.armazenar_conceito(self.media_zero, self.desvio_zero)
        
    def atualizar_ewma(self, MI0, i):
        #atualizando o ewma
        self.ecdd.atualizar_ewma(MI0, i)
            
    def monitorar(self, dados, real, enxame, i):
        '''
        Este metodo tem por objetivo monitorar um erro para saber se ele mudou de distribuicao
        :param erro: double com o erro para ser verificado
        :param t: instante de tempo
        :return: verdadeiro para mudanca, falso para nao mudanca
        '''
        #computando o comportamento para a janela de predicao, para somente uma instancia - media e desvio padrão
        comportamento_atual = self.Computar_comportamento_atual(dados, real, enxame)
                
        #atualizando o ewma
        self.atualizar_ewma(comportamento_atual[0], i)
                
        #monitorando o modulo ecdd
        string_ecdd = self.ecdd.monitorar()
                
        #somando o contador
        if(string_ecdd == self.ecdd.mudanca):
            self.contador = self.contador + 1
        elif((string_ecdd == self.ecdd.alerta) or (string_ecdd == self.ecdd.nada)):
            self.contador = 0
                    
        #procedimento pos mudanca
        if(self.contador == self.limite):
            self.contador = 0 
            return True
        else:
            return False
    
    def Atualizar_comportamento_media(self, vetor_caracteristicas, lags, enxame):
        '''
        Metodo para computar a deteccao de mudanca na serie temporal por meio do comportamento das particulas
        :param vetor_caracteristicas: vetor com uma amostra da serie temporal que sera avaliada para verificar a mudanca
        :param lags: quantidade de lags para modelar as entradas da RNA
        :param enxame: enxame utilizado para verificar a mudanca
        :return: retorna a media ou o comportamento do enxame em relacao ao vetor de caracteristicas
        '''
        
        #particionando o vetor de caracteristicas para usar para treinar 
        particao = Particionar_series(vetor_caracteristicas, [1, 0, 0], lags)
        [caracteristicas_entrada, caracteristicas_saida] = particao.Part_train()
        
        #variavel para salvar as medias das predicoes
        medias = []
        
        #realizando as previsoes e armazenando as acuracias 
        for i in range(enxame.numero_particulas):
            predicao_caracteristica = enxame.sensores[i].Predizer(caracteristicas_entrada)
            MAE = mean_absolute_error(caracteristicas_saida, predicao_caracteristica)
            medias.append(MAE)          

        #salvando a media e desvio padrao das acuracias
        comportamento = [0] * 2
        comportamento[0] = np.mean(medias)
        comportamento[1] = np.std(medias)
            
        return comportamento
    
    def Computar_comportamento_atual(self, dados, real, enxame):
        '''
        Metodo para computar o comportamento para os dados atuais
        :param dados: dados para realizar a previsao um passo a frente
        :param enxame: enxame utilizado para verificar a mudanca
        :return: retorna o comportamento para o instante atual
        '''
        
        #variavel para salvar as medias das predicoes
        medias = []
        
        #realizando as previsoes e armazenando as acuracias 
        for i in range(enxame.numero_particulas):
            predicao_caracteristica = enxame.sensores[i].Predizer(dados)
            MAE = mean_absolute_error(real, predicao_caracteristica)
            medias.append(MAE)          

        #salvando a media e desvio padrao das acuracias
        comportamento = [0] * 2
        comportamento[0] = np.mean(medias)
        comportamento[1] = np.std(medias)
            
        return comportamento   
    
def main():
    print("Sem nada")
    
    
if __name__ == "__main__":
    main()
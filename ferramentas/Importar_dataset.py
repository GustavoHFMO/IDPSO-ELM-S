# -*- coding: UTF-8 -*-

'''
Created on 8 de fev de 2017

@author: gusta
'''
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

#caminho onde se encontram as bases xlsx

class Datasets():
    def __init__(self, alocacao='fora'):
        if(alocacao == 'fora'):
            self.caminho_bases = 'series'
        elif(alocacao == 'dentro'):
            self.caminho_bases = '../series'
        
    '''
    classe que armazena as series com drifts
    '''

    def Leitura_dados(self, caminho, excel = None, csv = None, column = None):
        '''
        Metodo para fazer a leitura dos dados
        :param caminho: caminho da base que sera importada
        :return: retorna a serie temporal que o caminho direciona
        '''
        #leitura da serie dinamica
        
        if(excel == True):
            print(caminho)
            stream = pd.read_excel(caminho, header = None)
            stream = stream[0]
            stream = stream.values
            return stream
        
        elif(csv == True):
            
            if(column == 1):
                print(caminho)
                stream = pd.read_csv(caminho, header = None)
                stream = stream[1]
                stream = stream.values
                return stream
            
            else:
                print(caminho)
                stream = pd.read_csv(caminho, header = None)
                stream = stream[0]
                stream = stream.values
                return stream
    
    def bases_linear_graduais(self, numero):
        '''
        Metodo para mostrar o caminho das bases lineares graduais
        :param tipo: tipo das series lineares, podem ser dos tipos: 1, 2 e 3
        :param numero: numero das variacoes das series, pode variar entre [30,49]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/lineares_grad_abt/graduais/lin-grad' + str(numero)+ '.csv') 
        return base
    
    def bases_linear_abruptas(self, numero):
        '''
        Metodo para mostrar o caminho das bases lineares abruptas
        :param tipo: tipo das series lineares, podem ser dos tipos: 1, 2 e 3
        :param numero: numero das variacoes das series, pode variar entre [30,49]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/lineares_grad_abt/abruptas/lin-abt' + str(numero)+ '.csv') 
        return base
    
    def bases_nlinear_graduais(self, numero):
        '''
        Metodo para mostrar o caminho das bases nao lineares graduais
        :param tipo: tipo das series lineares, podem ser dos tipos: 1, 2 e 3
        :param numero: numero das variacoes das series, pode variar entre [30,49]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/nlineares_grad_abt/graduais/nlin-grad' + str(numero)+ '.csv')
        return base
    
    def bases_nlinear_abruptas(self, numero):
        '''
        Metodo para mostrar o caminho das bases nao lineares abruptas
        :param tipo: tipo das series lineares, podem ser dos tipos: 1, 2 e 3
        :param numero: numero das variacoes das series, pode variar entre [30,49]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/nlineares_grad_abt/abruptas/nlin-abt' + str(numero)+ '.csv') 
        return base
    
    def bases_hibridas(self, numero):
        '''
        Metodo para mostrar o caminho das bases hibridas
        :param numero: numero das variacoes das series, pode variar entre [1, 10]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/hibridas/hib-' + str(numero) + '.csv')
         
        return base
    
    def bases_lineares(self, numero):
        '''
        Metodo para mostrar o caminho das bases hibridas
        :param numero: numero das variacoes das series, pode variar entre [1, 10]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/lineares/lin-' + str(numero) + '.csv')
         
        return base
    
    def bases_nlineares(self, numero):
        '''
        Metodo para mostrar o caminho das bases hibridas
        :param numero: numero das variacoes das series, pode variar entre [1, 10]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/nlineares/nlin-' + str(numero) + '.csv')
         
        return base
    
    def bases_sazonais(self, numero):
        '''
        Metodo para mostrar o caminho das bases hibridas
        :param numero: numero das variacoes das series, pode variar entre [1, 10]
        :return: retorna o caminho da base
        '''
        
        base = (self.caminho_bases + '/Series Geradas Permanentes/sazonais/saz-' + str(numero) + '.csv')
         
        return base
    
    def bases_reais(self, tipo):
        '''
        Metodo para mostrar o caminho das bases reais
        :param tipo: tipo de séris utilizada
        :1 = Dow 30
        :2 = Nasdaq
        :3 = S&P 500
        :return: retorna o caminho da base
        '''
        
        base = 0
        
        if(tipo == 1):
            base = (self.caminho_bases + '/Series Reais/Dow.csv')
        if(tipo == 2):
            base = (self.caminho_bases + '/Series Reais/Nasdaq.csv')
        if(tipo == 3):
            base = (self.caminho_bases + '/Series Reais/S&P500.csv')
        
        return base
    
    def bases_reais_drift(self, tipo, retorno = None):
        '''
        Metodo para mostrar o caminho das bases reais
        :param tipo: tipo de séris utilizada
        :1 = Dow-drift
        :2 = S&P500-drift
        :return: retorna o caminho da base
        '''
        
        if(retorno == None):
            if(tipo == 1):
                base = (self.caminho_bases + '/Series Reais/Down-1972to1975.csv')
            if(tipo == 2):
                base = (self.caminho_bases + '/Series Reais/S&P500-1986to2002.csv')
                
        elif(retorno == True):
            if(tipo == 1):
                base = (self.caminho_bases + '/Series Reais/Dow-drift.csv')
            if(tipo == 2):
                base = (self.caminho_bases + '/Series Reais/S&P500-drift.csv')
            
                
        return base
    
    def calculo_retorno(self, prices, nome):
        '''
        método para transformar uma serie em uma serie de retorno
        :param: prices: serie com os valores iniciais
        :param: nome: nome em que a nova serie sera salva
        :return: retorna a serie de retorno
        '''
        
        import numpy as np
        
        serie = []
        for i in range(1, len(prices)):
            a = 100 * np.log(prices[i]/prices[i-1])
            serie.append(a)
        
        df = pd.DataFrame(data = serie)
        df.to_csv(nome+".csv", header=False, index=False)
        
        return serie 

    def Plotar_serie(self, serie):
        '''
        metodo para plotar o grafico de qualquer serie que for passada
        :param: serie: vetor de inteiros, serie a ser plotada
        '''
        
        plt.plot(serie)
        plt.show()

    def Plotar_series_reais_drift(self, dtst, tamanho, fonte, linha, alfa):
        '''
        metodo para plotar as series reais com drifts conhecidos
        :param: dtst: instancia dessa classe
        :param: tamanho: inteiro, tamanho do bloco em que fica os labels
        :param: fonte: inteiro, tamanho da fonte dos labels
        :param: linha: inteiro, tamanho da linha que mostra o drift
        '''
        
        
        ####################################################### series reais com drift #########################################
        figura = plt.figure()
        
        deteccoes = [124, 307, 510]
        caminho = dtst.bases_reais_drift(1, retorno = True)
        dataset = dtst.Leitura_dados(caminho, csv=True)
        plt.plot(dataset)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        plt.xticks(fontsize=tamanho, rotation=45)
        plt.yticks(fontsize=tamanho)
        plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
        plt.show()
        
        '''
        g1 = figura.add_subplot(2, 2, 1)
        g1.plot(dataset)
        for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g1.set_title("Dow Jones Industrial Average - Daily Return", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
        '''
        
        deteccoes = [124, 307, 510]
        caminho = dtst.bases_reais_drift(1)
        dataset = dtst.Leitura_dados(caminho, csv=True, column = 1)
        plt.plot(dataset)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
        plt.show()
        
        '''
        g1 = figura.add_subplot(2, 2, 3)
        g1.plot(dataset)
        for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g1.set_title("Dow Jones Industrial Average", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
        #plt.show()
        '''
        
        ######################################################################################################
                
        #figura = plt.figure()
        
        deteccoes = [448, 508, 1715, 2826, 4119]
        caminho = dtst.bases_reais_drift(2, retorno = True)
        dataset = dtst.Leitura_dados(caminho, csv=True)
        plt.plot(dataset)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
        plt.show()
        
        '''
        g2 = figura.add_subplot(2, 2, 2)
        g2.plot(dataset)
        for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g2.set_title("S&P500 - Daily Return", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
        '''
        
        deteccoes = [448, 508, 1715, 2826, 4119]
        caminho = dtst.bases_reais_drift(2)
        dataset = dtst.Leitura_dados(caminho, csv=True, column = 1)
        plt.plot(dataset)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
        plt.show()
        
        '''
        g2 = figura.add_subplot(2, 2, 4)
        g2.plot(dataset)
        for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g2.set_title("S&P500", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
        plt.show()
        '''
        #############################################################################################################################
    
    def Plotar_series_financeiras(self, dtst, tamanho, fonte, linha):
        '''
        metodo para plotar as series reais financeiras
        :param: dtst: instancia dessa classe
        :param: tamanho: inteiro, tamanho do bloco em que fica os labels
        :param: fonte: inteiro, tamanho da fonte dos labels
        :param: linha: inteiro, tamanho da linha que mostra o drift
        '''
        
        figura = plt.figure()
        
        ####################################################### series reais com drift #########################################
        caminho = dtst.bases_reais(1)
        dataset = dtst.Leitura_dados(caminho, csv=True)
        plt.plot(dataset)
        plt.show()
        
        '''
        g1 = figura.add_subplot(2, 2, 1)
        g1.plot(dataset)
        g1.set_title("Dow Jones Industrial Average", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
        '''
        
        caminho = dtst.bases_reais(2)
        dataset = dtst.Leitura_dados(caminho, csv=True)
        plt.plot(dataset)
        plt.show()
        
        '''
        g1 = figura.add_subplot(2, 2, 2)
        g1.plot(dataset)
        g1.set_title("Nasdaq", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
        '''
        
        caminho = dtst.bases_reais(3)
        dataset = dtst.Leitura_dados(caminho, csv=True)
        plt.plot(dataset)
        plt.show()
        
        '''
        g1 = figura.add_subplot(2, 2, 3)
        g1.plot(dataset)
        g1.set_title("S&P500", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
        plt.show()
        '''
        #############################################################################################################################
        
    def Plotar_series_artificiais(self, dtst, tamanho, fonte, linha, alfa):
        '''
        metodo para plotar as series artificiais com drifs
        :param: dtst: instancia dessa classe
        :param: tamanho: inteiro, tamanho do bloco em que fica os labels
        :param: fonte: inteiro, tamanho da fonte dos labels
        :param: linha: inteiro, tamanho da linha que mostra o drift
        '''
        
        figura = plt.figure()
        
        ####################################################### series artificiais ##################################################
        for z in range(1):
            # codigo para printar varias series em uma imagem
            deteccoes = [2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000]
            i = z+1
            
            lin_grad = dtst.Leitura_dados(dtst.bases_linear_graduais(i), csv=True)
            lin_abt = dtst.Leitura_dados(dtst.bases_linear_abruptas(i), csv=True)
            nlin_grad = dtst.Leitura_dados(dtst.bases_nlinear_graduais(i), csv=True)
            nlin_abt = dtst.Leitura_dados(dtst.bases_nlinear_abruptas(i), csv=True)
            sazonais = dtst.Leitura_dados(dtst.bases_sazonais(i), csv=True)
            hibridas = dtst.Leitura_dados(dtst.bases_hibridas(i), csv=True)
        
        
            plt.plot(lin_grad)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
            plt.show()
            
            plt.plot(lin_abt)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)                    
            plt.show()
            
            plt.plot(nlin_grad)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
            plt.show()
            
            plt.plot(nlin_abt)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
            plt.show()
            
            plt.plot(sazonais)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
            plt.show()
            
            plt.plot(hibridas)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            plt.xticks(fontsize=tamanho, rotation=45)
            plt.yticks(fontsize=tamanho)
            plt.subplots_adjust(left=0.1, bottom=0.13, right=0.99, top=0.99, wspace=None, hspace=None)
            plt.show()
        
        
        
            '''
            tamanho = 10
            fonte = 11
            linha = 1
        
            g1 = figura.add_subplot(2, 3, 1)
            g1.plot(lin_grad)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            g1.set_title("Linear gradual time series", fontsize = fonte)
            plt.tick_params(labelsize= tamanho)
            
            g2 = figura.add_subplot(2, 3, 2)
            g2.plot(lin_abt)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            g2.set_title("Linear abrupt time series", fontsize = fonte)
            plt.tick_params(labelsize= tamanho)
            
            g3 = figura.add_subplot(2, 3, 3)
            g3.plot(nlin_grad)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            g3.set_title("Non-linear gradual time series", fontsize = fonte)
            plt.tick_params(labelsize= tamanho)
            
            g4 = figura.add_subplot(2, 3, 4)
            g4.plot(nlin_abt)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            g4.set_title("Non-linear abrupt time series", fontsize = fonte)
            
            g5 = figura.add_subplot(2, 3, 5)
            g5.plot(sazonais)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            g5.set_title("Linear seasonal time series", fontsize = fonte)
            plt.tick_params(labelsize= tamanho)
            
            g6 = figura.add_subplot(2, 3, 6)
            g6.plot(hibridas)
            for i in range(len(deteccoes)):
                plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
            g6.set_title("Hybrid time series", fontsize = fonte)
            
            plt.tick_params(labelsize= tamanho)
            plt.show()
            '''
        
    def Plotar_series_ICTAI(self, dtst, tamanho, fonte, linha, alfa):
        '''
        metodo para plotar as series artificiais usadas no artigo ICTAI
        :param: dtst: instancia dessa classe
        :param: tamanho: inteiro, tamanho do bloco em que fica os labels
        :param: fonte: inteiro, tamanho da fonte dos labels
        :param: linha: inteiro, tamanho da linha que mostra o drift
        '''
        
        # codigo para printar varias series em uma imagem
        deteccoes = [2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000]
        i = 1
            
        lineares = dtst.Leitura_dados(dtst.bases_lineares(i), csv=True)
        #gerador.Plotar(dataset, deteccoes)
            
        nlineares = dtst.Leitura_dados(dtst.bases_nlineares(i), csv=True)
        #gerador.Plotar(dataset, deteccoes)
            
        sazonais = dtst.Leitura_dados(dtst.bases_sazonais(i), csv=True)
        #gerador.Plotar(dataset, deteccoes)
        
        hibridas = dtst.Leitura_dados(dtst.bases_hibridas(i), csv=True)
        #gerador.Plotar(dataset, deteccoes)
        
        tamanho = 20
        fonte = 18
        linha = 2
        
        figura = plt.figure()
        g1 = figura.add_subplot(2, 2, 1)
        g1.plot(lineares)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g1.set_title("Linear time series", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
            
        g2 = figura.add_subplot(2, 2, 2)
        g2.plot(nlineares)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g2.set_title("Nonlinear time series", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
            
        g3 = figura.add_subplot(2, 2, 3)
        g3.plot(sazonais)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g3.set_title("Linear seasonal time series", fontsize = fonte)
        plt.tick_params(labelsize= tamanho)
            
        g4 = figura.add_subplot(2, 2, 4)
        g4.plot(hibridas)
        for i in range(len(deteccoes)):
            plt.axvline(deteccoes[i], linewidth=linha, color='r', alpha = alfa)
        g4.set_title("Hybrid time series", fontsize = fonte)
            
        plt.tick_params(labelsize= tamanho)
        plt.show()
            
def main():
    dtst = Datasets('dentro')
    
    tamanho_ticks = 16
    fonte = 20
    linha = 1
    alfa = 0.5
    
    dtst.Plotar_series_reais_drift(dtst, tamanho_ticks, fonte, linha, alfa)
    #dtst.Plotar_series_financeiras(dtst, tamanho_ticks, fonte, linha)
    #dtst.Plotar_series_artificiais(dtst, tamanho_ticks, fonte, linha, alfa)
    
    '''
    dataset = dtst.Leitura_dados(dtst.bases_reais_drift(1), csv=True, column = 1)
    plt.annotate(u'Mudança de Conceito', 
                 xy=(138, 575.35), 
                 xycoords='data', 
                 xytext=(60, -4), 
                 size = 16, 
                 textcoords='offset points', 
                 arrowprops=dict(facecolor='black',
                                 shrink=0.05))

    plt.yticks(fontsize = 16)
    plt.xticks(fontsize = 16)
    plt.ylabel('Observações', fontsize = 16)
    plt.xlabel('Tempo', fontsize = 16)
    plt.legend()
    plt.plot(dataset)
    plt.show()
    '''
    
if __name__ == "__main__":
    main()
    
#-*- coding: utf-8 -*-
'''
Created on 6 de fev de 2017

@author: gusta
'''
import numpy as np
from ferramentas.Importar_dataset import Datasets 

class Janela():
    def __init__(self):
        '''
        Classe para instanciar a janela deslizante 
        '''
        self.dados = []
        self.dados_mais = []
        
    def Ajustar(self, valores):
        '''
        Metodo para ajustar o tamanho da jenela deslizante 
        :param valores: valores para serem inseridos na janela
        '''
        
        self.dados = valores
        self.dados_mais = np.append([0], valores)
    
    def Add_janela(self, valor):
        '''
        Metodo para inserir na janela deslizante, o valor mais antigo sera excluido 
        :param valor: valor de entrada
        '''
        self.dados = self.Fila(self.dados, valor)
        self.dados_mais = self.Fila(self.dados_mais, valor)
        
    def Fila(self, lista, valor):
        '''
        metodo para adicionar um novo valor a um ndarray
        :param: lista: lista que será acrescida
        :param: valor: valor a ser adicionado
        :return: retorna a lista com o valor acrescido
        '''
        
        if(len(lista) == 1):
            aux2 = len(lista[0])
            aux = [0] * aux2
            aux[len(lista[0])-1] = valor
            aux[:len(aux)-1] = lista[0][1:]
            lista[0] = aux
            lista[0] = np.asarray(lista[0])
            lista[0] = np.column_stack(lista[0])
            
            return lista
            
        else:
            aux2 = len(lista)
            aux = [0] * aux2
            aux[len(lista)-1] = valor
            aux[:len(aux)-1] = lista[1:]
            lista = aux
            lista = np.asarray(lista)
            lista = np.column_stack(lista)
            
            return lista
        
    def Increment_Add(self, valor):
        '''
        Metodo para inserir mais dados na janela deslizante 
        :param valor: valor de entrada
        '''
        
        if(len(self.dados) > 0):
            aux = np.asarray(self.dados)
            aux = [0] * (len(self.dados)+1)
            aux[:len(self.dados)] = self.dados
            aux[len(self.dados)] = valor
            self.dados = aux
        else:
            self.dados.append(valor)
    
    def Zerar_Janela(self):
        self.dados = []
        
def main():
    dtst = Datasets()
    dataset = dtst.Leitura_dados(dtst.bases_linear_abruptas(1, 30))
    
    
    janela = Janela()
    janela.Ajustar(dataset[1:4])
    for i in range(5):
        janela.Add_janela(10)
        print(type(janela.dados))
        print(janela.dados)
    
    print("---------------------------------------------")
    
    janela2 = Janela()
    janela2.Ajustar(dataset[1:4])
    for i in range(5):
        janela2.Add_janela(10)
        print(type(janela2.dados))
        print(janela2.dados)
    
       
    '''
    janela = Janela()
    janela.Ajustar(dataset)
    start_time = time.time()
    for i in range(50):
        janela.Add_janela(10)
    print((time.time()-start_time))
    
    janela2 = Janela()
    janela2.Ajustar(dataset)
    start_time = time.time()
    for i in range(50):
        janela2.Fila_Add2(10)
        #print(janela2.dados)
    print((time.time()-start_time))
    '''
    
    '''
    start_time = time.time()
    for i in range(50):
        janela.Increment_Add(10)
    print((time.time()-start_time))
    print(janela.dados)

    janela2 = Janela()
    janela2.Ajustar(dataset[1:5])
    
    start_time = time.time()
    for i in range(50):
        janela2.Increment_Add2(10)
    print((time.time()-start_time))
    print(janela2.dados)
    '''
    
    '''
    janela = Janela()
    janela.Ajustar(dataset[1:5])
    print(janela.dados)
    janela.Add_janela(10)
    print(janela.dados)
    janela.Increment_Add(10)
    print(janela.dados)
    janela.Zerar_Janela()
    print(janela.dados)
    janela.Increment_Add(10)
    print(janela.dados)
    '''
    
    
if __name__ == "__main__":
    main() 
        
        
'''
Created on 6 de fev de 2017

By Gustavo Oliveira
Universidade Federal de Pernambuco, Recife, Brasil
E-mail: ghfmo@cin.ufpe.br

ALGORITHMS USED IN THE PAPER PUBLISHED BELOW:

OLIVEIRA, Gustavo HFM et al. Time series forecasting in the presence of concept drift: A pso-based approach. 
In: 2017 IEEE 29th International Conference on Tools with Artificial Intelligence (ICTAI). 
IEEE, 2017. p. 239-246.
https://ieeexplore.ieee.org/document/8371949
'''

# importando os algoritmos
from algoritmos_online.ELM_DDM import ELM_DDM
from algoritmos_online.ELM_ECDD import ELM_ECDD
from algoritmos_online.ELM_FEDD import ELM_FEDD
from algoritmos_online.IDPSO_ELM_B import IDPSO_ELM_B
from algoritmos_online.IDPSO_ELM_S import IDPSO_ELM_S

# importando libs para auxiliar na execucao dos metodos
from ferramentas.Importar_dataset import Datasets
from ferramentas.Particionar_series import Particionar_series

#1. importanto o dataset
dtst = Datasets()
dataset = dtst.Leitura_dados(dtst.bases_reais(1), csv=True)
dataset = Particionar_series().Normalizar(dataset)
        
    
#2. importanto o dataset
# ELM-DDM
elm_ddm = ELM_DDM(dataset)
elm_ddm.Executar(grafico=True)

# ELM-ECDD
elm_ecdd = ELM_ECDD(dataset)
elm_ecdd.Executar(grafico=True)

# ELM-FEDD
elm_fedd = ELM_FEDD(dataset)
elm_fedd.Executar(grafico=True)

# IDPSO-ELM-B
idpso_elm_b = IDPSO_ELM_B(dataset)
idpso_elm_b.Executar(grafico=True)

# IDPSO-ELM-S
idpso_elm_s = IDPSO_ELM_S(dataset)
idpso_elm_s.Executar(grafico=True)






    

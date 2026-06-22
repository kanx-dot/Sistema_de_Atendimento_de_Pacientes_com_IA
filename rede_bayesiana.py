#IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

#==============================================================#

#ESTRUTURA DA REDE

modelo_hospital = BayesianNetwork([
    ('Febre', 'Gravidade'),
    ('Saturacao', 'Gravidade'),
    ('Pressao_Arterial', 'Gravidade'),
    ('Frequencia_Cardiaca', 'Gravidade'),
    ('Nivel_Dor', 'Gravidade'),
    ('Nivel_Consciencia', 'Gravidade'),
    ('Idade_Comorbidade', 'Gravidade'),
])

#Temos um cenário aqui onde cada variável de probabilidade nas CPDs é dividido entre 0 (Normal) e 1 (Alterado/Sintomático)
#Por exemplo, 70% dos pacientes que chegam ao hospital não possuem febre, i.e, está com febre normal, enquanto 30% delas chegam com febre alta. E por aí vai

cpd_febre = TabularCPD(variable='Febre', variable_card=2, values=[[0.7], [0.3]])
cpd_saturacao = TabularCPD(variable='Saturacao', variable_card=2, values=[[0.85], [0.15]])
cpd_pressao = TabularCPD(variable='Pressao_Arterial', variable_card=2, values=[[0.80], [0.20]])
cpd_frequencia = TabularCPD(variable='Frequencia_Cardiaca', variable_card=2, values=[[0.75], [0.25]])
cpd_dor = TabularCPD(variable='Nivel_Dor', variable_card=2, values=[[0.60], [0.40]])
cpd_risco_base = TabularCPD(variable='Idade_Comorbidade', variable_card=2, values=[[0.65], [0.35]])

#CPD para Nível de Consciência -> 0 = Consciente/Orientado, 1 = Confuso/Letárgico/Inconsciente
cpd_consciencia = TabularCPD(variable='Nivel_Consciencia', variable_card=2, values=[[0.90], [0.10]])

#Considerando que temos 7 variáveis, teremos, no total, 2^7 = 128 colunas com possíveis combinações de sintomas que irão pesar na urgência do caso
#Realizamos, então, um For para preencher matematicamente o CPD de Gravidade, definindo o quanto cada combinação de sintomas pesa na saúde do paciente

num_combinacoes = 2**7  #128
prob_gravidade_alta = []

for i in range(num_combinacoes):
    
    bits = [int(x) for x in format(i, '07b')]  #<--- Converte o índice em binário para saber quais sintomas estão ativos (1) ou inativos (0)
    
    #O nível de consciência e saturação são críticos, podemos dar um peso maior a eles
    score = (bits[0]*1 + bits[1]*3 + bits[2]*1.5 + bits[3]*1.5 + bits[4]*1 + bits[5]*1 + bits[6]*3)
    max_score = 12.0
    
    #Mapeia o score para uma probabilidade entre 0.01 e 0.99
    p_alta = 0.01 + (score / max_score) * 0.98
    p_alta = min(0.99, max_score) if p_alta > 0.99 else p_alta
    prob_gravidade_alta.append(p_alta)

prob_gravidade_baixa = [1.0 - p for p in prob_gravidade_alta]

cpd_gravidade = TabularCPD(
    variable='Gravidade', 
    variable_card=2,
    values=[prob_gravidade_baixa, prob_gravidade_alta],
    evidence=['Febre', 'Saturacao', 'Pressao_Arterial', 'Frequencia_Cardiaca', 'Nivel_Dor', 'Idade_Comorbidade', 'Nivel_Consciencia'],
    evidence_card=[2, 2, 2, 2, 2, 2, 2]
)

modelo_hospital.add_cpds(
    cpd_febre, cpd_saturacao, cpd_pressao, cpd_frequencia, 
    cpd_dor, cpd_risco_base, cpd_consciencia, cpd_gravidade
)

assert modelo_hospital.check_model(), "Erro na consistência das tabelas!"

#Definimos o Motor de Inferência agora
inferencia = VariableElimination(modelo_hospital)

def calcular_probabilidade_gravidade(sintomas_paciente): #<--- Esta função recebe os sintomas do paciente e retorna a probabilidade para que seu quadro seja grave
    resultado = inferencia.query(variables=['Gravidade'], evidence=sintomas_paciente)
    return float(resultado.values[1])

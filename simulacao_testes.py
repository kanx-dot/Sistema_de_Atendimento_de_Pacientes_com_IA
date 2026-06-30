import copy
import random
from paciente import Paciente
from buscar_fila import a_estrela
from rede_bayesiana import obter_probabilidade_gravidade


def criar_paciente_sintomatico(nome, sintomas):
    probabilidade = obter_probabilidade_gravidade(sintomas)
    return Paciente(nome, probabilidade)


def simular_fifo(pacientes_iniciais, tempo_atendimento=10): #<---- o que a FIFO deve fazer: Atender os pacientes estritamente na ordem em que estão na lista.
    pacientes = copy.deepcopy(pacientes_iniciais)
    atendidos = []
    custo_g_total = 0
    
    while pacientes:
        paciente_atendido = pacientes.pop(0)
        atendidos.append(paciente_atendido)
        
        for p in pacientes:
            p.tempo_espera += tempo_atendimento
            custo_g_total += p.calcular_risco()
            
    return atendidos, custo_g_total


def simular_gulosa(pacientes_iniciais, tempo_atendimento=10): #<--- o que a Gulosa deve fazer: Atender sempre quem tem a maior probabilidade de gravidade alta, ignorando há quanto tempo os outros estão esperando.
    pacientes = copy.deepcopy(pacientes_iniciais)
    atendidos = []
    custo_g_total = 0
    
    while pacientes:
        pacientes.sort(key=lambda x: x.p_gravidade_alta, reverse=True)
        
        paciente_atendido = pacientes.pop(0)
        atendidos.append(paciente_atendido)
        
        for p in pacientes:
            p.tempo_espera += tempo_atendimento
            custo_g_total += p.calcular_risco()
            
    return atendidos, custo_g_total


#===================================================================================================================#


#==== Cenário de Experimento Prático ====
if __name__ == "__main__":
    print("="*60)
    print("        SIMULADOR INTEGRADO: REDE BAYESIANA + A*     ")
    print("="*60)


# -----------------------------------------------------------------
                        #1. CENÁRIO PEQUENO 
# -----------------------------------------------------------------
    print("\n>>> CONFIGURANDO CENÁRIO PEQUENO (6 PACIENTES FIXOS) <<<")

#Criamos os pacientes fictícios para podermos realizar nossas simulações!!
    
cenario_pequeno = [
        criar_paciente_sintomatico("João (Muito Grave)", {'Febre': 1, 'Saturacao': 1, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 1}),
        criar_paciente_sintomatico("Maria (Leve)",        {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 1, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        criar_paciente_sintomatico("Pedro (Moderado)",   {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 0, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        criar_paciente_sintomatico("Ana (Grave)",         {'Febre': 0, 'Saturacao': 1, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        criar_paciente_sintomatico("Lucas (Leve)",       {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 0, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        criar_paciente_sintomatico("Carla (Moderado)",    {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0})
    ]
    
_, custo_fifo_p = simular_fifo(cenario_pequeno)
_, custo_gulosa_p = simular_gulosa(cenario_pequeno)
ordem_astar_p, custo_astar_p = a_estrela(cenario_pequeno)
    
print(f"🔴 Custo FIFO: {custo_fifo_p:.2f} ")
print(f'🟡 Custo GULOSA: {custo_gulosa_p:.2f}')
print(f'🔵 Custo A*: {custo_astar_p:.2f}')
print(f"\n📋 Ordem de chamada do A*: {[p.nome for p in ordem_astar_p]}")

# -----------------------------------------------------------------
                        #2. CENÁRIO MÉDIO
#------------------------------------------------------------------

print("\n" + "="*60)
print(">>> CONFIGURANDO CENÁRIO MÉDIO (20 PACIENTES FIXOS) <<<")
    
   
#Considerando o fato de ser um número substancialmente maior que 5, caso pudéssemos de qualquer jeito,
#haveria a chance do código demorar muito para rodar, então, para o Cenário Médio, vamos organizar a fila inicial do paciente mais greve
#para o menos grave, maximizando a eficiência da função heurística h(n), permitindo que o A* rode mais rápido, mesmo com 20 pacientes
     
dados_pacientes_fixos = [
        ("Roberto (Crítico)",    {'Febre': 1, 'Saturacao': 1, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 1}),
        ("Fernanda (Crítica)",   {'Febre': 1, 'Saturacao': 1, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Ricardo (Grave)",      {'Febre': 0, 'Saturacao': 1, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Beatriz (Grave)",      {'Febre': 1, 'Saturacao': 1, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 1}),
        ("Marcos (Grave)",       {'Febre': 0, 'Saturacao': 1, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 1}),
        ("Juliana (Moderado+)",  {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Gabriel (Moderado+)",  {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Amanda (Moderado)",    {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 0, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Rodrigo (Moderado)",   {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Camila (Moderado)",    {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Larissa (Moderado-)",  {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 0, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Bruno (Moderado-)",    {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 0, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Vinicius (Leve+)",     {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 0, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Leticia (Leve+)",      {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Paula (Leve)",         {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 1, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Daniel (Leve)",        {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 1, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Thiago (Leve)",        {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 0, 'Idade_Comorbidade': 1, 'Nivel_Consciencia': 0}),
        ("Aline (Muito Leve)",   {'Febre': 1, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 0, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Vanessa (Muito Leve)", {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 1, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
        ("Clara (Sem Sintomas)", {'Febre': 0, 'Saturacao': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 0, 'Idade_Comorbidade': 0, 'Nivel_Consciencia': 0}),
    ]
    
cenario_medio = []
for nome, sintomas in dados_pacientes_fixos:
        paciente_instanciado = criar_paciente_sintomatico(nome, sintomas)
        cenario_medio.append(paciente_instanciado)
        
_, custo_fifo_m = simular_fifo(cenario_medio, tempo_atendimento=1)
_, custo_gulosa_m = simular_gulosa(cenario_medio, tempo_atendimento=1)
ordem_astar_m, custo_astar_m = a_estrela(cenario_medio, tempo_atendimento=1)
    
print(f"🔴 Custo FIFO: {custo_fifo_m:.2f} ")
print(f"🟡 Custo GULOSA: {custo_gulosa_m:.2f}")
print(f"🔵 Custo A*: {custo_astar_m:.2f}")
print(f"\n📋 Ordem de chamada do A*: {[p.nome for p in ordem_astar_m]}")
print("="*60)

import copy
from paciente import Paciente
from busca_fila import a_estrela
from rede_bayesiana import obter_probabilidade_gravidade

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

#Criamos os pacientes fictícios para podermos realizar nossas simulações!! No Cenário Pequeno, onde é mais razoável ir a mão, digitamos individualmente cada caso. No Médio, usamos um for para gerar pacientes simulados aleatoriamente,
#considerando o N° maior de pacientes no total em comparação à apenas 6
    
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
    
    print(f"🔴 Custo FIFO: {custo_fifo_p:.2f} | 🟡 Custo GULOSA: {custo_gulosa_p:.2f} | 🔵 Custo A*: {custo_astar_p:.2f}")
    print(f"Ordem de chamada do A*: {[p.nome for p in ordem_astar_p]}")

# -----------------------------------------------------------------
            #2. CENÁRIO MÉDIO (Automatizado com LOOP FOR)
#------------------------------------------------------------------

print("\n" + "="*60)
    print(">>> CONFIGURANDO CENÁRIO MÉDIO (25 PACIENTES ALEATÓRIOS) <<<")
    
    cenario_medio = []
    chaves = ['Febre', 'Saturacao', 'Pressao_Arterial', 'Frequencia_Cardiaca', 'Nivel_Dor', 'Idade_Comorbidade', 'Nivel_Consciencia']
    
    for i in range(1, 26):
        sintomas_aleatorios = {s: random.choice([0, 1]) for s in chaves}
        paciente_random = criar_paciente_sintomatico(f"Paciente_{i}", sintomas_aleatorios)
        cenario_medio.append(paciente_random)
        
    #Rodando as simulações do Cenário Médio...
    _, custo_fifo_m = simular_fifo(cenario_medio)
    _, custo_gulosa_m = simular_gulosa(cenario_medio)
    _, custo_astar_m = a_estrela(cenario_medio)
    
    print(f"🔴 Custo FIFO: {custo_fifo_m:.2f} | 🟡 Custo GULOSA: {custo_gulosa_m:.2f} | 🔵 Custo A*: {custo_astar_m:.2f}")
    print("="*60)

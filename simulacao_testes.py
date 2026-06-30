import copy
from paciente import Paciente
from busca_fila import a_estrela

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


# --- Cenário de Experimento Prático ---
if __name__ == "__main__":
    print("="*60)
    print("        SIMULADOR DE TRIAGEM HOSPITALAR INTELIGENTE       ")
    print("="*60)
    
#Criamos, agora, pacientes fictícios para podermos realizar nossas simulações!!
    
    cenario_pacientes = [
        Paciente("Carlos (Grave)", 0.95),
        Paciente("Ana (Moderada)", 0.45),
        Paciente("Bruno (Leve)", 0.10),
        Paciente("Daniela (Grave)", 0.88),
        Paciente("Eduardo (Moderado)", 0.50)
    ]
    
    print("\n[CONFIGURAÇÃO] Pacientes Iniciais na Fila:")
    for p in cenario_pacientes:
        print(f" - {p.nome} | P(Gravidade Alta): {p.p_gravidade_alta:.2%}")
    print("-" * 60)

    # 1. Executando FIFO
    ordem_fifo, custo_fifo = simular_fifo(cenario_pacientes)
    print(f"\n🟢 RESULTADO FIFO:")
    print(f" Ordem: { [p.nome for p in ordem_fifo] }")
    print(f" Risco Acumulado Total: {custo_fifo:.4f}")

    # 2. Executando GULOSA
    ordem_gulosa, custo_gulosa = simular_gulosa(cenario_pacientes)
    print(f"\n🟡 RESULTADO GULOSA:")
    print(f" Ordem: { [p.nome for p in ordem_gulosa] }")
    print(f" Risco Acumulado Total: {custo_gulosa:.4f}")

    # 3. Executando A*
    ordem_astar, custo_astar = a_estrela(cenario_pacientes)
    print(f"\n🔵 RESULTADO A* (ÓTIMO):")
    print(f" Ordem: { [p.nome for p in ordem_astar] }")
    print(f" Risco Acumulado Total: {custo_astar:.4f}")
    
    print("\n" + "="*60)
    print("🎯 CONCLUSÃO PARA O RELATÓRIO:")
    reducao = ((custo_fifo - custo_astar) / custo_fifo) * 100
    print(f"O algoritmo A* reduziu o risco de deterioração em {reducao:.2f}% comparado ao FIFO!")
    print("="*60)

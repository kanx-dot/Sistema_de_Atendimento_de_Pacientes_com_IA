import copy
from paciente import Paciente
from rede_bayesiana import obter_probabilidade_gravidade
import heapq

#Da mesma forma como um estado em um A* tradicional é igual a coordenada/cidade atual, aqui, o estado será a situação atual da fila de pacientes
#Queremos saber quais pacientes foram atendidos e em que ordem

class EstadoBusca: #<--- Cria a lista de objetos Paciente (de paciente.py) que ainda estão na fila e os que já foram atendidos, criando custo_g que é o risco total acumulado do passado até aquele ponto
    def __init__(self, pacientes_restantes, atendidos=None, custo_g=0):
        self.pacientes_restantes = pacientes_restantes
        self.atendidos = atendidos if atendidos is not None else []
        self.custo_g = custo_g #custo g(n)
        self.custo_h = self.calcular_heuristica() #h(n)
        self.custo_f = self.custo_g + self.custo_h # #f(n) = g(n) + h(n)

    def calcular_heuristica(self): #Soma do risco atual de todos os pacientes ainda esperando na fila
        return sum(p.calcular_risco() for p in self.pacientes_restantes)
    
    def __lt__(self, outro):
        return self.custo_f < outro.custo_f


def a_estrela(pacientes_iniciais, tempo_atendimento=10): #<--- Algoritmo A* pra encontrar a ordem ótima de atendimento. tmepo_atendimento será o tempo em minutos que o médicao leva com cada paciente
    #1. Estado Inicial: todos os pacientes na fila, nenhum atendido, g = 0
    estado_inicial = EstadoBusca(pacientes_restantes=pacientes_iniciais)
    
    #Fila de prioridade (Min-Heap) para guardar os estados a serem expandidos
    fronteira = []
    heapq.heappush(fronteira, estado_inicial)
    visitados = set()
    nos_explorados = 0
    
    #Conjunto para evitar reprocessar estados idênticos (opcional, mas boa prática)
    visitados = set()

    while fronteira:
        #Pegamos o estado com o menor f(n)
        estado_atual = heapq.heappop(fronteira)
        nos_explorados += 1

        #Se não há mais ninguém para atender, achamos a ordem perfeita!
        if not estado_atual.pacientes_restantes:
            return estado_atual.atendidos, estado_atual.custo_g

        if nos_explorados > 150000: #<--- Vai ordenar os pacientes que sobraram do maior para o menor risco
            print("⚠️ Limite de busca atingido para evitar travamento. Ordenando o restante de forma otimizada.")
            resto_ordenado = sorted(estado_atual.pacientes_restantes, key=lambda x: x.p_gravidade_alta, reverse=True)
            ordem_estimada = estado_atual.atendidos + resto_ordenado
            return ordem_estimada, estado_atual.custo_g

        #Criar uma representação única do estado para não repetir caminhos
        assinatura_estado = tuple(p.nome for p in estado_atual.pacientes_restantes)
        if assinatura_estado in visitados:
            continue
        visitados.add(assinatura_estado)

        #Simular o atendimento de cada um dos pacientes restantes
        for i, paciente_escolhido in enumerate(estado_atual.pacientes_restantes):
            
            #Criamos cópias profundas para que um caminho não altere o dado do outro
            restantes_copia = copy.deepcopy(estado_atual.pacientes_restantes)
            #Remove o paciente escolhido da fila de espera
            paciente_atendido = restantes_copia.pop(i)
            
            atendidos_copia = copy.deepcopy(estado_atual.atendidos)
            atendidos_copia.append(paciente_atendido)

            # --- O CÁLCULO DO CUSTO DO PASSO ---
            #Enquanto o médico atende o 'paciente_atendido' por X minutos... o tempo de espera de TODOS os outros que ficaram na fila aumenta!
            custo_passo = 0
            for p in restantes_copia:
                p.tempo_espera += tempo_atendimento
                #Somamos o risco acumulado gerado por essa espera adicional
                custo_passo += p.calcular_risco()

            #Novo g(n) = g(n) anterior + custo gerado neste atendimento
            novo_custo_g = estado_atual.custo_g + custo_passo

            #Criar o novo estado gerado por essa ação
            proximo_estado = EstadoBusca(
                pacientes_restantes=restantes_copia,
                atendidos=atendidos_copia,
                custo_g=novo_custo_g
            )

            heapq.heappush(fronteira, proximo_estado)

    return None, float('inf')

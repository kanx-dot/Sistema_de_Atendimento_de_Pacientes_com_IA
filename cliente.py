#Objeto Cliente o qual saberá calcular seu próprio índice de deteriorização com o tempo

class Pacient:
  def __init__(self, nome, probabilidade_gravidade):
    self.nome = nome
    self.p_gravidade_alta = probabilidade_gravidade #<--- Valor vem direto do rede_bayesiana.py
    self.tempo_espera = 0 #<--- Tempo que o paciente já esperou no hosptal antes de ser atendido

  def calcular_risco(self): #Esta função irá  calcular o Risco de Deterioração baseado na fórmula linear do enunciado: Risco = P(gravidade_alta) * tempo_esperando
        return self.p_gravidade_alta * self.tempo_espera

    def __repr__(self):
        return f"{self.nome} (P: {self.p_gravidade_alta:.2f}, Tempo: {self.tempo_espera}min)"

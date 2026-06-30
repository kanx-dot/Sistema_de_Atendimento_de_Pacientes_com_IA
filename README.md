# Trabalho-de-Inteligência-Artificial-Aplicada---UFC

### Repositório do Trabalho de Inteligência Artificial Aplicada gerenciada pelo professor José Macedo, da Universidade Federal do Ceará. 
#
### ⚫ Realizada com: Linguagem Python 
#
### 🔧 Participantes do trabalho:
#### -   Kauã Cavalcante Modesto de Souza (570304)
#### -   Carlos Abimael (587010)
#### -   Luzia Vitória (566811)

---

### ⚫ O que estamos fazendo:
Construção de um sistema inteligente voltado para fins médicos, os quais se detalham na estimativa automática da gravidade de cada paciente com base de dados e decisão da melhor ordem de atendimento. Visamos facilitar a sobrecarga do sistema de saúde público atual por meio da criação deste algoritmo. 

---

### ⚫ Como o sistema funciona?
####O sistema é dividido em dois módulos principais que se comunicam diretamente:

* **Módulo 1 — Rede Bayesiana (`rede_bayesiana.py`):** Recebe as evidências clínicas do paciente (7 variáveis como Febre, Saturação de O2, Pressão Arterial, Frequência Cardíaca, Nível de Dor, Idade/Comorbidade e Nível de Consciência) e calcula a probabilidade matemática do paciente estar em estado grave.
* **Módulo 2 — Algoritmo A\* (`busca_astar.py`):** Utiliza a probabilidade calculada no Módulo 1 e o tempo em que o paciente está aguardando na fila para encontrar a sequência ideal de atendimento que **minimiza o risco acumulado total de deterioração clínica**.

---

### ⚫ Os arquivos

* `rede_bayesiana.py`: Definição da estrutura da Rede Bayesiana e do motor de inferência via `pgmpy`.
* `paciente.py`: Classe que define o objeto Paciente e o cálculo do risco de deterioração individual.
* `busca_astar.py`: Implementação do espaço de estados, função heurística admissível e o algoritmo de busca A\*.
* `simulador_testes.py`: Script central modular que configura os cenários de teste e compara o A\* com as abordagens **FIFO** e **Gulosa**.

### ⚫ Como executar o Projeto passo a passo

#### 1. Pré-requisitos
Certifique-se de ter o **Python 3.8+** instalado em sua máquina.

#### 2. Método .zip 
* 2.1. Entre no site GitHub do projeto e clique no botão verde Code e, depois, em ***download .Zip***
* 2.2. Vá na pasta de Downloads do seu computador e extraia o arquivo
* 2.3. Abra o VSCode, vá em Arquivo -> Abra Pasta e então selecione a pasta extraída

### 3. Executando o sistema
Execute no terminal `pip install pgmpy` e `python simulador_testes.py`



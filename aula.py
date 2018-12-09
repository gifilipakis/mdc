
from fractions import Fraction
from math import factorial
import random
import itertools

def cross(A, B):
    "O conjunto de formas de concatenar os itens de A e B (produto cartesiano)"
    return {a + b
            for a in A for b in B 
           }

def combos(items, n):
    "Todas as combinações de n items; cada combinação concatenada em uma string"
    return {' '.join(combo)
            for combo in itertools.combinations(items, n)
           }

def escolha(n, c):
    "Número de formas de escolher c itens de uma lista com n items"
    return factorial(n) // (factorial(c) * factorial(n - c))

def P(evento, espaco):
    """A probabilidade de um evento, dado um espaço amostral de resultados equiprováveis.
    evento: uma coleção de resultados, ou um predicado.
    espaco: um conjunto de resultados ou a distribuicao de probabilidade na forma de pares {resultado: frequencia}.
    """
    if callable(evento):
        evento = tal_que(evento, espaco)
    if isinstance(espaco, ProbDist):
        return sum(espaco[o] for o in espaco if o in evento)
    else:
        return Fraction(len(evento & espaco), len(espaco))


def tal_que(predicado, espaco):
    """Os resultados no espaço amostral para os quais o predicado é verdadeiro.
    Se espaco é um conjunto, retorna um subconjunto {resultado, ...}
    Se espaco é ProbDist, retorna um ProbDist{resultado, frequencia}"""
    if isinstance(espaco, ProbDist):
        return ProbDist({o: espaco[o] for o in espaco if predicado(o)})
    else:
        return {o for o in espaco if predicado(o)}


class ProbDist(dict):
    "Uma distribuição de probablidade; um mapeamento {resultado: probabilidade}"
    def __init__(self, mapping=(), **kwargs):
        self.update(mapping, **kwargs)
        total = sum(self.values())
        if total != 0:
            for outcome in self:
                self[outcome] = self[outcome]/total
                assert self[outcome] >= 0

def joint(A, B, sep=''):
    """A probabilidade conjunta de duas distribuições de probabilidade independentes.
    Resultado é todas as entradas da forma {a+sep+b: P(a)*P(b)}"""
    return ProbDist({a + sep + b: A[a] * B[b]
                    for a in A
                    for b in B})

## predicados
def soma_eh_primo(r): return eh_primo(sum(r))

def eh_primo(n): return n > 1 and not any(n % i == 0 for i in range(2, n))

def eh_par(n): return n % 2 == 0

# print(royal)
PDSexo = ProbDist (
Sexo_M =4,
Sexo_F =1
)
PDIdades = ProbDist (
 Idade_A = 4,
 Idade_B = 1,
 Idade_C = 0,
 Idade_D = 0
)

def sexo_f(r):
    return "Sexo_F" in r
def sexo_m(r):
    return "Sexo_M" in r
# print(P(sexo_m , PDSexo ))
def idade_A (r):
    return 'Idade_A' in r
def idade_B (r):
    return 'Idade_B' in r
def idade_C (r):
    return 'Idade_C' in r
def idade_D (r):
    return 'Idade_D' in r

# print(P(idade_B , PDIdades))

PDSexoIdade = joint (PDSexo , PDIdades , ' ')
# print(PDSexoIdade)
# print("Probabilidade",P(sexo_m , tal_que (idade_B , PDSexoIdade ))*100)

PA = P(sexo_m , PDSexoIdade)
# print(PA)
PE = P(idade_B , PDSexoIdade)
# print(PE)
prob = PA * PE / PE
# Evidência
PE = P(idade_B , PDSexoIdade )
# print('P(E) = P(Idade=B) = %.1f%% ' % (PE * 100))
 # Hipótese A (Sexo = F)
PA = P(sexo_f , PDSexoIdade )
# print('P(A) = P(Sexo=F) = %.1f%% ' % (PA * 100))

# Hipótese B (Sexo = M)
PB = P(sexo_m , PDSexoIdade )
# print('P(B) = P(Sexo=M) = %.1f%% ' % (PB * 100))
# Evidência , dada Hipótese A
PEA = P(idade_B , tal_que (sexo_f , PDSexoIdade ))
# print('P(E|A) = P( Idade=B|Sexo=F) = %.1f%% ' % (PEA * 100))

# Evidência , dada Hipótese B
PEB = P(idade_B , tal_que (sexo_m , PDSexoIdade ))
# print('P(E|B) = P( Idade=B|Sexo=M) = %.1f%% ' % (PEB * 100))
 # Outra forma de encontrar P(E)
PE2 = PEA * PA + PEB * PB
# print('P(E) = P(Idade=B) = %.1f%% ' % (PE2 * 100))
 # probabilidade desejada (Sexo = M), dada a Evidência -> P(B|E)
PBE = P(sexo_m , tal_que (idade_B , PDSexoIdade ))
# print('P(B|E) = P(Sexo=M| Idade=B) = %.1f%% ' % (PBE * 100))
 # outra forma de encontrar P(B|E)
PBE2 = PEB * PB / PE
# print('P(B|E) = P(Sexo=M| Idade=B) = %.1f%% ' % (PBE2 * 100))

# outra forma de encontrar P(B|E)
PBE3 = PB * PE / PE
# print('P(B|E) = P(Sexo=M| Idade=B) = %.1f%% ' % (PBE3 * 100))

''' sexo; idade ; rendafamiliar
 F ;20;2000
 M ;19;3000
 M ;19;3000
 M ;20;2500
 M ;21;3000'''

PSalario = ProbDist (
    Salario_A = 0,
    Salario_B = 5,
    Salario_C = 0,
    Salario_D = 0
)

def salario_A (r):
    return 'Salario_A' in r

def salario_B (r):
    return 'Salario_B' in r

def salario_C (r):
    return 'Salario_C' in r

def salario_D (r):
    return 'Salario_D' in r

probSalarioSexo = joint (PDSexo , PSalario , ' ')
# print(probSalarioSexo)

prob_salarioB = P(salario_B, tal_que (sexo_f , probSalarioSexo )) 
# print (prob_salarioB)

prob_salarioA =  P(salario_A, tal_que (sexo_f , probSalarioSexo )) 
# print (prob_salarioA)

array_escolaridade = []
array_frequencia = []
array_docs = []
array_problemas = []
array_ferramentas = []

def read_archive():
    arq = open('base.csv')
    for linha in arq.readlines() :
        x = linha.split(",")
        # print(x)
        x.pop(0)
        array_escolaridade.append(x[0])
        array_frequencia.append(x[1])
        array_docs.append(x[2])
        array_problemas.append(x[3])
        array_ferramentas.append(x[4])

read_archive()
array_docs.pop(0)


def normalizacao(array):
    array_teste = []
    novo_array = []
    for i in array:        
        x = i.split(";")         
        array_teste.extend(x)
    for l in array_teste:
        l = l.lower()
        novo_array.append(l) 
            
    return novo_array
        
# array_docs = []
normalizacao(array_escolaridade)
#print(normalizacao(array_escolaridade))

# array_teste = normalizacao(array_docs)
# print(array_teste)
# print(normalizacao(array_docs).count("word"))
PFerremantas = ProbDist(
    Google = normalizacao(array_docs).count("google docs"),
    Word = normalizacao(array_docs).count("word"),
    Libre_office = normalizacao(array_docs).count("libre office"),
    One_note = normalizacao(array_docs).count("onenote"),
    Latex = normalizacao(array_docs).count("latex"),
    Only_office = normalizacao(array_docs).count("only office"),
    Bloco_Notas = normalizacao(array_docs).count("bloco de notas"),
    Share_latex = normalizacao(array_docs).count("sharelatex"),
    Planilha = normalizacao(array_docs).count("planilha google/exel"),
    Fast_format = normalizacao(array_docs).count("fastformat"),
    Quip = normalizacao(array_docs).count("quip"),
    Zoho = normalizacao(array_docs).count("zoho"),
    Only_Office = normalizacao(array_docs).count("only office"),
    Overleaf = normalizacao(array_docs).count("overleaf"),
)
PEscolaridade = ProbDist(
    Superior_completo = array_escolaridade.count("Ensino Superior Incompleto"),
    Superior_incompleto = array_escolaridade.count("Ensino Superior Incompleto"),
    Medio_completo = array_escolaridade.count("Ensino Médio Completo"),
    Pos_graduacao = array_escolaridade.count("Pós-Graduação"),
)


print(array_escolaridade)

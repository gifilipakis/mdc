# coding=utf-8

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

array_ecolaridade = []
array_frequencia = []
array_docs = []
array_problemas = []
array_requisitos = []

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
        array_requisitos.append(x[4])

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
normalizacao(array_docs)

# array_teste = normalizacao(array_docs)
# print(array_teste)
# print(normalizacao(array_docs).count("word"))
PDocs = ProbDist(
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

PFrequancia = ProbDist(
    Nenhuma = array_frequencia.count("Nenhuma"),
    Pouca = array_frequencia.count("Pouca"),
    Moderada = array_frequencia.count("Moderada"),
    Intensa = array_frequencia.count("Intensa")
)

PRequisitos = ProbDist(
    Modelo = normalizacao(array_requisitos).count("modelo de documentos"),
    GeradorReferencias = normalizacao(array_requisitos).count("gerador de referências"),
    TutorialIterativo = normalizacao(array_requisitos).count("tutorial iterativo"),
    SugestoesErros = normalizacao(array_requisitos).count("sugestões de erros"),
    CriacaoAutomaticaSumarios = normalizacao(array_requisitos).count("criação automática de sumários"),
    VerificacaoPlagios = normalizacao(array_requisitos).count("verificação de plágio"),
    GeradorTabelaSiglas = normalizacao(array_requisitos).count("gerador de tabela de siglas"),
    GeradorTabelaImagens = normalizacao(array_requisitos).count("gerador de tabela de imagens")
)

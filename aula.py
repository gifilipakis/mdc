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

array_escolaridade = []
array_frequencia = []
array_docs = []
array_problemas = []
array_requisitos = []

def read_archive():
    arq = open('base.csv')
    for linha in arq.readlines() :
        x = linha.split(",")
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

PEscolaridade = ProbDist(
    Fundamental_completo = array_escolaridade.count("Ensino Fundamental Completo"),
    Superior_completo = array_escolaridade.count("Ensino Superior Incompleto"),
    Superior_incompleto = array_escolaridade.count("Ensino Superior Incompleto"),
    Medio_completo = array_escolaridade.count("Ensino Médio Completo"),
    Pos_graduacao = array_escolaridade.count("Pós-Graduação"),
)

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
    TutorialInterativo = normalizacao(array_requisitos).count("tutorial iterativo"),
    SugestoesErros = normalizacao(array_requisitos).count("sugestões de erros"),
    CriacaoAutomaticaSumarios = normalizacao(array_requisitos).count("criação automática de sumários"),
    VerificacaoPlagios = normalizacao(array_requisitos).count("verificação de plágio"),
    GeradorTabelaSiglas = normalizacao(array_requisitos).count("gerador de tabela de siglas"),
    GeradorTabelaImagens = normalizacao(array_requisitos).count("gerador de tabela de imagens")
)

PProblemas = ProbDist(
    Criacao_sumario = normalizacao(array_problemas).count('criação de sumários'),
    Fazer_citacoes = normalizacao(array_problemas).count('fazer citações'),
    Power_point = normalizacao(array_problemas).count('power point'),
    Criacao_listaFiguras = normalizacao(array_problemas).count('criação de lista de figuras'),
    Libre_office = normalizacao(array_problemas).count('libre office'),
    Numeracao_paginas = normalizacao(array_problemas).count('numeração de páginas'),
    Criar_refrencias = normalizacao(array_problemas).count('criar referências'),
    Nao_sei = normalizacao(array_problemas).count('não sei'),
    Procurar_modelo_de_documento= normalizacao(array_problemas).count('procurar um modelo de documento'),
    Gerador_referencias = normalizacao(array_problemas).count('gerador de refêrencias'),
    Dicas_formatacao = normalizacao(array_problemas).count('dicas de formatação'),
    Verificacao_plagio = normalizacao(array_problemas).count('verificação de plágio'),
    Alinhamento_texto = normalizacao(array_problemas).count('alinhamento de texto'),
    Overleaf_shareLatex = normalizacao(array_problemas).count('overleaf (latex) e sharelatex'),
    Escrita_texto = normalizacao(array_problemas).count('escrita de texto'),
    Tutorial_interativo = normalizacao(array_problemas).count('tutorial interativo da ferramenta'),
    Entregar_pronto = normalizacao(array_problemas).count('entregar o trabalho pronto'),
    Latex = normalizacao(array_problemas).count('latex'),
    Nenhuma_dasOpcoes = normalizacao(array_problemas).count('nenhuma das opções'),
    Um_poucodeCada = normalizacao(array_problemas).count('um pouco de cada')

)   

#Escolaridade
def fundamental_completo(r):
    return 'Fundamental_completo' in r

def superior_completo(r):
    return 'Superior_completo' in r

def superior_incompleto(r):
    return 'Superior_incompleto' in r

def medio_completo(r):
    return 'Medio_completo' in r

def pos_graduacao(r):
    return 'Pos_graduacao' in r

#Docs
def word(r):
    return 'Word' in r

def google(r):
    return 'Google' in r

def libre_office(r):
    return 'Libre_office' in r

def one_note(r):
    return 'One_note' in r

def latex(r):
    return 'Latex' in r

def only_office(r):
    return 'Only_office' in r

def bloco_notas(r):
    return 'Bloco_Notas' in r

def share_latex(r):
    return 'Share_latex' in r

def planilha(r):
    return 'Planilha' in r

def Fast_format(r):
    return 'Fast_format' in r

def quip(r):
    return 'Quip' in r

def zoho(r):
    return 'Zoho' in r

def overleaf(r):
    return 'Overleaf' in r

#Frequência
def nenhuma(r):
    return 'Nenhuma' in r

def pouca(r):
    return 'Pouca' in r

def moderada(r):
    return 'Moderada' in r

def intensa(r):
    return 'Intensa' in r  

#Problemas
def criacao_sumario(r):
    return 'Criacao_sumario' in r

def fazer_citacoes(r):
    return 'Fazer_citacoes' in r

def power_point(r):
    return 'Power_point' in r

def criacao_lista_figura(r):
    return 'Criacao_listaFiguras' in r

def libre_office(r):
    return 'Libre_office' in r

def numeracao_paginas(r):
    return 'Numeracao_paginas' in r

def criar_referencia(r):
    return 'Criar_refrencias' in r

def nao_sei(r):
    return 'Nao_sei' in r

def procurar_modelos_doc(r):
    return 'Procurar_modelo_de_documento' in r

def gerador_referencias(r):
    return 'Gerador_referencias' in r

def dicas_formatacao(r):
    return 'Dicas_formatacao' in r

def verifiacao_plagio(r):
    return 'Verificacao_plagio' in r

def alinhamento_texto(r):
    return 'Alinhamento_texto' in r

def overleaf_shareLatex(r):
    return 'Overleaf_shareLatex' in r

def escrita_texto(r):
    return 'Escrita_texto' in r

def tutorial_interativo(r):
    return 'Tutorial_interativo' in r

def entregar_pronto(r):
    return 'Entregar_pronto' in r

def latex(r):
    return 'Latex' in r

def nenhuma_opcoes(r):
    return 'Nenhuma_dasOpcoes' in r

def um_pouco_cada(r):
    return 'Um_poucodeCada' in r
    
#Requisitos
def modelo(r):
    return 'Modelo' in r 

def geradorReferencias(r):
    return 'GeradorReferencias' in r  

def tutorialInterativo(r):
    return 'TutorialInterativo' in r  

def sugestoesErros(r):
    return 'SugestoesErros' in r  

def criacaoAutomaticaSumarios(r):
    return 'CriacaoAutomaticaSumarios' in r  

def verificacaoPlagios(r):
    return 'VerificacaoPlagios' in r

def geradorTabelaSiglas(r):
    return 'GeradorTabelaSiglas' in r

def geradorTabelaImagens(r):
    return 'GeradorTabelaImagens' in r


#QUESTÕES
"""Q1: Qual a probabilidade de uma pessoa que tenha respondido ao questionário ser do sexo masculino?"""


"""Q2: Dado que uma pessoa indique que sua formação acadêmica é Ensino Superior Incompleto qual a 
probabilidade de ela ter problemas com Criar referências, Fazer citações ou Numeração de páginas?"""


"""Q3: Dado que uma pessoa indique que utiliza o ambiente Word qual a probabilidade de que o problema na edição 
de trabalhos acadêmicos seja Criação de sumários?"""

"""Q4: Dado que uma pessoa indique que utiliza o ambiente Word e seu problema de edição de trabalhos acadêmicos 
seja Criação de sumários qual a probabilidade de que ela gostaria que uma ferramenta de edição fornecesse como 
ajuda a Criação automática de sumários?"""


"""Q5: Dado que uma pessoa indique que sua formação acadêmica é Ensino Fundamental Completo qual a probabilidade 
de ela utilizar Google Docs ou Word como ambiente de edição de trabalhos?"""
# PEscolaridadeDocs = joint(PEscolaridade , PDocs , ' ')
# prob = P(google or word, tal_que(fundamental_completo, PEscolaridadeDocs))
# print(prob)

"""Q6: Dado que uma pessoa indique que sua formação acadêmica é Ensino Superior Incompleto ou Ensino Superior Completo 
qual a probabilidade de ela não utilizar nem Google Docs e nem Word?"""
PEscolaridadeDocs = joint(PEscolaridade , PDocs , ' ')

def notGoogle_Word(valor):
    if valor != "google docs" and valor != "word":
        return True
        
prob = P(notGoogle_Word, tal_que(superior_incompleto or superior_completo, PEscolaridadeDocs))
print(prob)

"""Q7: Dado que uma pessoa indique que utilize o ambiente Word qual os dois problemas com maiores probabilidades -- e 
quais seriam elas?"""


"""Q8: Dado que uma pessoa indique que sua formação acadêmica é Ensino Superior Incompleto ou Ensino Superior Completo 
qual a probabilidade de ela realizar trabalhos acadêmicos com frequência intensa ou moderada?"""
# PEscolaridadeFrequencia = joint(PEscolaridade , PFrequancia , ' ')
# prob = P(intensa or moderada, tal_que(superior_incompleto or superior_completo, PEscolaridadeFrequencia))
# print(prob)

"""Q9: Dado que uma pessoa indique que utiliza o ambiente Libre Office qual a probabilidade de que o problema na edição 
de trabalhos acadêmicos seja Gerador de Tabela de Imagens?"""
# PDocsProblema = joint(PDocs , PProblema , ' ')
# prob = P(geradorTabelaImagens, tal_que(libre_office, PDocsProblema))
# print(prob)

"""Q10: Dado que uma pessoa indique que realiza trabalhos acadêmicos com frequência intensa, qual a probabilidade de que 
o problema na edição de trabalhos acadêmicos seja Criação automática de sumários?"""
# PFrequenciaProblema = joint(PFrequencia , PProblema , ' ')
# prob = P(criacaoSumarios, tal_que(intensa, PFrequenciaProblema))
# print(prob)
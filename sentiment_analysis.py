###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Lucas Oliveira Franco
#            
#
# Email:    lof@cin.ufpe.br
#           
#
# Data:        2016-06-10
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Fulano de Tal, Beltrano do Cin
#
###############################################################################

import sys
import re

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result



def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))

def stopWords(lista):
    listaStop = []
    listaNova = []
    arquivo = open('stopWords.txt')
    lista_arquivo = list(arquivo)
    arquivo.close()
    #removendo '\n' das palavras e armazenando as stopwords numa lista
    for palavra in lista_arquivo :
        palavra = palavra.strip('\n')
        listaStop.append(palavra)

    #armazenando os elementos que nao sao stopwords da lista numa nova lista
    for elemento in lista:
        if elemento in lista and elemento not in listaStop:
            listaNova.append(elemento)
    return listaNova

         
def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    linhasLimpas = []
    aux = []
    words = dict()
    arquivo = open('trainSet.txt')
    arquivo_linhas = list(arquivo)
    arquivo.close()
    #Limpando cada linha com o clean_up()
    for linha in arquivo_linhas :
        linhasLimpas.append(clean_up(linha)) 

    #Removendo as stopwords e aplicando o split_on_separators() numa nova lista
    for comentario in linhasLimpas :
        listaPalavras = stopWords(list(split_on_separators(comentario, ' ´`\/-')))
        escore = int(listaPalavras[0])

        #Checando se a palavra esta no dicionario
        
        for palavra in listaPalavras :
            if palavra not in words and palavra != "" :
                words[palavra] = [1, escore]
            else :
                words[palavra][0] = words[palavra][0] + 1 
                words[palavra][1] = words[palavra][0] + escore
                
    #Armazenando a palavra numa tripla (palavra,frequencia,media de escores da palavra)
    for palavra in words:
        freq = words[palavra][0]
        media_escores = int(words[palavra][1])/int(freq)

        words[palavra] = (palavra,freq,media_escores)
    return words
                               

def readTestSet(fname):
        ''' Esta funcao le o arquivo contendo o conjunto de teste
            retorna um vetor/lista de pares (escore,texto) dos
            comentarios presentes no arquivo.
        '''    
        reviews = []
        arquivo = open(fname)
        arquivo_linhas = arquivo.readlines()
        arquivo.close()

        for linha in arquivo_linhas :
            linha = linha.strip("\n")
            linha = linha.strip("\t")
            reviews.append((int(linha[0]),linha[2:]))

        return reviews
  
	

def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    score = 0.0
    count = 0
    reviewSplit = stopWords(list(split_on_separators(review, " \/´`-")))

    for palavra in reviewSplit:
        palavra = clean_up(palavra)
        if palavra not in words :
            score = score + 2
            count = count + 1
        else:
            score = score + words[palavra][-1]
            count = cont + 1

    return score/count


def computeSumSquaredErrors(reviews,words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0
    for review in reviews:
        valorSentimento = computeSentiment(review[1], words)
        difer = (valorSentimento - review[0])
        sse = sse + (difer * difer)

    sse = (sse/len(reviews))
    return sse

    
def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 3:
        print 'Numero invalido de argumentos'
        print 'O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>'
        sys.exit(0)

    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1])
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words)
    
    print 'A soma do quadrado dos erros e\': {0}'.format(sse)
            

if __name__ == '__main__':
   main()
    
    

import sys

if len(sys.argv) < 2:
    sys.exit(1)

# Nome do arquivo de entrada
nome_arquivo = sys.argv[1] + ".asm"

# Se o usuário fornecer um arquivo de saída, abra o arquivo para escrita
if len(sys.argv) > 2:
    nome_arquivo_saida = sys.argv[2]
    saida = open(nome_arquivo_saida + ".asm", "w")

#MANIPULAÇÃO DE ARQUIVOS

def ler_palavra_em_linha(nome_arquivo, numero_linha, numero_palavra):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for indice, linha in enumerate(arquivo, start=1):
                palavras = linha.split()
                linha_formatada = ""
                for palavra in palavras:
                    if palavra != "xor" and palavra != "xori":
                        palavra = palavra.replace(",", "")
                        palavra = palavra.replace(")", " ")
                        palavra = palavra.replace("(", " ")
                        palavra = palavra.replace("x", "")
                    linha_formatada += palavra + " "
                if indice == numero_linha:
                    palavras = linha_formatada.split()
                    if numero_palavra < len(palavras):  # Verificar se o número da palavra é menor que o comprimento da lista de palavras
                        return palavras[numero_palavra]  # Índices em Python começam em 0
                    else:
                        return None
    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
        return None

    
    #ler_palavra_em_linha("entrada_2.asm", 1, 2) --> é passado como parametro o nome do arquivo, o numero da linha, e a palavra da linha a ser lida


#DICIONARIOS
funct3 = {"lb": "000", "ori": "110", "add": "000", "sll": "001", "bne": "001", "sb": "000", "lw":"010","lh": "001", "sh":"001", "sw":"010", "sub":"000", "and":"111", "or":"110", "xor":"100", "addi":"000", "andi":"111", "srl":"101", "beq":"000", "bge":"101", "xori":"100"   }
opcode = {"lb": "0000011", "ori": "0010011", "add": "0110011", "sll": "0110011", "bne":"1100011", "sb":"0100011", "lw":"0000011","lh":"0000011", "sh":"0100011", "sw":"0100011", "sub":"0110011", "and":"0110011", "or":"0110011", "xor":"0110011 ", "addi":"0010011", "andi":"0010011", "srl": "0110011", "beq":"1100011", "bge":"1100011", "xori":"0010011" } 
funct7 = "0000000" #usado em instruçoes do tipo R (No nosso caso o ADD e SLL)
    
def Binario_Str(valor_binario):
    return str(valor_binario)

def Complemento_Dois(valor_bin):
    valor_decimal = int(valor_bin, 2)
    if valor_decimal >= 0:
        return "{:012b}".format(int(valor_decimal))
    else:
        valor_binario = format(valor_decimal * (-1), '012b')
        numero_invertido = ""
        
        for bit in valor_binario:
            if bit == '0':
                numero_invertido += '1'
            else:
                numero_invertido += '0'
        
        valor_complemento_dois = bin(int(numero_invertido, 2) + 1)[2:]
    return str(valor_complemento_dois)
    
numero_linha = 1

while True:
    palavras = [] # Reinicializa a lista de palavras para cada linha
    for contador_linha in range(4):   # percorre toda a linha do arquivo
        palavra = ler_palavra_em_linha(nome_arquivo, numero_linha, contador_linha) # Lê palavra por palavra da linha atual
        if palavra is None:  # Se a palavra for None, indica que não há mais linhas para processar
            break
        palavras.append(palavra)  # Adiciona a palavra ao vetor palavras
        
    if not palavras:  # Se a lista de palavras estiver vazia, indica que não há mais linhas para processar
        break
    
    palavras[1] = "{:05b}".format(int(palavras[1])) #rd
    palavras[2] = "{:05b}".format(int(palavras[2])) #rs1
    if len(palavras) > 3:                               #Caso a linha de instrução possua menos de 3 palavras
        palavras[3] = "{:05b}".format(int(palavras[3])) #rs2
    else:
        None
    x = "" # Declaramos x
    
    #FORMATO TIPO R
    if palavras[0] =="add" or palavras[0] =="sll" or palavras[0] =="sub" or palavras[0] =="and" or palavras[0] =="or" or palavras[0] =="xor" or palavras[0] =="srl":
        if palavras[0] == "add":
            x = funct7 + palavras[3] + palavras[2] + funct3["add"] + palavras[1] + opcode["add"]
        elif palavras[0] == "sll":
            x = funct7 + palavras[3] + palavras[2] + funct3["sll"] + palavras[1] + opcode["sll"]
        elif palavras[0] == "sub":
            x = "0100000" + palavras[3] + palavras[2] + funct3["sub"] + palavras[1] + opcode["sub"]
        elif palavras[0] == "and":
            x = funct7 + palavras[3] + palavras[2] + funct3["and"] + palavras[1] + opcode["and"]
        elif palavras[0] == "or":
            x = funct7 + palavras[3] + palavras[2] + funct3["or"] + palavras[1] + opcode["or"]
        elif palavras[0] == "xor":
            x = funct7 + palavras[3] + palavras[2] + funct3["xor"] + palavras[1] + opcode["xor"]
        elif palavras[0] == "srl":
            x = funct7 + palavras[3] + palavras[2] + funct3["srl"] + palavras[1] + opcode["srl"]
        if len(sys.argv) > 2:
            saida.write(x + '\n')
        else:
          print(x)
    
    #FORMATO TIPO I
    elif palavras[0] =="ori" or palavras[0] =="lb" or palavras[0] =="lw" or palavras[0] =="lh" or palavras[0] =="addi" or palavras[0] =="andi" or palavras[0] =="xori":
        palavras[3]= Complemento_Dois(palavras[3])
        if palavras[0] == "ori":
            x = palavras[3] + palavras[2] + funct3["ori"] + palavras[1] + opcode["ori"]
        elif palavras[0] == "lb":
            x = palavras[3] + palavras[2] + funct3["lb"] + palavras[1] + opcode["lb"]
        elif palavras[0] == "lw":
            x = palavras[3] + palavras[2] + funct3["lw"] + palavras[1] + opcode["lw"]
        elif palavras[0] == "lh":
            x = palavras[3] + palavras[2] + funct3["lh"] + palavras[1] + opcode["lh"]
        elif palavras[0] == "addi":
            x = palavras[3] + palavras[2] + funct3["addi"] + palavras[1] + opcode["addi"]
        elif palavras[0] == "andi":
            x = palavras[3] + palavras[2] + funct3["andi"] + palavras[1] + opcode["andi"]
        elif palavras[0] == "xori":
            x = palavras[3] + palavras[2] + funct3["xori"] + palavras[1] + opcode["xori"]
        if len(sys.argv) > 2:
                saida.write(x + '\n')
        else:
            print(x)
        
    #FORMATO TIPO S/SB    
    elif palavras[0] =="sb" or palavras[0] == "bne" or palavras[0] =="sh" or palavras[0] =="sw" or palavras[0] =="beq" or palavras[0] =="bge":
        palavras[3]=Complemento_Dois(palavras[3])
        if palavras[0] == "sb":
            x = palavras[3][:7] + palavras[2] + palavras[1] + funct3["sb"] + palavras[3][7:] + opcode["sb"]
        elif palavras[0] == "bne":
            x = palavras[3][:7] + palavras[2] + palavras[1] + funct3["bne"] + palavras[3][7:] + opcode["bne"]
        elif palavras[0] == "sh":
            x = palavras[3][:7] + palavras[2] + palavras[1] + funct3["sh"] + palavras[3][7:] + opcode["sh"]
        elif palavras[0] == "sw":
            x = palavras[3][:7] + palavras[2] + palavras[1] + funct3["sw"] + palavras[3][7:] + opcode["sw"]
        elif palavras[0] == "beq":
            x = palavras[3][:7] + palavras[2] + palavras[1] + funct3["beq"] + palavras[3][7:] + opcode["beq"]
        elif palavras[0] == "bge":
            x = palavras[3][:7] + palavras[2] + palavras[1] + funct3["bge"] + palavras[3][7:] + opcode["bge"]
        if len(sys.argv) > 2:
                saida.write(x + '\n')
        else:
            print(x)
            
    #implementaçao das PSEUDOINSTRUÇOES            
    elif palavras[0]=="mv" or palavras[0] == "li" or palavras[0] == "not" or palavras[0] == "neg":
        if palavras[0] == "mv":
            x = Complemento_Dois("0") + palavras[2] + funct3["addi"] + palavras[1] + opcode["addi"]
        elif palavras[0] == "not":
            x = Complemento_Dois("-1") + palavras[2] + funct3["xori"] + palavras[1] + opcode["xori"]
        elif palavras[0] == "neg":
            x = "0100000" + palavras[3] + "00000" + funct3["sub"] + palavras[1] + opcode["sub"]
        elif palavras[0] == "li":
            palavras[2]=Complemento_Dois(palavras[2])
            x = palavras[2] + "00000" + funct3["addi"] + palavras[1] + opcode["addi"]
        if len(sys.argv) > 2:
                saida.write(x + '\n')
        else:
            print(x)
            
    numero_linha += 1  # Avança para a próxima linha
    
#Se um arquivo de saída foi fornecido, feche-o
if len(sys.argv) > 2:
    saida.close() 

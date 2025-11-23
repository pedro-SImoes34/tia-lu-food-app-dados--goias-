import json

class node:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1
        

def arvore(node, nivel=0, prefixo="Raiz: "):
    if node is not None:
        if nivel == 0:
            print(prefixo + str(node.valor))
            print()
        else:
            print(" " * (nivel - 1) * 4 + "|--" + str(node.valor))            

        if node.esquerda is not None or node.direita is not None:
            arvore(node.esquerda, nivel + 1)
            arvore(node.direita, nivel + 1)

def altura(node):
    return node.altura if node else 0

def altura_atualizada(node):
    node.altura = 1 + max(altura(node.esquerda), altura(node.direita))

def balanceamento(node):
    return altura(node.esquerda) - altura(node.direita)

def rotacao_direita(y):
    x = y.esquerda
    T2 = x.direita

    x.direita = y
    y.esquerda = T2

    altura_atualizada(y)
    altura_atualizada(x)
    return x

def rotacao_esquerda(x):
    y = x.direita
    T2 = y.esquerda

    y.esquerda = x
    x.direita = T2

    altura_atualizada(x)
    altura_atualizada(y)
    return y


def inserirNode(node_atual, chave, valor):
    if node_atual is None:
        return node(chave, valor)
    
    if chave < node_atual.chave:
        node_atual.esquerda = inserirNode(node_atual.esquerda, chave, valor)
    elif chave > node_atual.chave:
        node_atual.direita = inserirNode(node_atual.direita, chave, valor)
    else:
        node_atual.valor = valor
        return node_atual

    altura_atualizada(node_atual)
    balance = balanceamento(node_atual)

    if balance > 1 and chave < node_atual.esquerda.chave:
        return rotacao_direita(node_atual)
    
    if balance < -1 and chave > node_atual.direita.chave:
        return rotacao_esquerda(node_atual)

    if balance > 1 and chave > node_atual.esquerda.chave:
        node_atual.esquerda = rotacao_esquerda(node_atual.esquerda)
        return rotacao_direita(node_atual)

    if balance < -1 and chave < node_atual.direita.chave:
        node_atual.direita = rotacao_direita(node_atual.direita) 
        return rotacao_esquerda(node_atual)
    
    return node_atual

def buscarNode(node_atual, chave):
    if node_atual is None:
        return None
    
    if chave == node_atual.chave:
        return node_atual.valor
    elif chave < node_atual.chave:
        return buscarNode(node_atual.esquerda, chave)
    else:
        return buscarNode(node_atual.direita, chave)
    
def atualizar_node(raiz, chave, novo_valor):
    return inserirNode(raiz, chave, novo_valor)

class node_pedidos:
    def __init__(self, pedido):
        self.pedido = pedido
        self.esquerda = None
        self.direita = None
        self.altura = 1

def inserir_pedido(node_atual, pedido):
    if node_atual is None:
        return node_pedidos(pedido)
    
    if pedido["codigo"] < node_atual.pedido["codigo"]:
        node_atual.esquerda = inserir_pedido(node_atual.esquerda, pedido)

    elif pedido["codigo"] > node_atual.pedido["codigo"]:
        node_atual.direita = inserir_pedido(node_atual.direita, pedido)

    else:
        node_atual.pedido = pedido
        return node_atual
    
    node_atual.altura = 1 + max(
        getattr(node_atual.esquerda, 'altura', 0),
        getattr(node_atual.direita, 'altura', 0)
    )

    balance = getattr(node_atual.esquerda, 'altura', 0) - getattr(node_atual.direita, 'altura', 0)

    if balance > 1 and pedido["codigo"] < node_atual.esquerda.pedido["codigo"]:
        return rotacao_direita(node_atual)
    if balance < -1 and pedido["codigo"] > node_atual.direita.pedido["codigo"]:
        return rotacao_esquerda(node_atual)
    if balance > 1 and pedido["codigo"] > node_atual.esquerda.pedido["codigo"]:
        node_atual.esquerda = rotacao_esquerda(node_atual.esquerda)
        return rotacao_direita(node_atual)
    if balance < -1 and pedido["codigo"] < node_atual.direita.pedido["codigo"]:
        node_atual.direita = rotacao_direita(node_atual.direita)
        return rotacao_esquerda(node_atual)

    return node_atual

def buscar_pedido(node_atual, codigo):
    if node_atual is None:
        return None
    if codigo == node_atual.pedido["codigo"]:
        return node_atual.pedido
    elif codigo < node_atual.pedido["codigo"]:
        return buscar_pedido(node_atual.esquerda, codigo)
    else:
        return buscar_pedido(node_atual.direita, codigo)
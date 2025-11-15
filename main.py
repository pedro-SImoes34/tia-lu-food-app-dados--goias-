import json
import os

menu_de_itens = []

if os.path.exists("restaurante.json"):
    with open("restaurante.json", "r", encoding="utf-8") as arq:
        menu_de_itens = json.load(arq)   

else:
    menu_de_itens = [] 

id = 1
  

def registrar_item():
    global id
    print("\n--- Cadastrar Novo Item ---")
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição: ")
    preco = float(input("Digite o preço: "))
    estoque = int(input("Digite a quantidade em estoque: "))

    novo_item = {
        "id": id,
        "nome": nome, 
        "descricao": descricao,
        "preco": preco, 
        "estoque": estoque
                 }
    menu_de_itens.append(novo_item)

    with open("restaurante.json", "w", encoding="utf-8") as arq:
        json.dump(menu_de_itens, arq, ensure_ascii=False)

    id += 1
    print("Item cadastrado com sucesso!")

def atualizar_item():
    codigo = int(input("\n Digite o código do item a ser atualizado:  "))
    for item in menu_de_itens:
        if item["id"] == codigo:
            print(f"\nEditando item {item['nome']} (código {item['id']})")
            novo_nome = input(f"Novo nome ({item['nome']}): ")
            if novo_nome:
                 item["nome"] = novo_nome
            nova_desc= input(f"Nova descrição ({item['descricao']}): ")
            if nova_desc:
                 item["descricao"] = nova_desc
            novo_preco= input(f"Novo preço ({item['preco']}): ")
            if novo_preco:
                item["preco"] = float(novo_preco)
            novo_estoque = input(f"Novo estoque ({item['estoque']}): ")
            if novo_estoque:
                item["estoque"] = int(novo_estoque)
            print("\nItem atualizado.\n")
            with open("restaurante.json", "w", encoding="utf-8") as arq:
                json.dump(menu_de_itens, arq, ensure_ascii=False)
            return
    print("\nItem não encontrado!\n")

def consultar_itens():
    if not menu_de_itens:
        print("\nNenhum item cadastrado.\n")
        return
    print("\nLista de Itens:")
    for item in menu_de_itens:
        print(f"[{item['id']}] {item['nome']} - R${item['preco']:.2f} (Estoque: {item['estoque']})")
    print()
        
def detalhes_item():
    codigo = int(input("\n Digite o código do item:  "))
    for item in menu_de_itens:
        if item["id"] == codigo:
            print("\nDetalhes do Item:")
            print(f"Código: {item['id']}")
            print(f"Nome: {item['nome']}")
            print(f"Descrição: {item['descricao']}")
            print(f"Preço: R${item['preco']:.2f}")
            print(f"Estoque: {item['estoque']}\n")
            return
    print("\nItem não encontrado!\n")

def menu_principal():
    menu = 1
    while menu != 0:
        print("\n === MENU PRINCIPAL ===")
        print("1 - Registrar Item")
        print("2 - Atualizar Item")
        print("3 - Consultar Itens")
        print("4 - Detalhes do Item")
        print("0 - Sair")

        opcao = input("\n Escolha uma opção: ")
        
        match opcao:
            case "1":
                registrar_item()
            case "2":
                atualizar_item()
            case "3":
                consultar_itens()
            case "4":
                detalhes_item()
            case "0":
                print("\nSaindo...")
                menu = 0
            case _:
                print("\nOpção inválida.\n")

menu_principal()
           
fila_pedidos_pendentes = []  
fila_pedidos_aceitos = []    
fila_pedidos_prontos = []     
fila_pedidos_entrega = []     
todos_pedidos = []
valor_total = 0

def realizar_pedido(nome_cliente, itens):
    codigo = len(todos_pedidos) + 1 
    valor_total = 0
    
    for item in menu_de_itens:
        if item["id"] == itens: 
            valor_total += item["preco"]

    valido = 0
    while valido == 0: 
        desconto = input("Deseja adicionar algum cupom de desconto? (S/N): ")
        cupom = "GOIAS10"
        
        if desconto == "S":
            cupom = input("Digite o cupom: ") 
            if cupom == "GOIAS10":
                valor_desconto = valor_total * 0.1 
                valor_total -= valor_desconto
                print(f"O valor caiu para R${valor_total:.2f}")
                valido = 1     
            else:
                print("\nCupom inválido!")
                print("1 - Tentar novamente.")
                print("2 - Continuar sem cupom.")
                resposta = int(input("Escolha uma opção: "))
                
                if resposta == 1:
                    valido = 0              
                elif resposta == 2:
                    print(f"\nValor: R${valor_total:.2f}")
                    valido = 1
                else:
                    valido = 0
        elif desconto == "N":
            print(f"\nValor: R${valor_total:.2f}")
            valido = 1
        else:
            valido = 0
        
    pedido = {
        "codigo": codigo,
        "nome_cliente": nome_cliente,
        "itens": [],
        "status": "AGUARDANDO APROVACAO", 
        "valor_total": valor_total
    }
        
    fila_pedidos_pendentes.append(pedido) 
    todos_pedidos.append(pedido)   
    print(f"Pedido {codigo} criado.")

def adicionar_item_pedido():
    codigo_pedido = int(input("Digite o código do pedido: "))
    item_id = int(input(f"Digite o item que deseja adicionar ao pedido {codigo_pedido}: "))
        
    pedido = None
    for p in todos_pedidos:
        if int(p["codigo"]) == codigo_pedido:
            pedido = p

    item = None
    for it in menu_de_itens:
        if int(it["id"]) == item_id:
            item = it

    match (pedido, item):
        case (None, _):
            print("Pedido não encontrado!")
            return

        case (_, None):
            print("Item não encontrado!")
            return

        case (_, _) if item["estoque"] <= 0:
            print("Sem estoque desse item!")
            return

        case _:
            novo_item = {
                "id": item["id"],
                "nome": item["nome"],
                "preco": item["preco"]
            }

            pedido["itens"].append(novo_item)
            pedido["valor_total"] += item["preco"]
            item["estoque"] -= 1

            print(f"Item adicionado ao pedido!\n O novo valor do pedido ficou no total de R${pedido["valor_total"]} ")
            return pedido

def processar_pedido():
    if len(fila_pedidos_pendentes) == 0:
        print("Nenhum pedido pendente.")
        
    else:
        pedido = fila_pedidos_pendentes.pop(0)
        print(f"\nProcessando pedido {pedido['codigo']}")
        print("1 - Aceitar pedido")
        print("2 - Rejeitar pedido")
        escolha = input("Digite sua escolha: ")

        if escolha == "1":
            pedido["status"] = "ACEITO"
            fila_pedidos_aceitos.append(pedido)
            print(f"Pedido {pedido['codigo']} foi ACEITO.")
        elif escolha == "2":
            pedido["status"] = "REJEITADO"
            print(f"Pedido {pedido['codigo']} foi REJEITADO.")
        else:
            print("Opção inválida.")

def preparar_pedido():
    if len(fila_pedidos_aceitos) == 0:
        print("Nenhum pedido aceito.")
    else:
        pedido = fila_pedidos_aceitos.pop(0)
        pedido["status"] = "FEITO"
        fila_pedidos_prontos.append(pedido)
        print(f"Pedido {pedido['codigo']} está pronto.")

def entregar_pedido():
    if len(fila_pedidos_prontos) == 0:
        print("Nenhum pedido pronto.")
    else:
        pedido = fila_pedidos_prontos.pop(0)
        pedido["status"] = "SAIU PARA ENTREGA"
        fila_pedidos_entrega.append(pedido)
        print(f"Pedido {pedido['codigo']} saiu para entrega.")

def pedido_entregue():
    if len(fila_pedidos_entrega) == 0:
        print("Nenhum pedido em rota.")
    else:
        pedido = fila_pedidos_entrega.pop(0)
        pedido["status"] = "ENTREGUE"
        print(f"Pedido {pedido['codigo']} foi ENTREGUE.")

def exibir_pedidos():
    print("\n--- LISTA DE PEDIDOS ---")
    for pedido in todos_pedidos:
        print(f"Código: {pedido['codigo']} | Cliente: {pedido['nome_cliente']} | Status: {pedido['status']}")
    print("-------------------------\n")

def filtrar_pedidos():
    print("1 - AGUARDANDO APROVACAO")
    print("2 - ACEITO")
    print("3 - FAZENDO")
    print("4 - FEITO")
    print("5 - ESPERANDO GARÇOM")
    print("6 - SAIU PARA ENTREGA")
    print("7 - ENTREGUE")
    print("8 - CANCELADO")
    print("9 - REJEITADO")
    filtro = input("Qual status deseja usar como filtro: ")
    
    match filtro:
        case "1":
            status = "AGUARDANDO APROVACAO"
        case "2":
            status = "ACEITO"
        case "3":
            status = "FAZENDO"
        case "4":
            status = "FEITO"
        case "5":
            status = "ESPERANDO GARÇOM"
        case "6":
            status = "SAIU PARA ENTREGA"
        case "7":
            status = "ENTREGUE"
        case "8":
            status = "CANCELADO"
        case "9":
            status = "REJEITADO"
        case _:
            print("Inválido.")
            return

    for pedido in todos_pedidos:
        if pedido["status"] == status:
            print(pedido)

def menu_pedidos():
    sair = 1
    while sair != 0:
        print("\n ------ SISTEMA DE PEDIDOS ------")
        print("1 - Realizar Pedido")
        print("2 - Adicionar item ao pedido")
        print("3 - Processar Pedido Pendente")
        print("4 - Preparar Pedido")
        print("5 - Enviar para a Mesa")
        print("6 - Finalizar Entrega")
        print("7 - Exibir todos os pedidos")
        print("8 - Filtrar pedidos por status")
        print("9 - Voltar ao menu anterior")
        print("0 - Sair")
        opcao = input("\n Escolha uma opção: ")

        match opcao:
            case "1":
                nome = input("\n Nome do cliente: ")
                itens = int(input("Itens do pedido: "))
                item_encontrado = False
                for novo_item in menu_de_itens:
                    if itens == novo_item["id"]:
                        item_encontrado = True
                        if novo_item["estoque"] > 0:
                            realizar_pedido(nome, itens)
                            novo_item["estoque"] -= 1
                        else:
                            print("Sem estoque.")
                        break
                if not item_encontrado:
                    print("Item não encontrado.")
            case "2":
                adicionar_item_pedido()
            case "3":
                processar_pedido()
            case "4":
                preparar_pedido()
            case "5":
                entregar_pedido()
            case "6":
                pedido_entregue()
            case "7":
                exibir_pedidos()
            case "8":
                filtrar_pedidos()
            case "9":
                menu_principal()
            case "0":
                sair = 0
                print("Saindo...")
            case _:
                print("Inválido.")

menu_pedidos()
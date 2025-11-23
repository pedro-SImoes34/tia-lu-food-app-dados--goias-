import json
import os
import arvore_avl

menu_de_itens = []
todos_pedidos = []
id = 1

raiz_itens = None
raiz_pedidos = None

if os.path.exists("restaurante.json") and os.path.getsize("restaurante.json") > 0:
    with open("restaurante.json", "r", encoding="utf-8") as arq:
        dados_json = json.load(arq)

    menu_de_itens = dados_json.get("itens", [])
    todos_pedidos = dados_json.get("pedidos", [])

    if menu_de_itens:
        id = max(item["id"] for item in menu_de_itens) + 1

else:
    menu_de_itens = []
    dados_json = {
        "itens": [],
        "pedidos": []
    }
    with open("restaurante.json", "w", encoding="utf-8") as arq:
        json.dump(dados_json, arq, ensure_ascii=False, indent=4)

    menu_de_itens = dados_json["itens"]
    todos_pedidos = dados_json["pedidos"]

for item in menu_de_itens:
    raiz_itens = arvore_avl.inserirNode(raiz_itens, item["id"], item)
for pedido in todos_pedidos:
    raiz_pedidos = arvore_avl.inserir_pedido(raiz_pedidos, pedido)


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

    dados_json["itens"] = menu_de_itens
    with open("restaurante.json", "w", encoding="utf-8") as arq:
        json.dump(dados_json, arq, ensure_ascii=False, indent=4)

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
            nova_desc = input(f"Nova descrição ({item['descricao']}): ")
            if nova_desc:
                item["descricao"] = nova_desc
            novo_preco = input(f"Novo preço ({item['preco']}): ")
            if novo_preco:
                item["preco"] = float(novo_preco)
            novo_estoque = input(f"Novo estoque ({item['estoque']}): ")
            if novo_estoque:
                item["estoque"] = int(novo_estoque)
            print("\nItem atualizado.\n")

            dados_json["itens"] = menu_de_itens
            with open("restaurante.json", "w", encoding="utf-8") as arq:
                json.dump(dados_json, arq, ensure_ascii=False)
            return
    print("\nItem não encontrado!\n")


def counting_sort_dicts(arr, key_name):
    if not arr:
        return []
    max_val = 0
    for d in arr:
        if d[key_name] > max_val:
            max_val = d[key_name]
    count = [0] * (max_val + 1)
    for d in arr:
        count[d[key_name]] += 1
    for i in range(1, len(count)):
        count[i] += count[i-1]
    output = [None] * len(arr)
    for d in reversed(arr):
        element_val = d[key_name]
        output_index = count[element_val] - 1
        output[output_index] = d
        count[element_val] -= 1
    return output


def consultar_itens():
    if not menu_de_itens:
        print("\n⚠ Nenhum item cadastrado.\n")
        return
    print("\n📋 Lista de Itens (Ordenada por ID):")
    lista_ordenada = counting_sort_dicts(menu_de_itens, "id")
    for item in lista_ordenada:
        print(
            f"[{item["id"]}] {item["nome"]} - R${item["preco"]:.2f} (Estoque: {item["estoque"]})")
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
valor_total = 0


def realizar_pedido(nome_cliente, itens):
    codigo = len(todos_pedidos) + 1
    valor_total = 0

    buscar_item = arvore_avl.buscarNode(raiz_itens, itens)
    if buscar_item is None:
        print("Item não encontrado!")
        return
    valor_total = buscar_item["preco"]

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

    global raiz_pedidos
    raiz_pedidos = arvore_avl.inserir_pedido(raiz_pedidos, pedido)

    dados_json["pedidos"] = todos_pedidos
    with open("restaurante.json", "w", encoding="utf-8") as arq:
        json.dump(dados_json, arq, ensure_ascii=False, indent=4)
    print(f"Pedido {codigo} criado.")


def adicionar_item_pedido():
    codigo_pedido = int(input("Digite o código do pedido: "))
    item_id = int(
        input(f"Digite o item que deseja adicionar ao pedido {codigo_pedido}: "))

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

            print(
                f"Item adicionado ao pedido!\n O novo valor do pedido ficou no total de R${pedido["valor_total"]:.2f} ")

            dados_json = {
                "itens": menu_de_itens,
                "pedidos": todos_pedidos
            }

            with open("restaurante.json", "w", encoding="utf-8") as arq:
                json.dump(dados_json, arq, ensure_ascii=False, indent=4)

            return pedido

    with open("restaurante.json", "w", encoding="utf-8") as arq:
        json.dump(dados_json, arq, ensure_ascii=False, indent=4)


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

    dados_json = {
        "itens": menu_de_itens,
        "pedidos": todos_pedidos
    }

    with open("restaurante.json", "w", encoding="utf-8") as arq:
        json.dump(dados_json, arq, ensure_ascii=False, indent=4)


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
    print("\n--- LISTA DE PEDIDOS (Ordenada) ---")
    lista_pedidos_ordenados = counting_sort_dicts(todos_pedidos, "codigo")
    for pedido in lista_pedidos_ordenados:
        print(
            f"Código: {pedido['codigo']} | Cliente: {pedido['nome_cliente']} | Valor: {pedido['valor_total']:.2f} |Status: {pedido['status']}")
    print("-------------------------\n")

def buscar_pedido_avl():
    codigo = int(input("Digite o código do pedido: "))
    resultado = arvore_avl.buscar_pedido(raiz_pedidos, codigo)

    if resultado == None:
        print("Pedido não encontrado!")
        return

    print("\n--- Detalhes do Pedido ---")
    print(f"Código: {resultado['codigo']}")
    print(f"Cliente: {resultado['nome_cliente']}")
    print(f"Valor: {resultado['valor_total']:.2f}")
    print(f"Status: {resultado['status']}")


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
        print("8 - Buscar pedidos (AVL)")
        print("9 - Filtrar pedidos por status")
        print("10 - Voltar ao menu anterior")
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
                buscar_pedido_avl()
            case "9":
                filtrar_pedidos()
            case "10":
                menu_principal()
            case "0":
                sair = 0
                print("Saindo...")
            case _:
                print("Inválido.")


menu_pedidos()

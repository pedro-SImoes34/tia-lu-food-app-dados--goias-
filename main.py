import json
menu_de_itens = []
id = 1
with open("restaurante.json", "r", encoding="utf-8") as arq:
    json.load(arq)

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
            print(f"\nEditando item {item["nome"]} (código {item["id"]})")
            novo_nome = input(f"Novo nome ({item["nome"]}): ")
            if novo_nome:
                 item["nome"] = novo_nome
            nova_desc= input(f"Nova descrição ({item["descricao"]}): ")
            if nova_desc:
                 item["descricao"] = nova_desc
            novo_preco= input(f"Novo preço ({item["preco"]}): ")
            if novo_preco:
                item["preco"] = float(novo_preco)
            novo_estoque = input(f"Novo estoque ({item["estoque"]}): ")
            if novo_estoque:
                item["estoque"] = int(novo_estoque)
            print("\n✅ Item atualizado com sucesso!\n")
            with open("restaurante.json", "w", encoding="utf-8") as arq:
                json.dump(menu_de_itens, arq, ensure_ascii=False)
            return
    print("\n❌ Item não encontrado!\n")

def consultar_itens():
    if not menu_de_itens:
        print("\n⚠ Nenhum item cadastrado.\n")
        return
    print("\n📋 Lista de Itens:")
    for item in menu_de_itens:
        print(f"[{item["id"]}] {item["nome"]} - R${item["preco"]:.2f} (Estoque: {item["estoque"]})")
    print()
        
def detalhes_item():
    codigo = int(input("\n Digite o código do item:  "))
    for item in menu_de_itens:
        if item["id"] == codigo:
            print("\n🔎 Detalhes do Item:")
            print(f"Código: {item["id"]}")
            print(f"Nome: {item["nome"]}")
            print(f"Descrição: {item["descricao"]}")
            print(f"Preço: R${item["preco"]:.2f}")
            print(f"Estoque: {item["estoque"]}\n")
            return
    print("\n❌ Item não encontrado!\n")

def menu_principal():
    menu = 1
    while menu != 0:
        print("\n === MENU PRINCIPAL ===")
        print("1 - Cadastrar Item")
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
                print("\n👋 Saindo do sistema. Até mais!")
                menu = 0
            case _:
                print("\n⚠ Opção inválida, tente novamente.\n")

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
                print("\n Você ganhou 10% de desconto!")
                print(f"O valor do seu pedido acabou de cair para R${valor_total:.2f}!!")
                valido = 1     
            else:
                print("\n Cupom inválido!")
                print("1 - Tentar novamente.")
                print("2 - Continuar sem cupom.")
                resposta = int(input("Escolha uma opção: "))
                
                if resposta == 1:
                    valido = 0              
                elif resposta == 2:
                    print(f"\n O seu pedido ficou no valor de R${valor_total:.2f}")
                    valido = 1
                else:
                    print("\n Não consegui te entender, tente inserir o cupom novamente...")
                    valido = 0
        elif desconto == "N":
            print(f"\n O seu pedido ficou no valor de R${valor_total:.2f}")
            valido = 1
        else:
            print("\n Desculpe, não entendi sua resposta, tente novamente.")
        
    pedido = {
        "codigo": codigo,
        "nome_cliente": nome_cliente,
        "itens": itens, 
        "status": "AGUARDANDO APROVACAO", 
        "valor_total": valor_total
    }
        
    fila_pedidos_pendentes.append(pedido) 
    todos_pedidos.append(pedido)   
    print(f"Pedido {codigo} criado para {nome_cliente} e está AGUARDANDO APROVACAO.")

def processar_pedido():
    if len(fila_pedidos_pendentes) == 0:
        print("Nenhum pedido pendente para processar.")
    else:
        pedido = fila_pedidos_pendentes.pop(0)
        print(f"\n Processando pedido {pedido["codigo"]} de valor R${pedido["valor_total"]:.2f} do cliente {pedido["nome_cliente"]}")
        print("1 - Aceitar pedido")
        print("2 - Rejeitar pedido")
        escolha = input("Digite sua escolha: ")

        if escolha == "1":
            pedido["status"] = "ACEITO"
            fila_pedidos_aceitos.append(pedido)
            print(f"Pedido {pedido["codigo"]} foi ACEITO e está na fila de preparo.")
        else:
            pedido["status"] = "REJEITADO"
            print(f"Pedido {pedido["codigo"]} foi REJEITADO.")

def preparar_pedido():
    if len(fila_pedidos_aceitos) == 0:
        print("Nenhum pedido aceito para preparar.")

    else:
        pedido = fila_pedidos_aceitos.pop(0)
        print(f"\n Deseja prosseguir com o pedido {pedido["codigo"]} de {pedido["nome_cliente"]} no valor de {pedido["valor_total"]:.2f}?")
        print("1- Prosseguir com o pedido")  
        print("2- Cancelar o pedido")
        escolha = input("Digite a sua escolha: ")

        if escolha == "1":
            pedido["status"] = "FAZENDO"
            print(f"Pedido {pedido["codigo"]} está sendo preparado...")
            pedido["status"] = "FEITO"
            fila_pedidos_prontos.append(pedido)
            print(f"Pedido {pedido["codigo"]} está FEITO e agora ESPERANDO GARÇOM.")
        
        elif escolha == "2":
            pedido["status"] = "CANCELADO"
            print(f"Pedido {pedido["codigo"]} foi cancelado.")

def entregar_pedido():
    if len(fila_pedidos_prontos) == 0:
        print("Nenhum pedido pronto para enviar.")
    else:
        pedido = fila_pedidos_prontos.pop(0)
        pedido["status"] = "SAIU PARA ENTREGA"
        fila_pedidos_entrega.append(pedido)
        print(f"Pedido {pedido["codigo"]} de {pedido["nome_cliente"]} SAIU PARA ENTREGA.")

def pedido_entregue():
    if len(fila_pedidos_entrega) == 0:
        print("Nenhum pedido em rota de entrega.")
    else:
        pedido = fila_pedidos_entrega.pop(0)
        pedido["status"] = "ENTREGUE"
        print(f"Pedido {pedido["codigo"]} foi ENTREGUE ao cliente {pedido["nome_cliente"]}.")

def exibir_pedidos():
    print("\n--- LISTA DE PEDIDOS ---")
    for pedido in todos_pedidos:
        print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Status: {pedido["status"]}")
    print("-------------------------\n")

def filtrar_pedidos():
    print("----- TODOS OS STATUS -----")
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
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "AGUARDANDO APROVACAO":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe mais pedidos com esse status no momento.")
            
        case "2":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "ACEITO":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
                    
        case "3":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "FAZENDO":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
                
        case "4":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "FEITO":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
                
        case "5":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "ESPERANDO GARÇOM":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
                
        case "6":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "SAIU PARA ENTREGA":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
                
        case "7":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "ENTREGUE":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
                
        case "8":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "CANCELADO":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
                
        case "9":
            busca_sucedida = False
            for pedido in todos_pedidos:
                if pedido["status"] == "REJEITADO":
                    print(f"Código: {pedido["codigo"]} | Cliente: {pedido["nome_cliente"]} | Itens: {pedido["itens"]} | Status: {pedido["status"]} | Valor do Pedido: {pedido["valor_total"]:.2f}")
                    busca_sucedida = True
            if not busca_sucedida:
                print("Não existe pedidos com esse status no momento.")
            
def menu_pedidos():
    sair = 1
    while sair != 0:
        print("\n ------ SISTEMA DE PEDIDOS ------")
        print("1 - Criar Pedido")
        print("2 - Processar Pedido Pendente")
        print("3 - Preparar Pedido")
        print("4 - Enviar para a Mesa")
        print("5 - Finalizar Entrega")
        print("6 - Exibir todos os pedidos")
        print("7 - Filtrar pedidos por status")
        print("8 - Voltar ao menu anterior")
        print("9 - Sair")
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
                            print("No momento estamos em falta deste item. Sentimos muito por isso ☹️")
                        break
                if not item_encontrado:
                    print("Item não encontrado, tente novamente.")

            case "2":
                processar_pedido()
            case "3":
                preparar_pedido()
            case "4":
                entregar_pedido()
            case "5":
                pedido_entregue()
            case "6":
                exibir_pedidos()
            case "7":
                filtrar_pedidos()
            case "8":
                menu_principal()
            case "9":
                sair = 0
                print("Saindo do sistema...")
            case _:
                print("Opção inválida, tente de novo.")

menu_pedidos()
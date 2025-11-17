import app.app as app

def menu():
    print("\n=== MINI BLOCKCHAIN CLI ===")
    print("1 - Cadastrar usuário")
    print("2 - Login")
    print("3 - Transferir")
    print("4 - Ver saldos")
    print("5 - Ver blockchain")
    print("0 - Sair")

while True:
    menu()
    op = input("Escolha: ")

    if op == "1":
        u = input("Usuário: ")
        if app.cadastrar_usuario(u):
            print("Cadastrado!")
        else:
            print("Usuário já existe.")

    elif op == "2":
        u = input("Usuário: ")
        s = input("Senha: ")
        print("Login OK!" if app.login(u,s) else "Falhou.")

    elif op == "3":
        de = input("De: ")
        para = input("Para: ")
        val = int(input("Valor: "))
        if app.transferir(de, para, val):
            print("Transferido!")
        else:
            print("Erro na transferência.")

    elif op == "4":
        print(app.users)

    elif op == "5":
        for b in app.blockchain.chain:
            print(vars(b))

    elif op == "0":
        break

    else:
        print("Opção inválida.")

from Class_Calculadora import Calculadora

decisao = "S"
while decisao == "S":
    operador = input("Escolha a operação (+,-,/,*) que você deseja realizar: ")
    while operador != "+" and operador != "-" and operador != "/" and operador != "*":
        operador = input("Ops, parece que você digitou algo errado\n"
                         "Digite novamente a operação (+,-,/,*) que você deseja realizar: ")

    num1 = int(input("Digite o primeiro número: "))
    num2 = int(input("Digite o segundo número: "))

    calculadora = Calculadora(num1, num2)

    if operador == "+":
        print(calculadora.soma())
    if operador == "-":
        print(calculadora.subtracao())
    if operador == "/":
        print(calculadora.divisao())
    if operador == "*":
        print(calculadora.multipicacao())

    decisao = input("Deseja continuar?s/n ").upper()
    if decisao == "S" and decisao == "N":
        pass
    else:
        while decisao != "S" and decisao != "N":
            decisao = input("Você digitou algo errado!!\n"
            "Digite a letra (s) para continuar ou (n) para sair! ").upper()


print("Saiu da calculadora")
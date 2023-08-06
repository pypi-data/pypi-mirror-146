def tipo_ordem ():
    # TODO: Complete os espaços em branco com uma possível solução para o problema.
    print('Informe 2 números (para interromper informe números iguais): ')
    X, Y = map(int, input().split())
    while (X != Y):
        floor = min(X, Y)
        top = max(X, Y)
        if (floor == X):
            print("Crescente")
        elif (top == X):
            print("Decrescente")
        X, Y = map(int, input().split())
    return ''
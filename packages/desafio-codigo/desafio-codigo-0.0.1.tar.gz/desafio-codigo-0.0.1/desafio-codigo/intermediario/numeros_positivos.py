def quantidade_positivos (qtd):
    print('Informe {} os números:'.format(qtd))
    counter = 0
    for _ in range(qtd):
        number = float(input())
        if number > 0:
            counter += 1

    return "{} valores positivos".format(counter)
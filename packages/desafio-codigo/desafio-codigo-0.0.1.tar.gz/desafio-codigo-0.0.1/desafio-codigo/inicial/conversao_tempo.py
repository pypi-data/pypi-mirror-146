def tempo_horas (segundos):
    # TODO Implementar a formula para calcular os minutos.
    minutos = (segundos // 60)
    segundos = int(segundos - (minutos * 60))
    # TODO Implementar a formula para calcular as horas.
    horas = (minutos // 60)
    minutos = int(minutos - (horas * 60))

    return "{}:{}:{}".format(horas, minutos, segundos)
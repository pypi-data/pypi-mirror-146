# desafio_codigo

Description. 
The package desafio-codigo is used to:
	Desafio Inicial:
		- Desafio da Média
		- Desafio do Triângulo
		- Desafio da Conversão de Tempo
	Desafio Intermediário:
		- Desafio dos Números Positivos
		- Desafio Crescente e Decrescente
		- Desafio do Resto de divisão
	Desafio Final:
		- Desafio dos Números Primos
		- Desafio do Vetor
		- Desafio do Encaixa e Não encaixa

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install desafi-codigo

```bash
pip install desafio-codigo
```

## Usage

```python
from desafio-codigo.inicial import media
media.calc_media(5.1, 7.0)

from desafio-codigo.inicial import triangulo
triangulo.perimetro_area([6.0, 4.0, 2.0])

from desafio-codigo.inicial import conversao_tempo
conversao_tempo.tempo_horas(556)

from desafio-codigo.intermediario import crescente_decrescente
crescente_decrescente.tipo_ordem()

from desafio-codigo.intermediario import numeros_positivos
numeros_positivos.quantidade_positivos(3):

from desafio-codigo.intermediario import resto_divisao
resto_divisao.umeros_intervalo(10, 18)

from desafio-codigo.final import numero_primo
numero_primo.primo(3)

from desafio-codigo.final import vetor
vetor.vetor_dobro(4, 10)

from desafio-codigo.final import encaixa
encaixa.encaixa(3)
```

## Author
Eric Cunha

## License
[MIT](https://choosealicense.com/licenses/mit/)
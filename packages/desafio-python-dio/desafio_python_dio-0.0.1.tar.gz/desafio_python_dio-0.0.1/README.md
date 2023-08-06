# desafio_python_dio

Description. 
The package desafio_python_dio is used to:
	Desafio Inicial:
		- Desafio da Media
		- Desafio do Triangulo
		- Desafio da Conversao de Tempo
	Desafio Intermediario:
		- Desafio dos Numeros Positivos
		- Desafio Crescente e Decrescente
		- Desafio do Resto de divisao
	Desafio Final:
		- Desafio dos Numeros Primos
		- Desafio do Vetor
		- Desafio do Encaixa e Nao encaixa

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install desafio_python_dio

```bash
pip install desafio_python_dio
```

## Usage

```python
from desafio_python_dio.inicial import media
media.calc_media(5.1, 7.0)

from desafio_python_dio.inicial import triangulo
triangulo.perimetro_area([6.0, 4.0, 2.0])

from desafio_python_dio.inicial import conversao_tempo
conversao_tempo.tempo_horas(556)

from desafio_python_dio.intermediario import crescente_decrescente
crescente_decrescente.tipo_ordem()

from desafio_python_dio.intermediario import numeros_positivos
numeros_positivos.quantidade_positivos(3)

from desafio_python_dio.intermediario import resto_divisao
resto_divisao.umeros_intervalo(10, 18)

from desafio_python_dio.final import numero_primo
numero_primo.primo(3)

from desafio_python_dio.final import vetor
vetor.vetor_dobro(4, 10)

from desafio_python_dio.final import encaixa
encaixa.encaixa(3)
```

## Author
Eric Cunha

## License
[MIT](https://choosealicense.com/licenses/mit/)
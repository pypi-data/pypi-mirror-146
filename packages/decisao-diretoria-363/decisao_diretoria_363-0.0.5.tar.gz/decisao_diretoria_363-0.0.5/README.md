# Decisão de Diretoria CETESB 363/11

[![Publish Python 🐍 distributions 📦 to PyPI](https://github.com/gaemapiracicaba/norma_dd_363_11/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/gaemapiracicaba/norma_dd_363_11/actions/workflows/publish-to-pypi.yml)
<br>
[![Publish Python 🐍 distributions 📦 to TestPyPI](https://github.com/gaemapiracicaba/norma_dd_363_11/actions/workflows/publish-to-test-pypi.yml/badge.svg)](https://github.com/gaemapiracicaba/norma_dd_363_11/actions/workflows/publish-to-test-pypi.yml)

<br>

Por meio da [Decisão de Diretoria da CETESB nº 363 de 07.12.2011](https://github.com/gaemapiracicaba/norma_dd_363_11/blob/main/docs/2011.12.07%20-%20Decisão%20Diretoria%20363%20-%20E%20coli.pdf), que 
*"dispõe sobre a adoção do parâmetro E.coli, para avaliação da qualidade
dos corpos de águas do território do Estado de São Paulo"*, é adotado o 
parâmetro *Escherichia coli* em substituição aos Coliformes Termotolerantes,
estabelecidos pelas Resoluções CONAMA nº 357/2005, de 17.03.2005, e 274/2000, 
de 29.11.2000.

<br>

----

### Objetivo

<br>

O projeto objetiva disponibilizar os parâmetros de qualidade em formato adequado para utilização em análises computacionais.

<br>

----

### Como Instalar?

<br>

```bash
pip3 install decisao-diretoria-363 --upgrade
```

<br>

----

### Como Usar?

<br>

```python
from normas import decisao_diretoria_363

# Get Table
df_363, list_classes = decisao_diretoria_363.get_parameters()

# Filter Data by "Classe"
df_363, list_parametros = decisao_diretoria_363.filter_by_classe(df_363, classe='Classe 3')

# Filter Data by "Parâmetro", quando tem condições distintas!
dict_363 = decisao_diretoria_363.filter_by_parameters(df_363, parametro='Escherichia coli', condicao=1)
print(dict_363)
```

<br>

-----

### Testes

Caso queira testar, segue um [*Google Colab*](https://colab.research.google.com/drive/1BTUYs3Nwdfm5V3KIEB57lWtNT1R7_RJb?usp=sharing).

<br>

------

### *TODO*

1. ...

# Download e Extração de Dados Climáticos do INMET

* Este projeto foi desenvolvido como parte do trabalho do Instituto Federal da Paraíba (IFPB) para o "**Construção de Dashboards para Auxílio na Análise de Dados Meteorológicos**", coordenado por *Valnyr Vasconcelos Lira*. O objetivo principal deste projeto é fornecer uma ferramenta eficiente para a extração e processamento de dados anuais fornecidos pelo INMET ([INMET Portal](https://portal.inmet.gov.br/uploads/dadoshistoricos)).
* O projeto facilita o acesso a dados climáticos históricos, armazenados em formato ZIP, e permite seu processamento para análise. Além disso, inclui uma opção de integração com o banco de dados MongoDB. No entanto, a integração com o MongoDB é opcional, permitindo ao usuário optar por não utilizá-la, se assim desejar.

## Instalação

Certifique-se de ter o Python 3.x instalado em seu ambiente. Instale as dependências necessárias utilizando `pip`:

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

2. Baixe as dependências:

```bash
pip install requests
pip install pandas
pip install shutil
pip install zipfile
```

## Instruções de Execução e Uso

### Inicialização

Crie uma instância da classe `DownloadInmetData` fornecendo o caminho para o diretório onde os dados serão baixados. Se o diretório não existir, ele será criado automaticamente.

```python
from download_inmet_data import DownloadInmetData

baixador = DownloadInmetData(path="data/years")
```

### Exemplos de Comandos

Baixe dados de anos específicos. *Os dados serão armazenados em arquivos ZIP no diretório configurado, extraidos e separados por região e estados.*

```python
from download_inmet_data import DownloadInmetData

# Exemplo de uso
baixador = DownloadInmetData()
# Baixar dados correspondente ao ano de 2024
baixador.download_data_by_year(2024)
```

> *Lembre-se de que o ano especificado como parâmetro **deve estar dentro do intervalo de anos disponibilizado pelo INMET**. Caso contrário, o programa não conseguirá realizar o download dos dados.Lembrando que, o ano passado como parametro precisar estar num intervalo disponivel fornecido pelo inmet, caso contrario o programa não conseguira baixar*

### Extrair Dados por Estado

Após o download dos arquivos ZIP, você pode extrair e tratar os dados por estado. Especifique o ano, região e estado para os quais os dados devem ser movidos.

```python
from collect_inmet_data import CollectInmetData

# Crie uma nova instancia
''' Forneça o diretório principal onde ele irá coletar os dados 
    (Coloque o mesmo que você usou para baixar os dados)
'''
collect = CollectInmetData(path="data/years")
data = collect.extract_inmet_data(2024, "NE", "PB")
```

o método `extract_inmet_data(year:int, region:str, state:str` retorna um valor do tipo `dict`.

Estrutura dos valores retornados:

```json
{
    "NOME_ESTAÇÃO-ESTADO-CODIGO_ESTAÇÃO":
    {
        "UF": "X",
        "ESTACAO": "Y",
        "CODIGO": "A---",
        "LATITUDE": "W",
        "lONGITUDE": "Z",
        "DADOS": [
            "DATA": "XX-YY-ZZZZ",
            "HORA": "VVVV UTC",
            "PRECIPITACAO_TOTAL": X,
            "PRESSAO_ATMOSFERICA_NIVEL_ESTACAO": Y,
            "PRESSAO_ATMOSFERICA_MAX": Z,
            ...
            "VENTO_RAJADA_MAX": A,
            "VENTO_VELOCIDADE": B
        ]
    }
}
```

> O valor do tipo dicionário pode ser utilizado de diversas maneiras, incluindo o armazenamento de dados em um banco de dados, a resposta a uma API, a geração de arquivos, entre outras aplicações. Este projeto inclui uma integração opcional com o banco de dados MongoDB. No entanto, uma vez que a **implementação do banco de dados é facultativa**, não serão fornecidos detalhes específicos sobre como utilizá-lo e integrá-lo ao projeto.

### Funções Internas

- **`__create_folders(self, path_name:str) -> str`**: Cria um diretório se ele não existir.
- **`__extract_zip_files(self, zip_path:str, year:int)`**: Extrai um arquivo ZIP para um diretório específico.
- **`__organize_inmet_files(self, path_name:str)`**: Organiza os arquivos, separando eles por região e estado.
- **`__get_files_list(self, year:int, region:str, state:str) -> list`**: Retorna uma lista dos arquivos presente no diretório.
- **`__process_data(self,dataframe: pd.DataFrame) -> pd.DataFrame`**: Faz o tratamento dos dados.

## Contribuindo

Se você deseja contribuir para este projeto, sinta-se à vontade para enviar pull requests ou abrir issues com sugestões e correções.

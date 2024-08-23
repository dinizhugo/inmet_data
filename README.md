# ExtractInmetData

`ExtractInmetData` é uma classe Python para gerenciar o download e a extração de dados históricos meteorológicos do INMET. A classe suporta a realização das seguintes operações:

- **Baixar dados de anos específicos**: Faz o download de arquivos ZIP contendo dados meteorológicos para os anos especificados.
- **Extrair e organizar dados por estado**: Organiza e move arquivos extraídos para diretórios específicos baseados na região e no estado.

## Instalação

Certifique-se de ter o Python 3.x instalado em seu ambiente. Instale as dependências necessárias utilizando `pip`:

```bash
pip install requests
```

## Uso

### Inicialização

Crie uma instância da classe `ExtractInmetData` fornecendo o caminho para o diretório onde os dados serão armazenados. Se o diretório não existir, ele será criado automaticamente.

```python
from extract_inmet_data import ExtractInmetData

inmet_data = ExtractInmetData(path="data/years")
```

### Baixar Dados

Baixe dados de anos específicos. Os dados serão armazenados em arquivos ZIP no diretório configurado.

```python
inmet_data.baixar_dados_por_ano([2024])
```

### Extrair Dados por Estado

Após o download dos arquivos ZIP, você pode extrair e organizar os dados por estado. Especifique a região e o estado para os quais os dados devem ser movidos.

```python
inmet_data.get_dados_por_estado([2024], "dataPrev", "CO", "BA")
```

### Funções Internas

- **`__baixar_arquivo(url: str, destino: str)`**: Faz o download de um arquivo a partir de uma URL.
- **`__extrair_arquivo_zip(zip_path: str, ano: int)`**: Extrai um arquivo ZIP para um diretório específico.
- **`__criar_pasta(path: str)`**: Cria um diretório se ele não existir.
- **`__verificar_pasta(path: str) -> bool`**: Verifica se um diretório existe.
- **`__parse_filename(filename: str) -> dict`**: Analisa o nome do arquivo para extrair informações como região, estado e datas.

## Exemplo

```python
# Criar uma instância da classe
inmet_data = ExtractInmetData()

# Baixar dados para o ano de 2024
inmet_data.baixar_dados_por_ano([2024])

# Extrair e organizar dados para a região CO e estado BA
inmet_data.get_dados_por_estado([2024], "dataPrev", "CO", "BA")
```

## Contribuindo

Se você deseja contribuir para este projeto, sinta-se à vontade para enviar pull requests ou abrir issues com sugestões e correções.

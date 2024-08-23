import os
import re
import requests
import shutil
from zipfile import BadZipFile, ZipFile

class ExtractInmetData:
    def __init__(self, path: str="data/years") -> None:
        self.__BASE_URL = "https://portal.inmet.gov.br/uploads/dadoshistoricos"
        if not self.__verificar_pasta(path):
            self.__criar_pasta(path)
        
        self.__base_path = path
        
    def baixar_dados_por_ano(self, anos):
        if isinstance(anos, range):
            anos = list(anos)
            
        for ano in anos:
            print(f'Processando ano: {ano}')
            current_path = os.path.join(self.__base_path, str(ano))
            if not self.__verificar_pasta(current_path):
                self.__criar_pasta(current_path)
            
            url = f'{self.__BASE_URL}/{ano}.zip'
            arquivo_destino = os.path.join(current_path, f'{ano}.zip')
            self.__baixar_arquivo(url, arquivo_destino)
            self.__extrair_arquivo_zip(arquivo_destino, ano)
            
    def separar_dados_por_estado(self, anos, destino: str, regiao:str, estado:str):
        if isinstance(anos, range):
            anos = list(anos)
            
        if self.get_estado(regiao, estado):
            for ano in anos:
                path = os.path.join(self.__base_path, str(ano))
                if os.path.exists(path):
                    files_name = os.listdir(path);
                    self.__extrair_dados_por_estado(files_name, path, destino, regiao, estado)
    
    def get_estado(self, regiao: str, estado: str):
        regioes = {
            "CO": ["DF", "GO", "MS", "MT"],
            "N":  ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
            "NE": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
            "S":  ["PR", "RS", "SC"],
            "SE": ["ES", "MG", "RJ", "SP"]
        }
        
        if regiao in regioes:
            if estado in regioes[regiao]:
                return True
            else:
                print(f"Estado '{estado}' não encontrada.")
                return False
        else:
            print(f"Região '{regiao}' não encontrada.")
            return False
        
    def __extrair_dados_por_estado(self, files:list, path:str, destino:str, regiao:str, estado:str):
        for file in files:
            file_info = self.__parse_filename(file)
            
            if file_info and file_info['region'] == regiao and file_info['state'] == estado:
                region_dir = os.path.join(destino, file_info['region'])
                state_dir = os.path.join(region_dir, file_info['state'])
                
                self.__criar_pasta(state_dir)
                
                src_path = os.path.join(path, file)
                if os.path.exists(src_path):
                    dest_path = os.path.join(state_dir, file)
                    shutil.move(src_path, dest_path)
                    print(f"Arquivo movido para: {dest_path}")
                else:
                    print(f"Arquivo não encontrado: {src_path}")


    
    def __parse_filename(self, filename) -> dict:
        # Padrão revisado para capturar todos os detalhes
        pattern = r'^INMET_(\w{1,2})_(\w{2})_(\w{4})_([^_]+?)_(\d{2}-\d{2}-\d{4})_A_(\d{2}-\d{2}-\d{4})\.CSV$'
        
        match = re.fullmatch(pattern, filename)
        
        if match:
            return {
            'region': match.group(1),
            'state': match.group(2),
            'station_code': match.group(3),
            'station_name': match.group(4),
            'start_date': match.group(5),
            'end_date': match.group(6)
        }
        return None            
    
    def __baixar_arquivo(self, url: str, destino: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança um erro se o download falhar
            with open(destino, 'wb') as f:
                f.write(response.content)
            print(f'Arquivo baixado com sucesso: {destino}')
        except requests.exceptions.RequestException as e:
            print(f'Erro ao baixar o arquivo: {e}')
    
    def __extrair_arquivo_zip(self, zip_path: str, ano: int):
        extract_path = os.path.join(self.__base_path, str(ano))
        
        # Garantir que o diretório de extração exista
        os.makedirs(extract_path, exist_ok=True)
        
        try:
            with ZipFile(zip_path, 'r') as zip_file:
                # Listar todos os arquivos e diretórios no ZIP
                zip_files = zip_file.namelist()

                # Verificar se há um diretório principal com o mesmo nome do ano
                if any(file.startswith(f"{ano}/") for file in zip_files):
                    # Extrair todos os arquivos do ZIP
                    for file_info in zip_file.infolist():
                        # Se o caminho do arquivo começa com o ano, extrai para o diretório do ano
                        target_path = os.path.join(extract_path, os.path.relpath(file_info.filename, f"{ano}/"))
                        if file_info.is_dir():
                            os.makedirs(target_path, exist_ok=True)
                        else:
                            with zip_file.open(file_info) as source, open(target_path, 'wb') as target:
                                shutil.copyfileobj(source, target)   
                else:
                    # Se não houver diretório principal, verificar se o arquivo ZIP contém dados
                    if zip_files:
                        zip_file.extractall(extract_path)
                    else:
                        print(f"Nenhum dado encontrado no arquivo ZIP para o ano {ano}.")
                
                print(f"Arquivo extraído para {extract_path}\n")
                
        except FileNotFoundError:
            print(f"Arquivo ZIP não encontrado: {zip_path}")
        except BadZipFile:
            print(f"O arquivo não é um ZIP válido: {zip_path}")
        except Exception as e:
            print(f"Ocorreu um erro ao extrair o arquivo: {e}")
        finally:
            if os.path.exists(zip_path):
                try:
                    os.remove(zip_path)
                    print(f"Arquivo ZIP removido: {zip_path}")
                except OSError as e:
                    print(f"Erro ao remover o arquivo ZIP: {e}")

    def __criar_pasta(self, path: str):
        if not self.__verificar_pasta(path):
            os.makedirs(path)
            print(f'Pasta criada: {path}')
    
    def __verificar_pasta(self, path: str) -> bool:
        return os.path.exists(path)
    
import os
import requests
import shutil
from util.parse_file import ParseFile
from zipfile import BadZipFile, ZipFile
from requests import RequestException

class DownloadInmetData:
    def __init__(self, path:str="data/years"):
        self._base_path = self.__create_folders(path)
        self._INMET_URL = 'https://portal.inmet.gov.br/uploads/dadoshistoricos'
        
    def download_data_by_year(self, year:int):
        print(f">> Baixando dados correspondente ao ano: {year}\n")
        
        current_path = self.__create_folders(os.path.join(self._base_path, str(year)))
        current_url = f'{self._INMET_URL}/{str(year)}.zip'
        
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            
            destination_path = os.path.join(current_path, f'{year}.zip')
            
            with open(destination_path, 'wb') as file:
                file.write(response.content)
            print(f">> O arquivo {current_url} foi baixado com sucesso!\n")
            
            print(">> Extraindo os arquivos...")
            self.__extract_zip_files(current_path, year)
            
            print(">> Organizando arquivos...")
            self.__organize_inmet_files(current_path)
        
            print(">> Download concluido com sucesso!\n")    
        except RequestException as e:
            print(f"[Error] Ocorreu um erro ao tentar baixar o arquivo. Erro: {e}")
        
    
    def __create_folders(self, path_name:str) -> str:
        os.makedirs(path_name, exist_ok=True)
        return path_name
    
    def __extract_zip_files(self, zip_path:str, year:int):
        zip_file_path = os.path.join(zip_path, f'{str(year)}.zip')
        
        try:
            with ZipFile(zip_file_path, 'r') as zip_file:
                zip_files = zip_file.namelist()
                
                if any(file.startswith(f'{str(year)}/') for file in zip_files):
                    
                    for file_info in zip_file.infolist():
                        target_path = os.path.join(zip_path, os.path.relpath(file_info.filename, f"{str(year)}/"))
                        
                        if file_info.is_dir():
                            self.__create_folders(target_path)
                        else:
                            with zip_file.open(file_info) as source, open(target_path, 'wb') as target:
                                shutil.copyfileobj(source, target)
                else:
                    if zip_files:
                        zip_file.extractall(zip_path)
                    else:
                        print(f"[ERROR] Nenhum dado encontrado no arquivo ZIP para o ano {str(year)}.")
                        
                print(f">> Arquivo do ano {str(year)} extraido com sucesso!\n")
                
        except FileNotFoundError:
            print(f"[ERROR] O arquivo ZIP não encontrado: {zip_path}")
        except BadZipFile:
            print(f"[ERROR] O arquivo não é um ZIP válido: {zip_path}")
        except Exception as e:
            print(f"[ERROR] Ocorreu um erro ao extrair o arquivo: {e}")
        finally:
            if os.path.exists(zip_file_path):
                try:
                    os.remove(zip_file_path)
                except OSError as e:
                    print(f"[ERROR] Erro ao remover o arquivo ZIP: {e}")
    
    def __organize_inmet_files(self, path_name:str):
        list_files = os.listdir(path_name)
        
        for filename in list_files:
            file_info = ParseFile.parse_filename(filename)
            
            if file_info:
                region_dir = os.path.join(path_name, file_info['region'])
                state_dir = os.path.join(region_dir, file_info['state'])
                
                self.__create_folders(state_dir)
                
                current_path_file = os.path.join(path_name, filename)
                
                if os.path.exists(current_path_file):
                    destination_path = os.path.join(state_dir, filename)
                    shutil.move(current_path_file, destination_path)
                else:
                    print(f"[ERROR] Não foi possivel encontrar o arquivo: {current_path_file}.\n")
                
        print(f">> Os Arquivo foram movidos com sucesso!\n")
                    

inmet_data = DownloadInmetData()
inmet_data.download_data_by_year(2024)
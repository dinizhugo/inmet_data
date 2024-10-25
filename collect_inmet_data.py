import os
import pandas as pd
from datetime import datetime

class CollectInmetData:
    def __init__(self, path:str):
        if not os.path.exists(path):
            print("[Error] Não foi possivel encontrar um diretorio com esse nome.")
            print("[Error] Execute primeiro o 'download_inmet_data.py' para coletar os dados do inmet.")
            return None
        self._base_path = path
        self._DEFAULT_COLUMNS = [
            'DATA', 'HORA', 'PRECIPITACAO_TOTAL', 'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO', 'PRESSAO_ATMOSFERICA_MAX','PRESSAO_ATMOSFERICA_MIN', 'RADIACAO_GLOBAL', 'TEMP_BULBO_SECO', 'TEMP_PONTO_ORVALHO', 'TEMP_MAX','TEMP_MIN','TEMP_ORVALHO_MAX','TEMP_ORVALHO_MIN', 'UMIDADE_RELATIVA_MAX','UMIDADE_RELATIVA_MIN','UMIDADE_RELATIVA','VENTO_DIRECAO','VENTO_RAJADA_MAX','VENTO_VELOCIDADE'
        ]
        self.COLUMNS_TO_NUMERIC = [
            'PRECIPITACAO_TOTAL', 'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO', 'PRESSAO_ATMOSFERICA_MAX', 
            'PRESSAO_ATMOSFERICA_MIN', 'RADIACAO_GLOBAL', 'TEMP_BULBO_SECO', 'TEMP_PONTO_ORVALHO', 
            'TEMP_MAX', 'TEMP_MIN', 'TEMP_ORVALHO_MAX', 'TEMP_ORVALHO_MIN', 'VENTO_RAJADA_MAX', 
            'VENTO_VELOCIDADE', 'UMIDADE_RELATIVA_MAX', 'UMIDADE_RELATIVA_MIN', 
            'UMIDADE_RELATIVA', 'VENTO_DIRECAO'
        ]
    
    def extract_inmet_header_data(self, year: int, region: str, state: str) -> dict:
        files_list = self.__get_files_list(year, region, state)
        data = {}
        
        for file in files_list:
            temp = {}
            current_path = os.path.join(self._base_path, str(year), region.upper(), state.upper(), file)
            
            header_dataframe = pd.read_csv(current_path, encoding='latin1', on_bad_lines='skip', sep=';', nrows=8, header=None)
            
            uf = header_dataframe.iloc[1, 1]
            estacao = header_dataframe.iloc[2, 1]
            codigo = header_dataframe.iloc[3, 1]
            latitude = header_dataframe.iloc[4, 1]
            longitude = header_dataframe.iloc[5, 1]
            data_fundacao = header_dataframe.iloc[7, 1]
            
            data_fundacao = datetime.strptime(data_fundacao, "%d/%m/%y").strftime("%d/%m/%Y")
            
            temp['UF'] = uf
            temp['ESTACAO'] = estacao
            temp['CODIGO'] = codigo
            temp['LATITUDE'] = latitude
            temp['LONGITUDE'] = longitude
            temp['DATA_FUNDAÇÃO'] = data_fundacao
            
            key = f"{codigo}"
            
            data[key] = temp
            
        return data
    
    def extract_inmet_data(self, year:int, region:str, state:str) -> dict:
        files_list = self.__get_files_list(year, region, state)
        data = {}
        
        for file in files_list:
            temp = {}
            current_path = os.path.join(self._base_path, str(year), region.upper(), state.upper(), file)
            
            header_dataframe = pd.read_csv(current_path, encoding='latin1', on_bad_lines='skip', sep=';', nrows=8, header=None)
            main_dataframe = pd.read_csv(current_path, encoding='latin1', on_bad_lines='skip', sep=';', skiprows=8, na_values=['', 'NULL'])
            
            main_dataframe = self.__process_data(main_dataframe)
            
            codigo = header_dataframe.iloc[3, 1]
           
            temp['CODIGO'] = codigo
            
            dataframe_temp = main_dataframe.iloc[:, :19]
            dataframe_temp.columns = self._DEFAULT_COLUMNS
            
            grouped_data = dataframe_temp.groupby('DATA').agg({
            'PRECIPITACAO_TOTAL': 'mean',
            'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO': 'mean',
            'PRESSAO_ATMOSFERICA_MAX': 'mean',
            'PRESSAO_ATMOSFERICA_MIN': 'mean',
            'RADIACAO_GLOBAL': 'mean',
            'TEMP_BULBO_SECO': 'mean',
            'TEMP_PONTO_ORVALHO': 'mean',
            'TEMP_MAX': 'mean',
            'TEMP_MIN': 'mean',
            'TEMP_ORVALHO_MAX': 'mean',
            'TEMP_ORVALHO_MIN': 'mean',
            'UMIDADE_RELATIVA_MAX': 'mean',
            'UMIDADE_RELATIVA_MIN': 'mean',
            'UMIDADE_RELATIVA': 'mean',
            'VENTO_RAJADA_MAX': 'mean',
            'VENTO_VELOCIDADE': 'mean',
            'VENTO_DIRECAO': 'mean'
        }).reset_index()
            
            for _, row in grouped_data.iterrows():
                date = row['DATA']
                daily_register = {
                    'CODIGO': codigo,
                    'DATA': date,
                    'MEDICOES': []
                }
                
                # Adiciona as médias calculadas ao registro diário
                daily_register.update({f'MEDIA_{col}': row[col] for col in grouped_data.columns if col != 'DATA'})
                
                # Coletando medições horárias
                hourly_data = dataframe_temp[dataframe_temp['DATA'] == date]
                for _, hour_row in hourly_data.iterrows():
                    hour_register = {
                        'HORA': hour_row['HORA'],
                        'PRECIPITACAO_TOTAL': hour_row['PRECIPITACAO_TOTAL'],
                        'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO': hour_row['PRESSAO_ATMOSFERICA_NIVEL_ESTACAO'],
                        'PRESSAO_ATMOSFERICA_MAX': hour_row['PRESSAO_ATMOSFERICA_MAX'],
                        'PRESSAO_ATMOSFERICA_MIN': hour_row['PRESSAO_ATMOSFERICA_MIN'],
                        'RADIACAO_GLOBAL': hour_row['RADIACAO_GLOBAL'],
                        'TEMP_BULBO_SECO': hour_row['TEMP_BULBO_SECO'],
                        'TEMP_PONTO_ORVALHO': hour_row['TEMP_PONTO_ORVALHO'],
                        'TEMP_MAX': hour_row['TEMP_MAX'],
                        'TEMP_MIN': hour_row['TEMP_MIN'],
                        'TEMP_ORVALHO_MAX': hour_row['TEMP_ORVALHO_MAX'],
                        'TEMP_ORVALHO_MIN': hour_row['TEMP_ORVALHO_MIN'], 
                        'UMIDADE_RELATIVA_MAX': hour_row['UMIDADE_RELATIVA_MAX'],
                        'UMIDADE_RELATIVA_MIN': hour_row['UMIDADE_RELATIVA_MIN'],
                        'UMIDADE_RELATIVA': hour_row['UMIDADE_RELATIVA'],
                        'VENTO_DIRECAO': hour_row['VENTO_DIRECAO'],
                        'VENTO_RAJADA_MAX': hour_row['VENTO_RAJADA_MAX'],
                        'VENTO_VELOCIDADE': hour_row['VENTO_VELOCIDADE']
                    }
                    daily_register['MEDICOES'].append(hour_register)

                key = f'{codigo}_{date}'
                data[key] = daily_register  

        return data
        
    def __get_files_list(self, year:int, region:str, state:str) -> list:
        search_path = os.path.join(self._base_path, str(year), region.upper(), state.upper())
        
        if os.path.exists(search_path):
            return os.listdir(search_path)
        print(f"[ERROR] Não foi possivel encontrar arquivos no diretorio: {search_path}")
    
    def __process_data(self,dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.iloc[:, :len(self._DEFAULT_COLUMNS)]
        dataframe.columns = self._DEFAULT_COLUMNS
        
        for column in self.COLUMNS_TO_NUMERIC:
            dataframe[column] = pd.to_numeric(dataframe[column].astype(str).str.replace(',', '.'), errors='coerce')
        
        dataframe['DATA'] = pd.to_datetime(dataframe['DATA'], format='%Y/%m/%d').dt.strftime('%Y-%m-%d')
        
        dataframe = dataframe.map(lambda x: None if pd.isna(x) else x)
        
        return dataframe
    
import os
import pandas as pd

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
        
    def extract_inmet_data(self, year:int, region:str, state:str) -> dict:
        files_list = self.__get_files_list(year, region, state)
        data = {}
        
        for file in files_list:
            temp = {}
            current_path = os.path.join(self._base_path, str(year), region.upper(), state.upper(), file)
            
            header_dataframe = pd.read_csv(current_path, encoding='latin1', on_bad_lines='skip', sep=';', nrows=8, header=None)
            main_dataframe = pd.read_csv(current_path, encoding='latin1', on_bad_lines='skip', sep=';', skiprows=8)
            
            main_dataframe = self.__process_data(main_dataframe)
            
            uf = header_dataframe.iloc[1, 1]
            estacao = header_dataframe.iloc[2, 1]
            codigo = header_dataframe.iloc[3, 1]
            latitude = header_dataframe.iloc[4, 1]
            longitude = header_dataframe.iloc[5, 1]
            data_fundacao = header_dataframe.iloc[7, 1]
            
            temp['UF'] = uf
            temp['ESTACAO'] = estacao
            temp['CODIGO'] = codigo
            temp['LATITUDE'] = latitude
            temp['LONGITUDE'] = longitude
            temp['DATA_FUNDAÇÃO'] = data_fundacao
            temp['DADOS'] = []
            
            dataframe_temp = main_dataframe.iloc[:, :19]
            dataframe_temp.columns = self._DEFAULT_COLUMNS
            
            for _, row in dataframe_temp.iterrows():
                register = {
                    'DATA': row['DATA'],
                    'HORA': row['HORA'],
                    'PRECIPITACAO_TOTAL': row['PRECIPITACAO_TOTAL'],
                    'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO': row['PRESSAO_ATMOSFERICA_NIVEL_ESTACAO'],
                    'PRESSAO_ATMOSFERICA_MAX': row['PRESSAO_ATMOSFERICA_MAX'],
                    'PRESSAO_ATMOSFERICA_MIN': row['PRESSAO_ATMOSFERICA_MIN'],
                    'RADIACAO_GLOBAL': row['RADIACAO_GLOBAL'],
                    'TEMP_BULBO_SECO': row['TEMP_BULBO_SECO'],
                    'TEMP_PONTO_ORVALHO': row['TEMP_PONTO_ORVALHO'],
                    'TEMP_MAX': row['TEMP_MAX'],
                    'TEMP_MIN': row['TEMP_MIN'],
                    'TEMP_ORVALHO_MAX': row['TEMP_ORVALHO_MAX'],
                    'TEMP_ORVALHO_MIN': row['TEMP_ORVALHO_MIN'], 
                    'UMIDADE_RELATIVA_MAX': row['UMIDADE_RELATIVA_MAX'],
                    'UMIDADE_RELATIVA_MIN': row['UMIDADE_RELATIVA_MIN'],
                    'UMIDADE_RELATIVA': row['UMIDADE_RELATIVA'],
                    'VENTO_DIRECAO': row['VENTO_DIRECAO'],
                    'VENTO_RAJADA_MAX': row['VENTO_RAJADA_MAX'],
                    'VENTO_VELOCIDADE': row['VENTO_VELOCIDADE']
                }
                temp['DADOS'].append(register)
            
            key = f'{codigo}'
            
            data[key] = temp

        return data
        
    def __get_files_list(self, year:int, region:str, state:str) -> list:
        search_path = os.path.join(self._base_path, str(year), region.upper(), state.upper())
        
        if os.path.exists(search_path):
            return os.listdir(search_path)
        print(f"[ERROR] Não foi possivel encontrar arquivos no diretorio: {search_path}")
    
    def __process_data(self,dataframe: pd.DataFrame) -> pd.DataFrame:
        columns_name = self._DEFAULT_COLUMNS
        
        dataframe = dataframe.iloc[:, :len(columns_name)]
        dataframe.columns = columns_name
        
        columns_to_numeric = [
            'PRECIPITACAO_TOTAL',
            'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO',
            'PRESSAO_ATMOSFERICA_MAX',
            'PRESSAO_ATMOSFERICA_MIN',
            'RADIACAO_GLOBAL',
            'TEMP_BULBO_SECO',
            'TEMP_PONTO_ORVALHO',
            'TEMP_MAX',
            'TEMP_MIN',
            'TEMP_ORVALHO_MAX',
            'TEMP_ORVALHO_MIN',
            'VENTO_RAJADA_MAX',
            'VENTO_VELOCIDADE'
        ]
        
        for column in columns_to_numeric:
            if dataframe[column].dtype == 'object':
                dataframe[column] = pd.to_numeric(dataframe[column].str.replace(',', '.'), errors='coerce')
            else:
                dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')
        
        columns_to_int = [
            'UMIDADE_RELATIVA_MAX',
            'UMIDADE_RELATIVA_MIN',
            'UMIDADE_RELATIVA',
            'VENTO_DIRECAO'
        ]
        for column in columns_to_int:
            dataframe[column] = dataframe[column].astype('Int64')
        
        dataframe['DATA'] = pd.to_datetime(dataframe['DATA'], format='%Y/%m/%d').dt.strftime('%Y-%m-%d')
        
        dataframe = dataframe.map(lambda x: None if pd.isna(x) else x)
        
        return dataframe
    
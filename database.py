import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from collect_inmet_data import CollectInmetData

class MongoDB:
    def __init__(self, connection_string):
        try:
            self.__client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            self.__client.admin.command('ping')
            print(">> Conexão com o MongoDB estabelecida com sucesso!\n")

            self.DB = 'projeto_valnyr'
        except ConnectionFailure as e:
            print("[ERROR] Não foi possivel se conectar com o banco de dados.\n")

    def get_data_base(self):
        if self.__client:
            db = self.__client[self.DB]
            # db['colecao_inicial'].insert_one({'chave_inicial': 'valor_inicial'})
            return db
        else:
            print("[ERROR] Acesso ao banco de dados falhou. Conexão não estabelecida. \n")            
            return None
    
    def get_collection(self, name):
        collection_name = str(name)
        db = self.get_data_base()
        if db is not None:
            return db[collection_name]
        else:
            print("[ERROR] Não foi possível acessar a coleção com esse nome.\n")
            return None
    
    def insert_data_inmet(self, collection_name:str, data:dict):
        print("============ Inserindo dados ===============")
        collection = self.get_collection(collection_name)
        
        if collection is not None:
            try:
                documentos = []
                for chave, valor in data.items():
                    documento = valor
                    documento['_id'] = chave  # Adiciona a chave como o _id do documento
                    documentos.append(documento)
                
                print("Inserindo dados...")
                collection.insert_many(documentos)
                print(f">> O documento foi inserido no banco {collection_name}.\n")
            except DuplicateKeyError:
                pass
                #print("[ERROR] Violação de índice único")
        print("============================================")

        
    def _create_collections(self, collection_names):
        print("============ Criando Coleções ===============")
        if isinstance(collection_names, range):
            collection_names = list(collection_names)
        
        db = self.get_data_base()
        for collection in collection_names:
            name = str(collection)
            if name in db.list_collection_names():
                print("[ERROR] Já existe uma coleção com esse nome.\n")
            else:
                db.create_collection(name)
                print(f">> A coleção foi '{name}' criado com  sucesso!\n")
        print("=================================================\n")
    
    # Uso apenas para testes, se todas as coleções forem deletadas
    # O banco deixa de existir!   
    def _drop_all_collections(self):
        db = self.get_data_base()
        if db.list_collection_names():
            for collection_name in db.list_collection_names():
                db[collection_name].drop()
        else:
            print("[ERROR] O banco não possuí nenhuma coleção.")

mongo = MongoDB('mongodb://localhost:27017/')
data_years = range(2020,2025)
mongo._create_collections(data_years)

#Testes de inserção no banco
collect = CollectInmetData("data/years")
json = collect.extract_inmet_data(2024, "NE", "PB")
mongo.insert_data_inmet("2024", json)
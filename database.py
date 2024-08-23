from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from inmet_data import ExtractInmetData

class MongoDB:
    def __init__(self, connection_string):
        try:
            self.__client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            self.__client.admin.command('ping')
            print(">> Conexão com o MongoDB estabelecida com sucesso!")

            self.DB = 'projeto_valnyr'
        except ConnectionFailure as e:
            print("[ERROR] Não foi possivel se conectar com o banco de dados.")

    def get_data_base(self):
        if self.__client:
            db = self.__client[self.DB]
            # db['colecao_inicial'].insert_one({'chave_inicial': 'valor_inicial'})
            return db
        else:
            print("[ERROR] Acesso ao banco de dados falhou. Conexão não estabelecida.")            
            return None
    
    def get_collection(self, name):
        collection_name = str(name)
        db = self.get_data_base()
        if db:
            return db[collection_name]
        else:
            print("[ERROR] Não foi possível acessar a coleção com esse nome.")
            return None
    
    def insert_data_inmet(self, data:dict):
        pass
    
    def _create_collections(self, collection_names):
        if isinstance(collection_names, range):
            collection_names = list(collection_names)
        
        db = self.get_data_base()
        for collection in collection_names:
            name = str(collection)
            if name in db.list_collection_names():
                print("[ERROR] Já existe uma coleção com esse nome.")
            else:
                db.create_collection(name)
                print(f"A coleção foi '{name}' criado com  sucesso!")
    
    # Uso apenas para testes, se todas as coleções forem deletadas
    # O banco deixa de existir!   
    def _drop_all_collections(self):
        db = self.get_data_base()
        if db.list_collection_names():
            for collection_name in db.list_collection_names():
                db[collection_name].drop()
        else:
            print("[ERROR] O banco não possuí nenhuma coleção.")

# inmet_data = ExtractInmetData()
# inmet_data.baixar_dados_por_ano(range(2020, 2025))
# inmet_data.get_dados_por_estado(range(2020, 2025), "data/years", "NE", "PB")

mongo = MongoDB('mongodb://localhost:27017/')
# mongo._drop_all_collections()
data_years = range(2020,2025)
mongo._create_collections(data_years)
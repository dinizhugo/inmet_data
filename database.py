from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

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
      
    def insert_header_data_inmet(self, data: dict):
        collection = self.get_collection("informacoes_estacoes")
        if collection is None:
            self.create_collection("informacoes_estacoes")
            collection = self.get_collection("informacoes_estacoes")
        
        try:
            documentos = []
            for chave, valor in data.items():
                documento = valor
                documento["_id"] = chave
                documentos.append(documento)

            collection.insert_many(documentos)
            print(f">> Documentos inseridos na coleção 'informacoes_estacoes'.\n")
        except Exception as e:
            print(f"[ERROR] Um ou mais documentos já existem com essas chaves.\n error: {e}")

    
    def insert_data_inmet(self, collection_name:str, data:dict):
        print("============ Inserindo dados ===============")
        collection = self.get_collection(collection_name)
        
        if collection is not None:
            try:
                documentos = []
                for chave, valor in data.items():
                    documento = valor
                    documento['_id'] = chave
                    documentos.append(documento)
                
                print("Inserindo dados...")
                collection.insert_many(documentos)
                collection.create_index({'CODIGO': 1, 'DATA':1})
                print(f">> O documento foi inserido no banco {collection_name}.\n")
            except Exception as e:
                print(f"Erro ao inserir os dados: {str(e)}")
        print("============================================")

    def create_collection(self, collection_name: str):
        db = self.get_data_base()
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f">> A coleção '{collection_name}' foi criada com sucesso!\n")
        else:
            print("[ERROR] Já existe uma coleção com esse nome.\n")
        
    def create_collections(self, collection_names):
        print("============ Criando Coleções ===============")
        
        if isinstance(collection_names, range):
            collection_names = list(collection_names)
            
        if isinstance(collection_names, int):
            collection_names = [collection_names]
        
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

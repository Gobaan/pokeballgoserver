from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient
from models import Pokemon
from models.pokemon import PokemonAzureSerilizer
import uncommitable

class Database:
    def __init__(self):
        self.database_client = self.__get_database_client()
        self.table_client = self.__get_table_client()

    def __get_database_client(self):
        credential = AzureNamedKeyCredential(uncommitable.table_storage_account_name, uncommitable.table_storage_key)
        return TableServiceClient(endpoint=f"https://{uncommitable.table_storage_account_name}.table.core.windows.net", credential=credential)


    def __get_table_client(self, recreate_table = False):
        table_name = "Pokemon"
        tables = [table for table in self.database_client.list_tables()]
        if tables and recreate_table:
            self.database_client.delete_table(table_name=table_name)
        if not tables or recreate_table:
            return self.database_client.create_table(table_name=table_name)
        else:
            return self.database_client.get_table_client(table_name=table_name)

    def initialize_pokemon(self, pokemon_names):
        for pokemon_name in pokemon_names:
            pokemon = Pokemon(name=pokemon_name)
            self.table_client.upsert_entity(pokemon.to_entity())

    def find_pokemon(self, name, user='default'):
        name_filter = f"PartitionKey eq '{user}' and RowKey eq '{name}'"
        try:
            entities = self.table_client.query_entities(name_filter)
            first_pokemon = next(entities)
            return PokemonAzureSerilizer.from_entity(first_pokemon)
        except StopIteration:
            return 

    def update_pokemon(self, new_pokemon):
        new_entity = PokemonAzureSerilizer.to_entity(new_pokemon)
        entity = self.table_client.update_entity(entity=new_entity)
        return entity
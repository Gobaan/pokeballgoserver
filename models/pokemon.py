import json

# Make an azure serializer metaclass ?
class PokemonAzureSerilizer:
    @staticmethod
    def to_entity(pokemon):
        return {
            'PartitionKey' : pokemon.user,
            'RowKey': pokemon.name,
            'data': PokemonJSONSerializer.to_json(pokemon),
        }   

    @staticmethod
    def from_entity(entity):
        return PokemonJSONSerializer.from_json(entity['data'])

class PokemonJSONSerializer:
    @staticmethod
    def to_json(pokemon):
        return json.dumps(vars(pokemon))
    
    @staticmethod
    def from_json(pokemon_str):
        p = Pokemon()
        p.__dict__.update(json.loads(pokemon_str))
        return p

class Pokemon:
    def __init__(self, user='default', name=None):
        self.user = user
        self.name = name
        self.target = [0, 0]
        self.test = [0, 0]
        self.leagues = []

    def __repr__(self):
        return f'Pokemon({vars(self)})'
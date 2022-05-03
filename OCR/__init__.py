import logging
import azure.functions as func
import resources
from models.pokemon import PokemonJSONSerializer

MISSING_POKEMON_ERROR = 'No pokemon was found with name: {name}'
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    image = req.files['snapshot']
    text = resources.run_ocr(image)
    name = resources.pokemon_matcher.get_longest_match(text)
    if not name:
        return func.HttpResponse(MISSING_POKEMON_ERROR.format(name=name), status_code=200)

    pokemon = resources.database.find_pokemon(name)
    json_pokemon = PokemonJSONSerializer.to_json(pokemon)
    return func.HttpResponse(json_pokemon)
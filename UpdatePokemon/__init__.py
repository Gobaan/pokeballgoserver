import logging
import azure.functions as func
import logging
import resources

MISSING_POKEMON_ERROR = 'No pokemon was found with name: {name}'
def main(req: func.HttpRequest) -> func.HttpResponse:
    new_target = req.get_json()
    pokemon = resources.database.find_pokemon(new_target['name'])
    if not pokemon:
        return func.HttpResponse(MISSING_POKEMON_ERROR.format(name=pokemon), status_code=200)

    pokemon.target = new_target['target']
    resources.database.update_pokemon(pokemon)
    return func.HttpResponse(f'{pokemon}')
from .database import Database
from .ocr import run_ocr
from .Trie import create_trie

def __get_all_pokemon():
    with open('data/allpokemon.names') as fp:
        names = fp.readlines()
        return (name.lower().strip() for name in names)

def __get_pokemon_matcher():
    pokemon_names = __get_all_pokemon()
    matcher = create_trie(pokemon_names)
    return matcher

pokemon_matcher = __get_pokemon_matcher()
database = Database()

__all__ = ['pokemon_matcher', 'database', 'run_ocr']

def test_me():
    image = '../data/zubat.jpg'
    #text = run_ocr(image)
    text = '9:53 A O AR+ Zubat / CP 517 O 4 O'.lower()
    name = pokemon_matcher.get_longest_match(text)
    raw_pokemon = database.find_pokemon(name)
    print (raw_pokemon)
    raw_pokemon.target = [45, 23]
    database.update_pokemon(raw_pokemon)
    raw_pokemon = database.find_pokemon(name)
    print (raw_pokemon)
from cards.card_database import CardDatabase
from deckbuilding.pokemon.pool import PokemonPool
from deckbuilding.pokemon.selector import PokemonSelector


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


pool = PokemonPool(db)


selector = PokemonSelector(pool)


print("\n=== Best Evolution Lines ===")

lines = selector.get_best_evolution_lines(5)


for line in lines:
    print(
        line,
        "->",
        selector.scorer.score(
            line,
            pool.extractor
        )
    )


print("\n=== Example Evolution Deck Core ===")

cards = selector.build_evolution_line(
    lines[0]
)


for card in cards:
    print(
        card,
        db.get_name(card)
    )


print(
    "\nTotal cards:",
    len(cards)
)


print("\n=== Best Basic Attackers ===")

basics = selector.get_best_basic_attackers(5)


for pokemon in basics:

    print(
        pokemon.card_id,
        pokemon.name,
        "damage:",
        pokemon.max_damage,
        "HP:",
        pokemon.hp,
        "EX:",
        pokemon.is_ex
    )


print("\n=== Best EX Attackers ===")

ex_cards = selector.get_best_ex_attackers(5)


for pokemon in ex_cards:

    print(
        pokemon.card_id,
        pokemon.name,
        "damage:",
        pokemon.max_damage,
        "HP:",
        pokemon.hp
    )
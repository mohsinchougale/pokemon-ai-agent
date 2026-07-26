from cards.card_database import CardDatabase
from deckbuilding.energy.selector import EnergySelector


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


selector = EnergySelector(db)


pokemon = [
    932,   # Mega Emboar ex
    939,   # Mega Feraligatr ex
    1056   # Mega Zygarde ex
]


energies = selector.select_energy(
    pokemon,
    15
)


print(energies)

for e in energies:
    print(
        e,
        db.get_name(e)
    )
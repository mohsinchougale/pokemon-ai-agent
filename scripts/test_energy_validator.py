from cards.card_database import CardDatabase
from deckbuilding.deck import Deck
from deckbuilding.deck_validator import DeckValidator

CSV = "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"


def get_card_id(db, name):
    for card_id in db.cards.index:
        if db.get_name(card_id) == name:
            return card_id
    raise ValueError(f"Card not found: {name}")


def build_deck(pokemon_ids, energy_ids):
    cards = []

    cards.extend(pokemon_ids)

    # Fill trainer slots with Item cards
    trainer_count = 30
    added = 0

    for card_id in db.cards.index:
        if db.is_trainer(card_id):
            cards.append(card_id)
            added += 1
            if added == trainer_count:
                break

    cards.extend(energy_ids)

    while len(cards) < 60:
        cards.append(energy_ids[0])

    return Deck(cards[:60])


db = CardDatabase(CSV)
validator = DeckValidator(db)


print("=" * 60)
print("TEST 1 - Roaring Moon + Darkness Energy")
print("=" * 60)

roaring_moon = get_card_id(db, "Roaring Moon")
dark_energy = db.get_basic_energy_id("Darkness")

deck = build_deck(
    [roaring_moon] * 15,
    [dark_energy] * 15
)

print("Expected: True")
print("Actual  :", validator.validate(deck))


print()
print("=" * 60)
print("TEST 2 - Roaring Moon + Fire Energy")
print("=" * 60)

fire_energy = db.get_basic_energy_id("Fire")

deck = build_deck(
    [roaring_moon] * 15,
    [fire_energy] * 15
)

print("Expected: False")
print("Actual  :", validator.validate(deck))


print()
print("=" * 60)
print("TEST 3 - Gouging Fire ex + Fire Energy")
print("=" * 60)

gouging_fire = get_card_id(db, "Gouging Fire ex")

deck = build_deck(
    [gouging_fire] * 15,
    [fire_energy] * 15
)

print("Expected: True")
print("Actual  :", validator.validate(deck))


print()
print("=" * 60)
print("TEST 4 - Raging Bolt + Lightning/Fighting")
print("=" * 60)

raging_bolt = get_card_id(db, "Raging Bolt")

lightning = db.get_basic_energy_id("Lightning")
fighting = db.get_basic_energy_id("Fighting")

energy = [lightning] * 8 + [fighting] * 7

deck = build_deck(
    [raging_bolt] * 15,
    energy
)

print("Expected: True")
print("Actual  :", validator.validate(deck))


print()
print("=" * 60)
print("TEST 5 - Raging Bolt + Lightning Only")
print("=" * 60)

energy = [lightning] * 15

deck = build_deck(
    [raging_bolt] * 15,
    energy
)

print("Expected: False")
print("Actual  :", validator.validate(deck))
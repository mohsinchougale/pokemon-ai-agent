from database.card_database import CardDatabase

card_db = CardDatabase("data/cards.csv")   # <-- adjust path if your CSV is elsewhere

pokemon_found = 0

for card_id in card_db.cards.index:

    if card_db.is_pokemon(card_id):

        print("=" * 60)
        print("Card ID:", card_id)
        print("Name:", card_db.get_name(card_id))
        print("Type:", card_db.get_type(card_id))
        print("Weakness:", card_db.get_weakness(card_id))
        print("Resistance:", card_db.get_resistance(card_id))
        print("Retreat Cost:", card_db.get_retreat_cost(card_id))

        pokemon_found += 1

        if pokemon_found == 5:
            break
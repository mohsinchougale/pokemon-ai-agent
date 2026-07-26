from deckbuilding.deck import Deck
from deckbuilding.energy.selector import EnergySelector
from deckbuilding.deck_validator import DeckValidator


class DeckGenerator:
    """
    Combines Pokémon, Trainer, and Energy selections
    into a complete 60-card deck.
    """


    def __init__(
        self,
        pokemon_strategy,
        trainer_selector,
        energy_selector,
        validator
    ):

        self.pokemon_strategy = pokemon_strategy

        self.trainer_selector = trainer_selector

        self.energy_selector = energy_selector

        self.validator = validator



    def generate(
        self,
        pokemon_count=15,
        trainer_count=30,
        energy_count=15,
        max_attempts=10
    ):


        for attempt in range(max_attempts):

            cards = []


            pokemon_cards = (
                self.pokemon_strategy
                .select_pokemon(
                    pokemon_count
                )
            )


            trainer_cards = (
                self.trainer_selector
                .select_trainers(
                    trainer_count
                )
            )


            energy_cards = (
                self.energy_selector
                .select_energy(
                    pokemon_cards,
                    energy_count
                )
            )


            cards.extend(pokemon_cards)
            cards.extend(trainer_cards)
            cards.extend(energy_cards)


            deck = Deck(cards)


            if self.validator.validate(deck):

                return deck


            print(
                f"Invalid deck generated. Retry {attempt+1}/{max_attempts}"
            )


        raise RuntimeError(
            "Could not generate a valid deck"
        )
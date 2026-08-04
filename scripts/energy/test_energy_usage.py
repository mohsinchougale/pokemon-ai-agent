import inspect

from deckbuilding.deck_generator import DeckGenerator
from deckbuilding.archetypes.aggressive_ex import AggressiveEXArchetype
from deckbuilding.archetypes.evolution_heavy import EvolutionHeavyArchetype
from deckbuilding.archetypes.balanced import BalancedArchetype


def show_usage(obj, name):

    print("\n==============================")
    print(name)
    print("==============================\n")

    source = inspect.getsource(obj)

    for i, line in enumerate(source.splitlines(), 1):

        if (
            "EnergySelector" in line
            or "select_energy" in line
            or "energy" in line.lower()
        ):
            start = max(0, i-3)
            end = min(
                len(source.splitlines()),
                i+8
            )

            print(
                "\n".join(
                    source.splitlines()[start:end]
                )
            )

            print("----------------")


def main():

    show_usage(
        DeckGenerator,
        "DeckGenerator"
    )


    show_usage(
        AggressiveEXArchetype,
        "AggressiveEXArchetype"
    )


    show_usage(
        EvolutionHeavyArchetype,
        "EvolutionHeavyArchetype"
    )


    show_usage(
        BalancedArchetype,
        "BalancedArchetype"
    )



if __name__ == "__main__":
    main()
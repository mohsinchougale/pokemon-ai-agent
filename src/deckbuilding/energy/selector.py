from collections import Counter
import re


class EnergySelector:
    """
    Selects basic energy cards based on Pokémon attack requirements.
    """


    ENERGY_SYMBOLS = {

        "G": "Grass",
        "R": "Fire",
        "W": "Water",
        "L": "Lightning",
        "P": "Psychic",
        "F": "Fighting",
        "D": "Darkness",
        "M": "Metal"

    }


    def __init__(self, card_database):

        self.db = card_database



    def select_energy(
        self,
        pokemon_cards,
        count=15
    ):

        requirements = Counter()


        for card_id in pokemon_cards:

            attacks = self.db.get_attacks(card_id)


            for attack in attacks:

                cost = attack.get("cost")


                for energy in self._parse_cost(cost):

                    requirements[energy] += 1



        if not requirements:

            return self._default_energy(
                count
            )


        return self._allocate_energy(
            requirements,
            count
        )



    def _parse_cost(self, cost):

        if cost is None:
            return []


        cost = str(cost)


        if cost.lower() == "no cost":
            return []


        symbols = re.findall(
            r"\{(.*?)\}",
            cost
        )


        energies = []


        for symbol in symbols:

            if symbol in self.ENERGY_SYMBOLS:

                energies.append(
                    self.ENERGY_SYMBOLS[symbol]
                )


        return energies



    def _allocate_energy(
        self,
        requirements,
        count
    ):

        allocations = {}

        total = sum(
            requirements.values()
        )


        # Initial allocation
        for energy, value in requirements.items():

            exact = (
                value / total * count
            )

            allocations[energy] = {
                "base": int(exact),
                "remainder": exact - int(exact)
            }


        selected = []


        # Add guaranteed copies
        for energy, data in allocations.items():

            selected.extend(
                [energy] * data["base"]
            )


        remaining = (
            count - len(selected)
        )


        # Give leftovers to highest fractional remainder
        if remaining > 0:

            priority = sorted(
                allocations.items(),
                key=lambda x: x[1]["remainder"],
                reverse=True
            )


            index = 0

            while remaining > 0:

                energy = priority[index][0]

                selected.append(
                    energy
                )

                remaining -= 1

                index += 1


                if index == len(priority):
                    index = 0



        return [
            self.db.get_basic_energy_id(
                energy
            )
            for energy in selected
        ]



    def _default_energy(self, count):

        # Fire as fallback
        return [
            self.db.get_basic_energy_id(
                "Fire"
            )
        ] * count
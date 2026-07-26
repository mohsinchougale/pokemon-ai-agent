from collections import Counter


class EnergySelector:
    """
    Selects basic energy cards based on Pokémon attack requirements.
    """


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

                cost = attack["cost"]

                if cost is None:
                    continue


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

        mapping = {

            "G": "Grass",
            "R": "Fire",
            "W": "Water",
            "L": "Lightning",
            "P": "Psychic",
            "F": "Fighting",
            "D": "Darkness",
            "M": "Metal",
            "C": "Colorless"

        }


        energies = []


        for symbol in str(cost):

            if symbol in mapping:

                energies.append(
                    mapping[symbol]
                )


        return energies



    def _allocate_energy(
        self,
        requirements,
        count
    ):

        selected = []


        total = sum(
            requirements.values()
        )


        for energy, value in requirements.items():

            copies = round(
                value / total * count
            )


            selected.extend(
                [
                    energy
                ] * copies
            )


        while len(selected) < count:

            selected.append(
                requirements.most_common(1)[0][0]
            )


        selected = selected[:count]


        return [
            self.db.get_basic_energy_id(
                energy
            )
            for energy in selected
        ]



    def _default_energy(self, count):

        return [
            1
        ] * count
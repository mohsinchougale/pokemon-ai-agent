from collections import defaultdict

from cards.evolution_lines import EvolutionLine


class EvolutionLineBuilder:


    def __init__(self, card_database, extractor):

        self.db = card_database
        self.extractor = extractor



    def build(self, pokemon_ids):

        features = [
            self.extractor.extract(card_id)
            for card_id in pokemon_ids
        ]


        pokemon_by_name = {
            f.name.lower(): f
            for f in features
        }


        lines = []


        for pokemon in features:


            # We only start from Basic Pokémon
            if pokemon.stage != "Basic Pokémon":
                continue


            basic = pokemon


            stage1 = None
            stage2 = None


            # Find evolution of this basic
            for candidate in features:

                if (
                    candidate.previous_stage.lower()
                    ==
                    basic.name.lower()
                ):

                    if candidate.stage == "Stage 1 Pokémon":

                        stage1 = candidate


                        # Find Stage 2
                        for final in features:

                            if (
                                final.previous_stage.lower()
                                ==
                                stage1.name.lower()
                            ):

                                stage2 = final



            if stage1 or stage2:

                lines.append(

                    EvolutionLine(

                        basic=basic.name,

                        stage1=(
                            stage1.name
                            if stage1
                            else None
                        ),

                        stage2=(
                            stage2.name
                            if stage2
                            else None
                        ),

                        cards=[
                            basic.card_id,
                            *(

                                [stage1.card_id]
                                if stage1
                                else []

                            ),
                            *(

                                [stage2.card_id]
                                if stage2
                                else []

                            )
                        ]
                    )

                )


        return lines
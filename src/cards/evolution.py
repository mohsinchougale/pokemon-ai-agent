from collections import defaultdict


class EvolutionAnalyzer:

    def analyze(self, pokemon_features):

        names = {
            f.name.lower()
            for f in pokemon_features
        }


        result = {

            "evolution_lines": 0,
            "supported_stage1": 0,
            "supported_stage2": 0,
            "orphan_evolutions": 0,
            "orphan_stage1": 0,
            "orphan_stage2": 0,
            "evolution_score": 0

        }


        for pokemon in pokemon_features:

            previous = pokemon.previous_stage.lower()


            if not previous:
                continue


            if previous in names:

                if pokemon.stage == "Stage 1 Pokémon":
                    result["supported_stage1"] += 1
                    result["evolution_lines"] += 1


                elif pokemon.stage == "Stage 2 Pokémon":
                    result["supported_stage2"] += 1
                    result["evolution_lines"] += 1


            else:

                result["orphan_evolutions"] += 1

                if pokemon.stage == "Stage 1 Pokémon":
                    result["orphan_stage1"] += 1

                elif pokemon.stage == "Stage 2 Pokémon":
                    result["orphan_stage2"] += 1



        result["evolution_score"] = (
            result["supported_stage1"] * 3
            +
            result["supported_stage2"] * 6
            -
            result["orphan_stage1"] * 2
            -
            result["orphan_stage2"] * 5
        )


        return result
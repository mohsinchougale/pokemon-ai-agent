from collections import Counter


class DeckEvaluator:

    def __init__(self,card_feature_extractor,evolution_analyzer):
        self.extractor = card_feature_extractor
        self.evolution_analyzer = evolution_analyzer

    def evaluate(self, deck):

        features = [
            self.extractor.extract(card_id)
            for card_id in deck
        ]


        pokemon_features = [
            f for f in features
            if f.is_pokemon
        ]


        evolution_stats = self.evolution_analyzer.analyze(
            pokemon_features
        )

        pokemon = [
            f for f in features
            if f.is_pokemon
        ]

        energy = [
            f for f in features
            if f.is_energy
        ]

        trainers = [
            f for f in features
            if f.is_trainer
        ]


        result = {

            "total_cards": len(deck),

            "pokemon_count": len(pokemon),
            "energy_count": len(energy),
            "trainer_count": len(trainers),
            

            "basic_pokemon": sum(
                self.extractor.db.is_basic_pokemon(f.card_id)
                for f in pokemon
            ),

            "stage1_pokemon": sum(
                self.extractor.db.is_stage1_pokemon(f.card_id)
                for f in pokemon
            ),

            "stage2_pokemon": sum(
                self.extractor.db.is_stage2_pokemon(f.card_id)
                for f in pokemon
            ),

            "ex_count": sum(
                f.is_ex
                for f in pokemon
            ),

            "average_hp": self.average(
                [f.hp for f in pokemon]
            ),

            "average_damage": self.average(
                [f.max_damage for f in pokemon]
            ),
            "pokemon_quality": self.pokemon_quality(
                pokemon
            ),
            **evolution_stats
        }


        result["deck_score"] = self.score(result)


        return result

    def pokemon_quality(self, pokemon):

        if not pokemon:
            return 0


        score = 0


        avg_hp = self.average(
            [p.hp for p in pokemon]
        )


        avg_damage = self.average(
            [p.max_damage for p in pokemon]
        )


        ex_count = sum(
            p.is_ex
            for p in pokemon
        )


        # Survivability
        if avg_hp >= 200:
            score += 10

        elif avg_hp >= 150:
            score += 5


        # Damage output
        if avg_damage >= 150:
            score += 10

        elif avg_damage >= 100:
            score += 5


        # Powerful Pokémon bonus
        score += min(
            ex_count * 3,
            15
        )


        return score

    def average(self, values):

        values = [
            v for v in values
            if v > 0
        ]

        if not values:
            return 0

        return round(
            sum(values) / len(values),
            2
        )



    def score(self, stats):

        score = 0


        # Healthy Pokemon count
        score += min(
            stats["pokemon_count"] * 2,
            40
        )

        score += stats["pokemon_quality"]


        # Energy balance
        if 10 <= stats["energy_count"] <= 15:
            score += 20


        # Trainer support
        if stats["trainer_count"] >= 20:
            score += 20


        # Strong attackers
        if stats["average_damage"] >= 150:
            score += 10

        # Evolution consistency
        score += stats["evolution_score"]

        return score
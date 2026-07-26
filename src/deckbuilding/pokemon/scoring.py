class EvolutionScorer:


    def score(self, line, extractor):

        score = 0


        # Prefer complete evolution chains
        if line.stage2:
            score += 20

        elif line.stage1:
            score += 10


        # Check final evolution strength
        final_id = line.cards[-1]

        feature = extractor.extract(final_id)


        score += feature.max_damage / 10

        score += feature.hp / 50


        if feature.is_ex:
            score += 15


        return score
from deckbuilding.trainers.features import TrainerFeatureExtractor


class TrainerPool:


    def __init__(self, card_database):

        self.db = card_database

        self.extractor = TrainerFeatureExtractor(
            card_database
        )


        self.all_trainers = []

        self._build()



    def _build(self):

        for card_id in self.db.cards.index:

            stage = self.db.get_stage(card_id)


            if stage not in [
                "Item",
                "Supporter",
                "Stadium",
                "Pokémon Tool"
            ]:
                continue


            feature = self.extractor.extract(
                card_id
            )


            self.all_trainers.append(
                feature
            )
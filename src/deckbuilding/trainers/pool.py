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

            feature = self.extractor.extract(
                card_id
            )


            if feature is None:
                continue


            self.all_trainers.append(
                feature
            )
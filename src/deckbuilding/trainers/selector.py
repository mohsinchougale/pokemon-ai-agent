import random


class TrainerSelector:


    def __init__(self, trainer_pool):

        self.pool = trainer_pool



    def select_trainers(self, count=30):

        selected = []


        # Consistency first
        priority = sorted(

            self.pool.all_trainers,

            key=lambda x:

                (
                    x.is_draw
                    + x.is_search
                    + x.is_recovery
                ),

            reverse=True
        )


        selected.extend(
            [
                x.card_id
                for x in priority[:20]
            ]
        )


        remaining = count - len(selected)


        if remaining > 0:

            remaining_cards = [

                x.card_id

                for x in self.pool.all_trainers

                if x.card_id not in selected

            ]


            selected.extend(

                random.sample(

                    remaining_cards,

                    min(
                        remaining,
                        len(remaining_cards)
                    )
                )
            )


        return selected
import random


class TrainerSelector:


    def __init__(self, trainer_pool):

        self.pool = trainer_pool



    def select_trainers(self, count=30):
        selected = []


        # -----------------------------
        # Separate ACE SPEC and normal trainers
        # -----------------------------

        ace_specs = [
            x for x in self.pool.all_trainers
            if x.is_ace_spec
        ]


        normal_trainers = [
            x for x in self.pool.all_trainers
            if not x.is_ace_spec
        ]


        # -----------------------------
        # Pick exactly ONE ACE SPEC
        # -----------------------------

        if ace_specs:

            ace = random.choice(ace_specs)

            selected.append(
                ace.card_id
            )


        # -----------------------------
        # Rank normal trainers
        # -----------------------------

        priority = sorted(

            normal_trainers,

            key=lambda x:
                (
                    int(x.is_draw)
                    + int(x.is_search)
                    + int(x.is_recovery)
                    + int(x.is_switch)
                ),

            reverse=True
        )


        # Need remaining trainer slots
        remaining = count - len(selected)


        # Take highest priority cards
        selected.extend(
            [
                x.card_id
                for x in priority[:remaining]
            ]
        )


        # -----------------------------
        # Random fill if needed
        # -----------------------------

        if len(selected) < count:


            candidates = [

                x.card_id
                for x in normal_trainers
                if x.card_id not in selected

            ]


            selected.extend(

                random.sample(

                    candidates,

                    count - len(selected)

                )

            )


        return selected
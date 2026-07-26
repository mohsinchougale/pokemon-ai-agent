from dataclasses import dataclass


@dataclass
class TrainerFeatures:

    card_id: int
    name: str

    category: str
    effect: str
    rule: str

    # Strategic tags
    is_draw: bool
    is_search: bool
    is_switch: bool
    is_recovery: bool
    is_disruption: bool
    is_energy_acceleration: bool



class TrainerFeatureExtractor:


    def __init__(self, card_database):

        self.db = card_database



    def extract(self, card_id):

        name = str(
            self.db.get_name(card_id)
        )

        category = str(
            self.db.get_category(card_id)
        )

        card = self.db.get_card(card_id)


        effect = ""

        if card is not None:

            if "Effect Explanation" in card:

                effect = str(
                    card["Effect Explanation"]
                )


        rule = str(
            self.db.get_rule(card_id)
        )


        text = (
            name
            + " "
            + effect
            + " "
            + rule
        ).lower()



        return TrainerFeatures(

            card_id=card_id,

            name=name,

            category=category,

            effect=effect,

            rule=rule,


            is_draw=self._contains(
                text,
                [
                    "draw",
                    "cards"
                ]
            ),


            is_search=self._contains(
                text,
                [
                    "search",
                    "look at your deck",
                    "put onto your bench"
                ]
            ),


            is_switch=self._contains(
                text,
                [
                    "switch",
                    "retreat"
                ]
            ),


            is_recovery=self._contains(
                text,
                [
                    "discard pile",
                    "put back",
                    "recover"
                ]
            ),


            is_disruption=self._contains(
                text,
                [
                    "opponent",
                    "discard",
                    "shuffle"
                ]
            ),


            is_energy_acceleration=self._contains(
                text,
                [
                    "attach energy",
                    "accelerate",
                    "energy from your deck"
                ]
            )
        )



    def _contains(self, text, keywords):

        for word in keywords:

            if word in text:
                return True

        return False
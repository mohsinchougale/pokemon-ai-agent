from dataclasses import dataclass


@dataclass
class EvolutionLine:

    basic: str

    stage1: str | None

    stage2: str | None

    cards: list

    def length(self):

        count = 1

        if self.stage1:
            count += 1

        if self.stage2:
            count += 1

        return count
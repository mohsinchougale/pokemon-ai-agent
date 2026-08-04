from pathlib import Path


class DeckExporter:
    """
    Handles exporting generated decks into Kaggle submission format.

    Kaggle format:
    - one card ID per line
    - no header
    - no counts
    """

    @staticmethod
    def export(deck, path):
        """
        Export Deck object to CSV.

        Args:
            deck: Deck instance
            path: output file path
        """

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(path, "w") as f:

            for card_id in deck.cards:

                f.write(
                    f"{card_id}\n"
                )


    @staticmethod
    def load(path):
        """
        Load Kaggle formatted deck.csv.

        Returns:
            list[int]
        """

        with open(path, "r") as f:

            cards = [
                int(line.strip())
                for line in f
                if line.strip()
            ]

        return cards
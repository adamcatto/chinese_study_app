import json
import random
from pathlib import Path

class SpacedRepetition:
    def __init__(self, data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            self.cards = json.load(f)
        for card in self.cards:
            card["interval"] = 1
            card["next_review"] = 0
            card["repetitions"] = 0
            card["ease_factor"] = 2.5

    def get_due_cards(self, day):
        return [card for card in self.cards if card["next_review"] <= day]

    def update_card(self, card, quality, day):
        if quality >= 3:
            if card["repetitions"] == 0:
                card["interval"] = 1
            elif card["repetitions"] == 1:
                card["interval"] = 6
            else:
                card["interval"] *= card["ease_factor"]
            card["repetitions"] += 1
        else:
            card["repetitions"] = 0
            card["interval"] = 1

        card["ease_factor"] = max(1.3, card["ease_factor"] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        card["next_review"] = day + int(card["interval"])

    def save_progress(self, data_path):
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(self.cards, f, ensure_ascii=False, indent=4)

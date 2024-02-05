import numpy as np
from queue import Queue

import clash_royale.envs.game_engine.cards as cr


class Hand():
    def __init__(self, deck: list[type[cr.Card]]):
        self.deck = Queue(maxsize=8)
        for card in deck:
            self.deck.put(card, block=False)
        
        self.available = [self.deck.get(block=False) for i in range(4)]
        self.next = self.deck.get(block=False)

    def query(self, index: int):
        if index < 4:
            return self.available[index]
        else:
            return self.next
        
    def pop(self, index: int):
        self.deck.put(self.available[index], block=False)
        self.available[index] = self.next
        self.next = self.deck.get(block=False)

        

class Player():
    def __init__(self, deck: list[str]):
        self.elixir = 5

        deck = [cr.name_to_card[card_name] for card_name in deck]
        np.random.shuffle(deck)
        self.hand = Hand(deck)

class GameEngine():
    # note: muzero should never require a game to be copied
    def __init__(self, 
                 deck1: list[str] = ['barbarian' * 8], 
                 deck2: list[str] = ['barbarian' * 8], 
                 seed: int=0):
        np.random.seed(seed)

        self.images = []
        self.actions = []
        self.current_frame = 0

        self.player_1 = Player(deck1)
        self.player_2 = Player(deck2)
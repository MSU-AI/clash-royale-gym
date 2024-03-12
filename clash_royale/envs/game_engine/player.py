from typing import List

from queue import Queue
import random

from clash_royale.envs.game_engine.card import Card

class Player():
    """
    Player class

    This class represents the current state of players' cards, and the logic of playing cards.
    Handle elixir and legal cards.
    """

    def __init__(self,
                 deck: List[Card],
                 fps: int) -> None:
        """
        Player component is initialized with deck of string, 
        specifying the cards' names in the deck.
        """

        self.elixir: int = 0
        self.fps: int = fps

        random.shuffle(deck)
        self.deck: Queue = Queue(maxsize = 8)
        for card in deck:
            self.deck.put(card, block = False)

        self.hand: list[Card] = [self.deck.get(block = False) for i in range(4)]
        self.next: Card = self.deck.get(block = False)

    def reset(self, elixir: int = 5) -> None:
        """
        This method is used to reset Player class.
        TODO: implement deck shuffling
        """

        self.elixir: int = elixir

    def get_pseudo_legal_cards(self) -> List[Card]:
        """
        This method is used to get all cards that can be 
        played given the current amount of elixir.
        """

        legal_cards: list[Card] = []
        for card in self.hand:
            if card.elixir <= self.elixir:
                legal_cards.append(card)

        return legal_cards

    def step(self, 
             elixir_rate: float,
             frames: int=1) -> None:
        """
        Called with the value of elixir_rate and frame to update the elixir of player after 'frame' number of frames
        to better customize the elixir_rate that can vary depends on game modes.
        """

        self.elixir += (elixir_rate / self.fps) * frames

    def pop(self, card_index: int) -> None:

        """
        
        A helper function to discard a card in hand and put it into Queue of remaining cards
        that are not able to be played at the current state.

        """

        assert(card_index < 4)
        self.deck.put(self.hand[card_index], block = False)
        self.hand[card_index] = self.next
        self.next: Card = self.deck.get(block = False)


    def play_card(self, card_index: int) -> None:

        """
        
        Called with the index of cards in hand to update the state of available cards, next cards, and elixir.
        Should be called with the initial rendering of entity.

        """

        assert(card_index < 4)
        elixir_cost: float = self.hand[card_index].elixir_cost
        assert(elixir_cost <= self.elixir)
        self.pop(card_index)
        self.elixir -= elixir_cost

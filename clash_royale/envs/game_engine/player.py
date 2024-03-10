from queue import Queue
from clash_royale.envs.game_engine.card import Card
import random

class Player():
    """
    Player class

    This class represents the current state of players' cards, and the logic of playing cards.
    Handle elixir and legal cards.

    """
    def __init__(self,
                 deck: list[type[Card]]) -> None:
        
        """
        
        Player component is initialized with deck of string, specifiying the cards' names in the deck.

        """

        self.elixir: int = 5

        random.shuffle(deck)
        self.deck: Queue = Queue(maxsize = 8)
        for card in deck:
            self.deck.put(card, block = False)
        
        self.hand: list[type[Card]] = [self.deck.get(block = False) for i in range(4)]
        self.next: Card = self.get(block = False)

    def reset(self, elixir: int = 5) -> None:

        """
        
        This method is used to delete information of Player class in previous matches.

        """

        self.elixir: int = elixir

        """

        One way of reseting the player class with the same deck and without calling __init__ again when a new match starts.

        for card in self.hand:
            self.hand.put(card, block = False)
        self.hand.put(self.next, block = False)
        random.shuffle(self.deck)

        self.hand: list[type[Card]] = [self.deck.get(block = False) for i in range(4)]
        self.next: Card = self.get(block = False)

        """

        """

        Reseting all variables to None to reduce the unexpected side effects

        """

        self.deck: None = None
        self.hand: None = None
        self.next: None = None

    def get_pseudo_legal_cards(self, current_elixir: float) -> list[type[Card]]:
        
        """
        
        This method is used to get all cards that can be played given the current amount of elixir.

        """

        legal_cards: list[type[Card]] = []
        for card in self.hand:
            if card.elixir <= self.elixir:
                legal_cards.append(card)
        return legal_cards
    
    def step(self, 
             elixir_rate: float, 
             fps: int, 
             frame: int) -> None:

        """
        
        Called with the value of elixir_rate and frame to update the elixir of player after 'frame' number of frames
        to better customize the elixir_rate that can vary depends on game modes.

        """

        self.elixir += (elixir_rate / fps) * frame
    
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
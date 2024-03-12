class Card():
    '''
    pseudo Card class.

    This class is created for Player class to refer to statistics of cards.
    '''

    def __init__(self, elixir: int, elixir_cost: int) -> None:
        self.elixir: int = elixir
        self.elixir_cost: int = elixir_cost
        pass

# Author: Amar Jilani
# GitHub username: amarjilani
# Date: 2022-05-30
# Description: This program is a Monopoly inspired game called the RealEstateGame. It has classes for
#              the Player, the Property and the game itself, RealEstateGame. These classes work together to
#              simulate a game of Monopoly.

class Player:
    """
    This class represents a Player of the RealEstateGame. A Player possesses a name, position and balance. This allows
    for interaction with the RealEstateGame board. It is used by a RealEstateGame to allow for movement and purchases.
    """

    def __init__(self, name, balance):
        """
        Creates a Player
        :param name: name of player
        :param balance: starting balance of player
        """
        self._name = name
        self._balance = balance
        self._position = 0
        self._rect = None
        self._img = None

    def get_name(self):
        """
        Returns name of player
        :return: name of player
        """
        return self._name

    def get_balance(self):
        """
        Returns player's current balance
        :return: balance of player
        """
        return self._balance

    def get_position(self):
        """
        Returns player's current position
        :return: position of player
        """
        return self._position

    def set_position(self, position):
        """
        Sets the players position
        :param position: new position for player
        """
        self._position = position

    def change_balance(self, amount):
        """
        Adjusts the players balance, positive amount increases, negative amount decreases
        :param amount: amount to adjust
        """
        self._balance += amount

    def set_rect(self, rect):
        self._rect = rect

    def get_rect(self):
        return self._rect

    def get_image(self):
        return self._img

    def set_image(self, image):
        self._img = image

class Property:
    """
    This class represents a Property or space on the board of a RealEstateGame. It contains a certain rent price,
    purchasing price, owner and name. This class is used by the RealEstateGame class to allow for purchasing and
    rental transactions.
    """

    def __init__(self, name, rent_amount):
        """
        Creates a Property
        :param name: name of Property
        :param rent_amount: rent price
        """
        self._rent = rent_amount
        self._price = rent_amount*5
        self._owner = None
        self._name = name

    def get_name(self):
        """
        Returns name of property
        :return: name of property
        """
        return self._name

    def get_owner(self):
        """
        Return Player object that is the current owner of this space
        :return: Player object
        """
        return self._owner

    def set_owner(self, player):
        """
        Set the owner of this space
        :param player: name of player that owns
        """
        self._owner = player

    def get_price(self):
        """
        Return price to purchase this space
        :return: price (rent * 5)
        """
        return self._price

    def get_rent(self):
        """
        Return the cost of rent
        :return: rent 
        """
        return self._rent


class RealEstateGame:
    """
    Class representing an instance of the RealEstateGame. Allows for interaction between Players, who possess a certain
    amount of balance, with the board, consisting of instances of the Property class.
    Therefore, this class directly interacts with both the Player class and the Property class and allows a framework on
    which these two classes can interact. It allows for movement of Players on the board, purchasing of Properties and
    the collection and payment of rent.
    """

    def __init__(self):
        """
        Creates instance of RealEstateGame
        """
        self._spaces = []
        self._players = {}  # {name: player object}

    def create_spaces(self, go_amount, rent_amounts):
        """
        Creates the board using the given rent amounts.
        Uses Property class to create new property for each space.
        The first space is the "GO" space.
        :param go_amount: money obtained when player passes "GO"
        :param rent_amounts: amount of rent for each square
        :return: creates array representing game board with GO space
        """
        # creates the first space, which is the GO space
        self._spaces.append(Property("GO", go_amount))

        # creates property spaces
        count = 1
        for rent in rent_amounts:
            prop_name = "property_" + str(count)
            self._spaces.append(Property(prop_name, rent))
            count += 1


    def create_player(self, name, balance):
        """
        Creates a player.
        Uses the Player class to create a new Player and add them to the list of players.
        :param name: name of player
        :param balance: starting balance
        """
        new = Player(name, balance)
        self._players[name] = new
        return new

    def get_player_account_balance(self, name):
        """
        Gets the current balance of a player.
        Uses the Player class method get_balance()
        :param name: name of player
        :return: current balance
        """
        if name in self._players:
            player = self._players[name]
            return player.get_balance()
        else:
            print("This player does not exist: " + name)
            return

    def get_player_current_position(self, name):
        """
        Gets the current position of player.
        Uses the Player class method get_position().
        :param name: name of player
        :return: current position of player
        """
        # make sure that the player exists
        if name in self._players:
            player = self._players[name]
            return player.get_position()
        else:
            print("This player does not exist: " + name)
            return

    def buy_space(self, name):
        """
        Buys current space on which a player is positioned.
        Uses the Player class method get_position(), get_balance() and change_balance().
        Uses the Property class method get_price(), get_owner() and set_owner().
        If the space is already owned, the player does not have sufficient funds or the space is "GO",
        then the transaction does not go through and returns False.
        Otherwise, the player is able to purchase the space.
        :param name: name of player
        :return boolean of whether transaction was successful
        """
        # make sure that player exists
        if name in self._players:
            player = self._players[name]
            space = self._spaces[player.get_position()]
            cost = space.get_price()

            # GO space cannot be purchased
            if space.get_name == "GO":
                print("You cannot buy the GO space!")
                return False

            # the player cannot make the purchase if they do not have enough money
            elif cost >= player.get_balance():
                print("You do not have sufficient funds for this purchase!")
                return False

            # if the space already has an owner, then you cannot buy it
            elif space.get_owner() is not None:
                print("This space has already been purchased!")
                return False

            # otherwise, set the player as the owner and subtract the cost from their balance
            else:
                space.set_owner(player)
                player.change_balance(-cost)
                return True

        # if the player does not exist, return
        else:
            print("This player does not exist: " + name)
            return

    def move_player(self, name, number):
        """
        Moves the player the given amount of space.
        Uses methods from both the Player class and the Property class.
        Makes sure that the player is still in the game ( >0 balance).
        Ensures that the player loops around back to the beginning if they go past the last space.
        Ensures that the player pays the rent of any purchased space they land on.
        If player balance is 0 after a move, ensures that player no longer owns any spaces.
        :param name: name of player
        :param number: amount of spaces to move
        """
        # make sure that player exists
        if name in self._players:
            player = self._players[name]
            current = player.get_position()

            # if the player is out of the game, return without doing anything
            if player.get_balance() == 0:
                return

            # if the move will take the player off the edge of the board, loop back to beginning
            elif current + number > len(self._spaces) - 1:
                new_pos = number - (len(self._spaces) - current)
                player.set_position(new_pos)
                go = self._spaces[0]
                player.change_balance(go.get_rent())    # adds the GO amount to the players balance

                # make rent payments if the property has an owner
                space = self._spaces[new_pos]
                if space.get_owner() is not None and space.get_owner() != player:
                    rent = space.get_rent()
                    owner = space.get_owner()

                    # if the player has enough money to pay the rent, add rent amount to owner and subtract from player
                    if player.get_balance() > rent:
                        player.change_balance(-rent)
                        owner.change_balance(rent)
                        return

                    # if the player doesn't have enough, give the owner whatever remaining balance the player has
                    # since the player is now out of the game, reset all properties that are owned by that player
                    else:
                        owner.change_balance(player.get_balance())
                        player.change_balance(player.get_balance())
                        for space in self._spaces:
                            if space.get_owner() == player:
                                space.set_owner(None)

            # for normal movements throughout the board (no looping back to start)
            else:
                new_pos = current + number
                player.set_position(new_pos)
                space = self._spaces[new_pos]

                # make rent payments to the owner of the property
                if space.get_owner() is not None and space.get_owner() != player:
                    rent = space.get_rent()
                    owner = space.get_owner()

                    # if the player has enough money to pay the rent, subtract the rent from player and add to owner
                    if player.get_balance() > rent:
                        player.change_balance(-rent)
                        owner.change_balance(rent)
                        return

                    # if the player doesn't have enough money, give owner whatever is remaining
                    # the player is out of the game, so all properties that were owned by them are reset
                    else:
                        owner.change_balance(player.get_balance())
                        player.change_balance(-player.get_balance())

                        # loop through the spaces and if they are owned by the player, reset to None
                        for space in self._spaces:
                            if space.get_owner() == player:
                                space.set_owner(None)
        else:
            print("This player does not exist: " + name)
            return False

    def check_game_over(self):
        """
        Checks if all players except one have a balance of 0
        Uses the get_balance() method from the Player class.
        :return: winning players name if game is over, else empty string
        """
        non_zero = []  # initialize list of players that have a positive balance

        # loop through players, and if they have a balance > 0, add them to the list
        for player in self._players:
            player_obj = self._players[player]
            if player_obj.get_balance() == 0:
                continue
            else:
                non_zero.append(player)

        # if there is only one player in the list, the game is over, return name of winner
        if len(non_zero) == 1:
            return non_zero[0]

        # if the game is not over, return empty string
        else:
            return ""


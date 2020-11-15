import random
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.factory import Factory

# global initializations
suits = ('H', 'D', 'S', 'C')
ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
imagePath = "Images/"


# Supporting classes and methods used in game play for initializing things
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # returning cards in the file formats of images
        return str(self.rank) + self.suit + ".png"


class Deck:
    def __init__(self):
        # creating an empty deck
        self.deck = []
        for suit in suits:
            for rank in ranks:
                # Adding all 52 cards in deck by combining suits and ranks
                self.deck.append(Card(suit, rank))

    # extra method to test whats in our deck
    def __str__(self):
        deckComposition = ''
        for card in self.deck:
            deckComposition += '\n ' + card.__str__()
        return 'The deck has:' + deckComposition

    # method for shuffling deck
    def shuffle(self):
        random.shuffle(self.deck)

    # selecting a card from shuffled deck
    def deal(self):
        singleCard = self.deck.pop()
        return singleCard


class Hand:
    def __init__(self):
        # starting with an empty list as we did in the Deck class
        self.cards = []
        # starting with zero value
        self.value = 0
        # adding an attribute to keep track of aces
        self.aces = 0

    def addCard(self, card):
        self.cards.append(card)
        self.value += values[str(card.rank)]
        if card.rank == 'A':
            self.aces += 1

    def adjustForAce(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return self.cards


class Coins:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win(self):
        self.total += self.bet

    def lose(self):
        self.total -= self.bet


# global coin's initialization
playerCoins = Coins()


# GUI
class WelcomeWindow(Screen):
    rulesTextInput = ObjectProperty(None)


class BetWindow(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(BetWindow, self).__init__(**kwargs)

        # function to redirect screen to new game window
        def betCrosscheck(instance):
            if self.betTextInput.text != '' and playerCoins.total >= int(self.betTextInput.text) > 0:
                # saving bet amount
                playerCoins.bet = int(self.betTextInput.text)

                # resetting game window
                # self.parent.clear_widgets()
                # self.parent.add_widget(Factory.BetWindow(name = "Bet"))
                self.parent.add_widget(Factory.GameWindow(name="Game"))

                self.parent.current = "Game"

            else:
                # self.parent.clear_widgets()
                # self.parent.add_widget(Factory.BetWindow(name = "Bet"))
                self.parent.add_widget(Factory.GameWindow(name="Game"))
                self.parent.current = "Bet"

        self.cols = 1

        self.add_widget(Image(source="Coins.png"))

        self.betLabel = Label(text="Enter the number of coins you wanna bet:\n(initially you have 100 coins.)",
                              font_size=35, color=(1, 1, 1, 1), outline_width=1, outline_color=(0, 0.5, 0.5, 1),
                              halign="center")

        self.add_widget(self.betLabel)

        self.betTextInput = TextInput(text="", font_size=40, multiline=False, halign="center")

        self.add_widget(self.betTextInput)

        self.betButton = Button(text="BET & CONTINUE", font_size=35, background_color=(0, 1, 1, 1), on_release=betCrosscheck)

        self.add_widget(self.betButton)


class PopupWindow(FloatLayout):
    popupLabel = ObjectProperty(None)


# new class to continue playing if player wants to play again and again
class NewBetWindow(GridLayout, Screen):

    def __init__(self, **kwargs):
        super(NewBetWindow, self).__init__(**kwargs)
        # function to redirect screen to new game window
        def betCrosscheck(instance):

            if playerCoins.total > int(self.betTextInput.text) > 0:
                # saving bet amount
                playerCoins.bet = int(self.betTextInput.text)

                # resetting game window
                self.parent.clear_widgets()
                self.parent.add_widget(Factory.GameWindow(name="Game"))

                self.parent.current = "Game"

            else:
                self.parent.current = "newBet"

        self.cols = 1

        self.add_widget(Image(source="Coins.png"))

        self.betLabel = Label(text="Enter the number of coins you wanna bet:", font_size=35, color=(1, 1, 1, 1),
                              outline_width=1, outline_color=(0, 0.5, 0.5, 1), halign="center")

        self.add_widget(self.betLabel)

        self.betTextInput = TextInput(text="", font_size=40, multiline=False, halign="center")

        self.add_widget(self.betTextInput)

        self.betButton = Button(text="BET & CONTINUE", font_size=35, background_color=(0, 1, 1, 1), on_release=betCrosscheck)

        self.add_widget(self.betButton)


class GameWindow(GridLayout, Screen):

    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2

        self.GameWindow1 = GridLayout()
        self.GameWindow1.cols = 1
        self.GameWindow1.rows = 3

        self.GameWindow1.add_widget(Label(text="COMPUTER DEALER", font_size=25, color=(1, 1, 1, 1), outline_width=1,
                                          outline_color=(0, 0.5, 0.5, 1), halign="center", valign="center"))

        self.GameWindow2 = GridLayout()
        self.GameWindow2.cols = 7
        self.GameWindow2.rows = 1

        self.GameWindow2.add_widget(Label(text=""))

        self.compCardImage1 = Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(self.compCardImage1)

        self.compCardImage2 = Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(self.compCardImage2)

        self.compCardImage3 = Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(self.compCardImage3)

        self.compCardImage4 = Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(self.compCardImage4)

        self.compCardImage5 = Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(self.compCardImage5)

        self.GameWindow2.add_widget(Label(text=""))

        self.GameWindow3 = GridLayout()
        self.GameWindow3.cols = 1
        self.GameWindow3.rows = 1

        self.GameWindow4 = GridLayout()
        self.GameWindow4.cols = 1
        self.GameWindow4.rows = 3

        self.GameWindow5 = GridLayout()
        self.GameWindow5.cols = 7
        self.GameWindow5.rows = 1

        self.GameWindow5.add_widget(Label(text=""))

        self.playerCardImage1 = Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(self.playerCardImage1)

        self.playerCardImage2 = Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(self.playerCardImage2)

        self.playerCardImage3 = Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(self.playerCardImage3)

        self.playerCardImage4 = Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(self.playerCardImage4)

        self.playerCardImage5 = Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(self.playerCardImage5)

        self.GameWindow5.add_widget(Label(text=""))

        self.GameWindow6 = GridLayout()
        self.GameWindow6.cols = 1
        self.GameWindow6.rows = 1

        self.GameWindow6.add_widget(Label(text="PLAYER", font_size=25, color=(1, 1, 1, 1), outline_width=1,
                                          outline_color=(0, 0.5, 0.5, 1), halign="center", valign="center"))

        self.GameWindow7 = GridLayout()
        self.GameWindow7.cols = 7
        self.GameWindow7.rows = 1

        self.GameWindow7.add_widget(Label(text=""))

        self.GameWindow7.add_widget(Label(text=""))

        self.hitButton = Button(text="HIT", font_size=25, background_color=(0, 1, 1, 1))

        self.GameWindow7.add_widget(self.hitButton)

        self.GameWindow7.add_widget(Label(text=""))

        self.stayButton = Button(text="STAY", font_size=25, background_color=(0, 1, 1, 1))

        self.GameWindow7.add_widget(self.stayButton)

        self.GameWindow7.add_widget(Label(text="TOTAL :", font_size=25, color=(1, 1, 1, 1), outline_width=1,
                                          outline_color=(0, 0.5, 0.5, 1), halign="center", valign="center"))

        self.PlayerTotalLabel = Label(text="0", font_size=25, color=(1, 1, 1, 1), outline_width=1,
                                      outline_color=(0, 0.5, 0.5, 1), halign="center", valign="center")

        self.GameWindow7.add_widget(self.PlayerTotalLabel)

        self.add_widget(self.GameWindow1)
        self.GameWindow1.add_widget(self.GameWindow2)
        self.GameWindow1.add_widget(self.GameWindow3)

        self.add_widget(self.GameWindow4)
        self.GameWindow4.add_widget(self.GameWindow5)
        self.GameWindow4.add_widget(self.GameWindow6)
        self.GameWindow4.add_widget(self.GameWindow7)

        # initialization
        deck = Deck()
        deck.shuffle()
        # playerCoins = Coins()

        playerHandList = []
        compHandList = []

        # creating starting status of the game
        playerHand = Hand()
        playerHand.addCard(deck.deal())
        playerHand.addCard(deck.deal())
        playerHand.adjustForAce()

        compHand = Hand()
        compHand.addCard(deck.deal())
        compHand.addCard(deck.deal())
        compHand.adjustForAce()

        # appending starting cards into respective lists
        for i in playerHand.cards:
            playerHandList.append(str(i))
        for i in compHand.cards:
            compHandList.append(str(i))

        # displaying starting cards in gui
        self.playerCardImage1.source = imagePath + playerHandList[0]
        self.playerCardImage2.source = imagePath + playerHandList[1]
        self.compCardImage1.source = imagePath + compHandList[0]

        # Displaying value of cards in gui
        self.PlayerTotalLabel.text = str(playerHand.value)

        # function for displaying result in pop up window
        def displayResult():

            # resetting bet screen
            self.parent.clear_widgets()
            # self.parent.add_widget(Factory.GameWindow(name = "Game"))
            self.parent.add_widget(Factory.NewBetWindow(name="newBet"))

            # changing screen for displaying game result
            self.parent.current = "newBet"

            pw = PopupWindow()

            playerHandList1 = ", ".join(playerHandList)
            compHandList1 = ", ".join(compHandList)

            #Experimental
            playerHandList1 = playerHandList1.replace(".png", "").replace("H", " of Hearts").\
                replace("D", " of Diamonds").replace("S", " of Spades").replace("C", " of Clubs").\
                replace("J", "Jack").replace("Q", "Queen").replace("K", "King").replace("A", "Ace")

            compHandList1 = compHandList1.replace(".png", "").replace("H", " of Hearts").\
                replace("D", " of Diamonds").replace("S", " of Spades").replace("C", " of Clubs").\
                replace("J", "Jack").replace("Q", "Queen").replace("K", "King").replace("A", "Ace")

            # setting the text of popup window label according to the game result
            if playerHand.value > 21:
                playerCoins.lose()

                pw.popupLabel.text = "PLAYER BUSTS!\nYour coins: {0}\n\nPlayer\'s hand value = {1}" \
                                     "\n{2}\n(Greater than 21!)\n\nComputer\'s hand value is = {3}" \
                                     "\n{4}".format(str(playerCoins.total),
                                                    str(playerHand.value),
                                                    playerHandList1,
                                                    str(compHand.value),
                                                    compHandList1)

            elif compHand.value > 21:
                playerCoins.win()

                pw.popupLabel.text = "COMPUTER BUSTS!\nYour coins: {0}\n\nPlayer\'s hand value = {1}" \
                                     "\n{2}\n\nComputer\'s hand value is = {3}" \
                                     "\n{4}\n(Greater than 21!)".format(str(playerCoins.total),
                                                                        str(playerHand.value),
                                                                        playerHandList1,
                                                                        str(compHand.value),
                                                                        compHandList1)

            elif compHand.value > playerHand.value:
                playerCoins.lose()

                pw.popupLabel.text = "COMPUTER WINS!\nYour coins: {0}\n\nPlayer\'s hand value = {1}" \
                                     "\n{2}\n\nComputer\'s hand value is = {3}" \
                                     "\n{4}\n(Greater than Player's Hand)".format(str(playerCoins.total),
                                                                                  str(playerHand.value),
                                                                                  playerHandList1,
                                                                                  str(compHand.value),
                                                                                  compHandList1)

            elif compHand.value < playerHand.value:
                playerCoins.win()

                pw.popupLabel.text = "PLAYER WINS!\nYour coins: {0}\n\nPlayer\'s hand value = {1}" \
                                     "\n{2}\n(Greater than Computer's Hand)\n\nComputer\'s hand value is = {3}" \
                                     "\n{4}".format(str(playerCoins.total),
                                                    str(playerHand.value),
                                                    playerHandList1,
                                                    str(compHand.value),
                                                    compHandList1)

            # setting the contents of popup window
            popupWindow = Popup(title="RESULT", content=pw, size_hint=(None, None), size=(500, 500))
            popupWindow.open()

        # function for asking for another card if player clicks HIT button
        def hitFunction(instance):
            # new card added in player's hand object (background)
            playerHand.addCard(deck.deal())

            # appending newly added card in player's hand list
            for i in playerHand.cards:
                if str(i) not in playerHandList:
                    playerHandList.append(str(i))
            playerHand.adjustForAce()

            # Displaying value of cards in gui
            self.PlayerTotalLabel.text = str(playerHand.value)

            # adding new cards to player's hand in gui
            if len(playerHandList) == 3:
                self.playerCardImage3.source = imagePath + playerHandList[2]
                self.compCardImage2.source = imagePath + compHandList[1]
                time.sleep(1)

            elif len(playerHandList) == 4:
                self.playerCardImage4.source = imagePath + playerHandList[3]
                time.sleep(1)

            elif len(playerHandList) == 5:
                self.playerCardImage5.source = imagePath + playerHandList[4]
                time.sleep(1)

            # printing all details/logs on console
            print("HIT button pressed!")
            print("Player's cards:", playerHandList)
            print("Player's total:", playerHand.value)
            print("Computer's cards:", compHandList)
            print("Computer's total:", compHand.value)

            # checking if game ends or not
            if playerHand.value > 21 or compHand.value > 21 or compHand.value > playerHand.value \
                    or compHand.value < playerHand.value:
                displayResult()

        # function for playing computer's hand if  player clicks stay
        def stayFunction(instance):
            # if player isn't busted then adding a card to computer's hand
            if playerHand.value <= 21:
                self.compCardImage2.source = imagePath + compHandList[1]
                time.sleep(1)

                # while compHand.value < 17:
                while True:

                    # new card added in computers's hand object (background)
                    compHand.addCard(deck.deal())

                    # appending newly added card in computer's hand list
                    for i in compHand.cards:
                        if str(i) not in compHandList:
                            compHandList.append(str(i))
                        compHand.adjustForAce()

                    # adding new cards to computer's hand in gui
                    # self.compCardImage2.source = imagePath + compHandList[1]
                    time.sleep(1)

                    if len(compHandList) == 3:
                        self.compCardImage3.source = imagePath + compHandList[2]
                        time.sleep(1)

                    elif len(compHandList) == 4:
                        self.compCardImage4.source = imagePath + compHandList[3]
                        time.sleep(1)

                    elif len(compHandList) == 5:
                        self.compCardImage5.source = imagePath + compHandList[4]
                        time.sleep(1)

                    time.sleep(1)

                    # printing all details/logs on console
                    print("STAY button pressed!")
                    print("Player's cards:", playerHandList)
                    print("Player's total:", playerHand.value)
                    print("Computer's cards:", compHandList)
                    print("Computer's total:", compHand.value)

                    if playerHand.value > 21 or compHand.value > 21 or compHand.value > playerHand.value \
                            or compHand.value < playerHand.value:
                        break

            time.sleep(1)
            # checking if game ends or not
            if playerHand.value > 21 or compHand.value > 21 or compHand.value > playerHand.value \
                    or compHand.value < playerHand.value:
                displayResult()

        # binding buttons with functions
        self.hitButton.bind(on_press=hitFunction)
        self.stayButton.bind(on_press=stayFunction)


# class for managing all windows/screens
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.add_widget(WelcomeWindow(name="Welcome"))
        self.add_widget(BetWindow(name="Bet"))
        self.add_widget(GameWindow(name="Game"))
        self.add_widget(NewBetWindow(name="newBet"))


# kv code
kv = Builder.load_string("""

WindowManager:
    WelcomeWindow:
    BetWindow:
    GameWindow:
    NewBetWindow:


<WelcomeWindow>:
    rulesTextInput: rulesTextInput
    GridLayout:
        cols: 1
        Image:
            source: "honors_spade-14.png"
            keep_ratio: True

        Label:
            text: "- BLACKJACK RULES -"
            font_size: 35
            outline_width: 1
            outline_color: (0, 0.5, 0.5, 1)
            color: (1, 1, 1, 1)
            size_hint: .3, .3

        TextInput:
            id: rulesTextInput
            text: "(1) HIT - means ask for another card in an attempt to get closer to a sum of 21, or even hit 21 exactly. (2) STAY - means NOT ask for another card and let computer take new card. (3) BUST - If sum is over 21. (4) The player goes first and must decide whether to STAY or HIT. (5) Thus, a player may STAY on the two cards originally dealt to them, OR they may ask the computer dealer for additional cards, one at a time, until deciding to STAY on the total (if it is 21 or under), OR goes BUST. (6) Player can count the ace as a 1 or 11. (7) If the draw creates a BUST hand by counting the ace as an 11, then player simply counts the ace as a 1 and continues playing by STAYING or HITTING."
            font_size: 20
            readonly: True
            valign: "center"

        Button:
            text: "CLICK HERE TO START"
            font_size: 35
            size_hint: .7, .7
            pos: 100,100
            background_color: (0, 1, 1, 1)
            outline_color: (0, 1, 1, 1)
            on_release:
                root.manager.current = "Bet"


<BetWindow>:

<GameWindow>:

<NewBetWindow>:

<PopupWindow>:
    popupLabel: popupLabel
    Label:
        id: popupLabel
        text: "TEMP TEXT"
        font_size: 20
        color: (0,1,1,1)
        valign: "center"
        halign: "center"
        size_hint: 0.6, 0.2
        pos_hint: {"x": 0.2, "top": 0.7}


""")


# class for running the app
class BlackJackApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    BlackJackApp().run()

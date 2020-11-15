import random
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

from kivy.clock import Clock


suits=('H', 'D', 'S', 'C')
ranks=[2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
values={'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}
imagePath="/home/shubham/Desktop/PLP/PROJECT/BlackJack - ShubhAm/Images/"

#Supporting classes and methods used in gameplay for initializing things
class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank

    def __str__(self):
        return str(self.rank)+self.suit+".png" #returned cards in the file formats of images

class Deck:
    def __init__(self):
        self.deck=[] #Empty deck created..
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) #Added all 52 cards in deck by combining global suits and ranks..

    def __str__(self): #exrta methhod to test whats in our deck..
        deckComposition='' 
        for card in self.deck:
            deckComposition += '\n '+card.__str__()
        return 'The deck has:' + deckComposition

    def shuffle(self):
        random.shuffle(self.deck) #method for shuffling deck

    def deal(self):
        singleCard = self.deck.pop() #selecting a card from shuffled deck
        return singleCard

class Hand:
    def __init__(self):
        self.cards=[]  #start with an empty list as we did in the Deck class
        self.value=0   #start with zero value
        self.aces=0    #add an attribute to keep track of aces
    
    def addCard(self,card):
        self.cards.append(card)
        self.value+=values[str(card.rank)]
        if card.rank=='A':
            self.aces+=1

    def adjustForAce(self):
        while self.value>21 and self.aces:
            self.value-=10
            self.aces-=1

    def __str__(self):
        return self.cards

class Coins:
    def __init__(self):
        self.total=100
        self.bet=0

    def win(self):
        self.total+=self.bet

    def lose(self):
        self.total-=self.bet



######





######




#GUI
class WelcomeWindow(Screen):
    pass

class BetWindow(Screen):
    pass

screen_manager = ScreenManager()
screen_manager.add_widget(WelcomeWindow(name = "Welcome"))
screen_manager.add_widget(BetWindow(name = "Bet"))

class GameWindow(GridLayout,Screen):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.cols=1
        self.rows=2
        
        self.GameWindow1=GridLayout()
        self.GameWindow1.cols=1
        self.GameWindow1.rows=3
        self.GameWindow1.add_widget(Label(text="COMPUTER DEALER", font_size=20, color = (0,1,1,1), halign = "center", valign = "center"))

        self.GameWindow2=GridLayout()
        self.GameWindow2.cols=7
        self.GameWindow2.rows=1
        self.GameWindow2.add_widget(Label(text=""))
        compCardImage1=Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(compCardImage1)
        compCardImage2=Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(compCardImage2)
        compCardImage3=Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(compCardImage3)
        compCardImage4=Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(compCardImage4)
        compCardImage5=Image(source=imagePath + "blue_back.png")
        self.GameWindow2.add_widget(compCardImage5)
        self.GameWindow2.add_widget(Label(text=""))

        self.GameWindow3=GridLayout()
        self.GameWindow3.cols=1
        self.GameWindow3.rows=1

        self.GameWindow4=GridLayout()
        self.GameWindow4.cols=1
        self.GameWindow4.rows=3

        self.GameWindow5=GridLayout()
        self.GameWindow5.cols=7
        self.GameWindow5.rows=1
        self.GameWindow5.add_widget(Label(text=""))
        playerCardImage1=Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(playerCardImage1)
        playerCardImage2=Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(playerCardImage2)
        playerCardImage3=Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(playerCardImage3)
        playerCardImage4=Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(playerCardImage4)
        playerCardImage5=Image(source=imagePath + "blue_back.png")
        self.GameWindow5.add_widget(playerCardImage5)
        self.GameWindow5.add_widget(Label(text=""))

        self.GameWindow6=GridLayout()
        self.GameWindow6.cols=1
        self.GameWindow6.rows=1
        self.GameWindow6.add_widget(Label(text="PLAYER", font_size=20, color=(0,1,1,1), halign="center", valign="center"))

        self.GameWindow7=GridLayout()
        self.GameWindow7.cols=7
        self.GameWindow7.rows=1
        self.GameWindow7.add_widget(Label(text=""))
        self.GameWindow7.add_widget(Label(text=""))
        self.hitButton=Button(text="HIT", font_size=20, background_color=(0,1,1,1))

        self.GameWindow7.add_widget(self.hitButton)
        self.GameWindow7.add_widget(Label(text=""))
        self.stayButton=Button(text="STAY", font_size=20, background_color=(0,1,1,1))
        self.GameWindow7.add_widget(self.stayButton)
        self.GameWindow7.add_widget(Label(text=""))
        self.GameWindow7.add_widget(Label(text=""))

        self.add_widget(self.GameWindow1)
        self.GameWindow1.add_widget(self.GameWindow2)
        self.GameWindow1.add_widget(self.GameWindow3)

        self.add_widget(self.GameWindow4)
        self.GameWindow4.add_widget(self.GameWindow5)
        self.GameWindow4.add_widget(self.GameWindow6)
        self.GameWindow4.add_widget(self.GameWindow7)




        deck = Deck()
        deck.shuffle()
        playerCoins = Coins()
        playing=True

        
        playerHandList = []
        compHandList = []
        
        #creating starting status of game
        playerHand = Hand()
        playerHand.addCard(deck.deal())
        playerHand.addCard(deck.deal())
                
        compHand = Hand()
        compHand.addCard(deck.deal())
        compHand.addCard(deck.deal())
        
        #appending starting cards into respective lists
        for i in playerHand.cards:
            playerHandList.append(str(i))
        for i in compHand.cards:
            compHandList.append(str(i))
        
        #displaying starting cards in gui
        playerCardImage1.source = imagePath + playerHandList[0]
        playerCardImage2.source = imagePath + playerHandList[1]
        compCardImage1.source = imagePath + compHandList[0]

        

        def hit(instance):
            playerHand.addCard(deck.deal())  #new card added in player's hand object (background)
            for i in playerHand.cards:
                if str(i) not in playerHandList:
                    playerHandList.append(str(i)) #append newly added card in player hand list
            playerHand.adjustForAce()

            #adding new cards in gui
            print(playerHandList)
            if len(playerHandList) == 3:
                playerCardImage3.source = imagePath + playerHandList[2] #3rd card showed
            elif len(playerHandList) == 4:
                playerCardImage4.source = imagePath + playerHandList[3] #4th card showed
            elif len(playerHandList) == 5:
                playerCardImage4.source = imagePath + playerHandList[4] #5th card showed
            
            #checking if player busts or not
            if playerHand.value > 21:
                '''
                write bust code here
                '''
                print("player bust!")
                screen_manager.current = "Bet"
        
                
        
       
            
        #binding buttons with functions
        self.hitButton.bind(on_press=hit)
 

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("card.kv")

class MyCardApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyCardApp().run()
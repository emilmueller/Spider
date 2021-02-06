from tkinter import *
from PIL import Image, ImageTk
import random

class Card:
    suitChars = ['H','D','C','S']
    rankChars = [None,'A','2','3','4','5','6','7','8','9','T','J','Q','K']
    posX=-1
    posY=-1
    suit = -1
    rank = -1
    showCard = False
    image = None
    backImage = None
    imageWidth = 110 #Pixels
    imageHeight = 0

    @staticmethod
    def makeFullStack(num, shuffle=True):
        res = []
        for n in range(num):
            for s in range(4):
                for r in range(1,14):
                    c = Card(s,r)
                    res.append(c)
        if shuffle:
            random.shuffle(res)
        return res

    @staticmethod
    def getCardWidth() -> int:
        return int(Card.imageWidth)

    @staticmethod
    def getCardHeight() -> int:
        tempC = Card(0,1)
        return int(tempC.getImageHeight())
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.showCard = False
        fn = self.getRankChar()+""+self.getSuitChar()
        self.image = Image.open("cardsSVG\\"+fn+".png")
        imageSize = self.imageWidth/self.image.size[0]
        self.image=self.image.resize((int(self.image.size[0]*imageSize),int(self.image.size[1]*imageSize)),Image.ANTIALIAS)
        self.imageHeight = self.image.size[1]
        self.backImage = Image.open("cardsSVG\\1B.png")
        self.backImage=self.backImage.resize((int(self.backImage.size[0]*imageSize),int(self.backImage.size[1]*imageSize)),Image.ANTIALIAS)


    def getSuit(self):
        return self.suit
   
    
    def getSuitChar(self):
        return self.suitChars[self.suit]
    
    def getRank(self):
        return self.rank
    
    def getRankChar(self):
        return self.rankChars[self.rank]
    
    def __str__(self):
        res = self.getRankChar()+""+self.getSuitChar()
        if self.showCard:
            res = res +"*"
        return res

    def __repr__(self):
        res = self.getRankChar() + "" + self.getSuitChar()
        if self.showCard:
            res = res + "*"
        return res
    
    def turn(self):
        self.showCard = not self.showCard

    def isShowCard(self):
        return self.showCard

    def moveTo(self,x,y):
        self.posX=x
        self.posY=y

    def getImg(self):
        if self.showCard:

            return ImageTk.PhotoImage(self.image)
        else:

            return ImageTk.PhotoImage(self.backImage)

    def getImageWidth(self):
        return self.imageWidth

    def getImageHeight(self):
        return self.imageHeight
    
    def suits(self,c):
        if self.getSuit()==c.getSuit():
            return True
        else:
            return False

    def getPosition(self):
        return (self.posX, self.posY)
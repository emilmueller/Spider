from card import *
import tkinter as tk
import sys
import time

pgWidth = 1220
pgHeight = 1000

root = tk.Tk(baseName='Spider Solitaire')
root.title('Spider Solitaire')
root.geometry(str(pgWidth) + "x" + str(pgHeight))

table = Canvas(root, width=pgWidth, height=pgHeight)
table.configure(bg='darkgreen')
table.pack()

completed = [[] for i in range(8)]
completedSuits = 0
active = [[] for i in range(10)]
stack = []

moves = []

completedPositions = []

# Params for Card-Positioning
marginLeft = 10
marginTop = 10
marginTopSecondRow = 200
cardsVerticalSpace = 15
marginCardLeft = 5

selectedCard = (-1, -1)
targetPile = -1

sys.setrecursionlimit(2000)
print('*********************')
print(sys.getrecursionlimit())
print('*********************')

# Temp-Containers for Graphics

movingCards = None
movingCardsImg = []
pileCardsImg = [[] for i in range(10)]
stackCardsImg = []
completedImg = None
dragging = False

won = False

x = 0
y = 0


def init():
    global completed, active, stack, moves, selectedCard  # ,completedImg, stackImg
    completed = [[] for i in range(8)]
    active = [[] for i in range(10)]
    stack = []
    moves = []
    selectedCard = (-1, -1)


def drag(event):
    global targetPile, movingCards, dragging, movingCardsImg
    mx = event.x
    my = event.y
    movingCardsImg = []

    if selectedCard[1] >= 0:
        if movingCards is None:

            movingCards = active[selectedCard[0]][selectedCard[1]:]
            for c in movingCards:
                movingCardsImg.append(c.getImg())
            removeCards(selectedCard[0], selectedCard[1])
            drawPlayGround()
        for i in range(len(movingCards)):
            movingCardsImg.append(movingCards[i].getImg())

            tempImg = movingCardsImg[i]
            im = table.create_image(mx, my + i * 20, image=tempImg)

        targetPile = getCardIndex(mx, my)
        dragging = True


def placeCard(event):
    global movingCards, movingCardsImg
    print(selectedCard)
    if dragging:
        targetCol = targetPile[0]
        if len(active[targetCol]) == 0 or movingCards[0].getRank() == active[targetCol][-1].getRank() - 1:
            doMove([selectedCard[0], selectedCard[1], targetCol, movingCards, False, False])

        else:
            appendCards(selectedCard[0], movingCards)
    else:
        if selectedCard[1] != -1:
            if selectedCard[1] == -2:
                # get new Cards from Stack
                # print("Get new Cards")
                doMove([-2, -1, -1, -1, False])

            else:
                suitFound = False
                # check for card with same suit
                for i in range(10):
                    print(i, end='')
                    try:
                        if len(active[i]) > 0 and active[i][-1].getRank() == active[selectedCard[0]][
                            selectedCard[1]].getRank() + 1 and active[i][
                            -1].getSuit() == active[selectedCard[0]][selectedCard[1]].getSuit():
                            doMove([selectedCard[0], selectedCard[1], i, active[selectedCard[0]][selectedCard[1]:], True,
                                    False])
                            # removeCards(selectedCard[0], selectedCard[1])
                            suitFound = True
                            break
                    except IndexError:
                        print("i: "+str(i)+" selected: "+str(selectedCard))
                        print(len(active[i]), end=' ')
                        print(active[i][-1])
                        print(active[selectedCard[0]][selectedCard[1]])

                if not suitFound:
                    rankFound = False
                    # check for card with rank -1
                    for i in range(10):
                        if len(active[i]) > 0 and active[i][-1].getRank() == active[selectedCard[0]][
                            selectedCard[1]].getRank() + 1:
                            # removeCards(selectedCard[0], selectedCard[1])
                            doMove(
                                [selectedCard[0], selectedCard[1], i, active[selectedCard[0]][selectedCard[1]:], True,
                                 False])
                            rankFound = True
                            break
                if not suitFound and not rankFound:
                    # check for empty pile
                    for i in range(10):
                        if len(active[i]) == 0:
                            # removeCards(selectedCard[0], selectedCard[1])
                            doMove(
                                [selectedCard[0], selectedCard[1], i, active[selectedCard[0]][selectedCard[1]:], True,
                                 False])
                            break

    drawPlayGround()
    print(getPossibleMoves())
    movingCards = None
    movingCardsImg = []
    # printPlayGround()
    # print(makeMoves())


def chooseCard(event):
    global selectedCard, dragging, won
    if not won:
        mx = event.x
        my = event.y
        c, r = getCardIndex(mx, my)
        # print(c, r)
        dragging = False
        if r > -1 and active[c][r].isShowCard():
            suited = True
            for j in range(r, len(active[c])):
                suited = suited and active[c][j].getRank() == active[c][r].getRank() - (j - r) and active[c][
                    j].getSuit() == \
                         active[c][r].getSuit()
            if suited:
                selectedCard = (c, r)
            else:
                selectedCard = (-1, -1)

        elif r == -2:
            # Deal new Cards from Stack
            selectedCard = (c, r)
        else:
            # Do Nothing
            selectedCard = (-1, -1)
    else:
        init()
        shuffle()
        drawPlayGround()
        won = False


def sortMoves(inList, out, desc):
    # print("in: ",mList)
    maxRank = -1
    ranks = []
    for i in range(len(inList)):
        ranks.append((inList[i][3][0].getRank(), i))
    # print(ranks)
    ranks.sort(key=lambda x: x[0], reverse=desc)

    for r in ranks:
        out.append(inList[r[1]])


def getPossibleMoves():
    pMoves = []
    sIndices = []
    suitFound = False
    # print(moves)
    # normal moves
    tmpMoves = []
    for sPile in range(10):
        j = len(active[sPile]) - 1
        sIndex = j
        while sIndex - 1 >= 0:
            if active[sPile][sIndex - 1].isShowCard() and active[sPile][sIndex].getSuit() == active[sPile][
                sIndex - 1].getSuit() and active[sPile][sIndex].getRank() == active[sPile][sIndex - 1].getRank() - 1:
                sIndex = sIndex - 1
            else:
                break
        source = sPile
        sourceIndex = sIndex
        sIndices.append(sourceIndex)

        # find suited matching moves

        for tPile in range(10):

            if tPile != source:
                for tmpIndex in range(sourceIndex, len(active[source])):
                    # print(tPile, len(active[tPile]))
                    if len(active[tPile]) > 0 and tmpIndex >= 0 and active[tPile][-1].getRank() == active[source][
                        tmpIndex].getRank() + 1:
                        if len(active[source]) > 1 and sourceIndex - 1 > 0 and not active[source][
                            sourceIndex - 1].isShowCard():
                            m = [source, tmpIndex, tPile, active[source][tmpIndex:], True, False]
                            tmpMoves.append(m)
                        elif active[tPile][-1].getSuit() == active[source][tmpIndex].getSuit():
                            m = [source, tmpIndex, tPile, active[source][tmpIndex:], True, False]
                            tmpMoves.append(m)
                            # if m not in moves:
                            #     tmpMoves.append(m)
                            #     suitFound=True
                            # else:
                            #     print("***FOUND***",m)
    sortMoves(tmpMoves, pMoves, True)

    # print(sIndices)
    tmpMoves = []
    # if not suitFound:
    if True:
        notSuitFound = False
        for sPile in range(10):

            source = sPile
            sourceIndex = sIndices[sPile]

            # find not suited matcing moves
            for tPile in range(10):

                if tPile != source:
                    if len(active[tPile]) > 0 and sourceIndex >= 0 and active[tPile][-1].getRank() == active[source][
                        sourceIndex].getRank() + 1:
                        m = [source, sourceIndex, tPile, active[source][sourceIndex:], True, False]
                        if m not in pMoves:
                            tmpMoves.append(m)
                        # if m not in pMoves:
                        #     if m not in moves:
                        #         tmpMoves.append(m)
                        #     else:
                        #         print("***FOUND***", m)
        sortMoves(tmpMoves, pMoves, True)
        tmpMoves = []
        # if not notSuitFound:
        if True:
            for sPile in range(10):
                source = sPile
                sourceIndex = sIndices[sPile]

                # find empty piles
                if sourceIndex > 0:
                    for tPile in range(10):

                        if tPile != source:
                            if len(active[tPile]) == 0:
                                m = [source, sourceIndex, tPile, active[source][sourceIndex:], True, False]
                                if m not in pMoves:
                                    tmpMoves.append(m)
                                # if m not in moves:
                                #     tmpMoves.append(m)
                                # else:
                                #     print("***FOUND***", m)
        sortMoves(tmpMoves, pMoves, False)
    # deal cards from Stack
    if len(stack) > 0:
        pMoves.append([-2, 0, 0, 0, False])

    # print("-->",pMoves)
    return pMoves


def autoplay(event):
    makeMoves(0)


def makeMoves(rekCounter):
    global completedPositions
    if rekCounter == sys.getrecursionlimit() - 1:
        print("---Too complicated ---")
        return False

    if isWon():
        print("______________SOLVED_____________")
        return True
    else:
        pMoves = getPossibleMoves()
        for move in pMoves:
            if hash(str(active) + str(move)) not in completedPositions:
                print(rekCounter, " - ", len(stack) // 10, "-", completedSuits, " ->", move)
                completedPositions.append(hash(str(active) + str(move)))
                doMove(move)

                drawPlayGround()

                # time.sleep(0.003)
                if makeMoves(rekCounter + 1):
                    undoMove(None)
                    return True

                undoMove(None)
            # else:
            #     print("Move",move,"already TESTED ++++++++++++++++++")

    return False


def shuffle():
    global stack
    deck = Card.makeFullStack(2, True)
    for i in range(54):
        if i > 43:
            deck[i].turn()
        appendCards(i % 10, [deck[i]])
    for i in range(54, 104):
        stack.append(deck[i])


def getCardX(num):
    cardWidth = Card.getCardWidth()
    cardHeight = Card.getCardHeight()
    cardX = marginLeft + (2 * num + 1) * marginCardLeft + num * cardWidth
    return cardX


def getCardIndex(x, y):
    c = (x - marginLeft) // (Card.getCardWidth() + 2 * marginCardLeft)
    r = -1
    for i in range(len(active[c])):
        tempC = active[c][i]
        if tempC.getPosition()[1] < y < tempC.getPosition()[1] + tempC.getImageHeight():
            r = i
    for i in range(len(stack)):
        (cx, cy) = stack[i].getPosition()
        if cx < x < cx + Card.getCardWidth() and cy < y < cy + Card.getCardHeight():
            r = int(-2)

    return c, r


def printPlayGround():
    max = 0
    for c in range(len(active)):
        if len(active[c]) > max:
            max = len(active[c])
    for r in range(max):
        for c in range(len(active)):
            if r >= len(active[c]):
                print("  ", end='  '),
            else:
                if active[c][r].isShowCard():
                    print(active[c][r], end=' '),
                else:
                    print(active[c][r], end='  '),
        print()
    print()


def drawPlayGround():
    global pileCardsImg, stackCardsImg, completedImg
    table.delete("all")
    # print(".", end='')
    cardWidth = Card.getCardWidth()
    cardHeight = Card.getCardHeight()
    pileCardsImg = [[] for i in range(10)]
    stackCardsImg = []
    completedImg = []
    # empty squares

    for i in range(8):
        if len(completed[i]) > 0:
            completedImg.append(completed[i][0].getImg())
            tmpImg = completedImg[i]
            table.create_image(getCardX(i), marginTop, image=tmpImg, anchor=NW)
        else:
            table.create_rectangle(getCardX(i), marginTop,
                                   getCardX(i) + cardWidth, marginTop + cardHeight, fill='#1e3813')

    # Stack
    for i in range(len(stack) // 10):
        stack[i * 10].moveTo(50 + getCardX(8) + i * 10, marginTop)
        stackCardsImg.append(stack[i * 10].getImg())
        tmpImg = stackCardsImg[i]
        table.create_image(50 + getCardX(8) + i * 10, marginTop, image=tmpImg, anchor=NW)

    # Piles
    for c in range(10):
        x = getCardX(c)
        countShowCards = 0
        for r in range(len(active[c])):
            y = marginTopSecondRow + r * cardsVerticalSpace
            if active[c][r].isShowCard():
                y = y + countShowCards * 20
                countShowCards = countShowCards + 1
            pileCardsImg[c].append(active[c][r].getImg())
            tmpImg = pileCardsImg[c][r]
            active[c][r].moveTo(x, y)

            table.create_image(x, y, image=tmpImg, anchor=NW)
    if won:
        table.create_text(600, 700, fill="red", font="Arial 40 bold",
                          text='GEWONNEN')
    table.update()


def appendCards(c, cards):
    for tc in cards:
        active[c].append(tc)


def removeCards(c, r):
    for i in range(r, len(active[c])):
        del active[c][-1]


def turnCard(c):
    active[c][-1].turn()

    # drawPlayGround()


def removeCompletedSuit():
    global completedSuits
    for i in range(10):
        j = len(active[i]) - 13
        # print("Check", len(active[i]),i, j),
        if j >= 0 and active[i][j].isShowCard() and active[i][j].getRank() == 13:

            match = True
            turn = False
            ti = j + 1
            while match and ti < j + 13:
                # print(ti),
                match = match and active[i][ti - 1].getRank() == active[i][ti].getRank() + 1 and active[i][
                    ti - 1].getSuit() == active[i][ti].getSuit()
                ti = ti + 1
            if match and ti == j + 13:
                for l in range(8):
                    if len(completed[l]) == 0:
                        break
                for k in range(13):
                    active[i][j + k].moveTo(-1, -1)
                    completed[l].append(active[i][j + k])
                completedSuits = completedSuits + 1

                removeCards(i, j)
                if len(active[i]) > 0 and not active[i][-1].isShowCard():
                    turnCard(i)
                    turn = True
                moves.append([i, l, turn])


def isWon():
    if len(completed[7]) > 0:
        return True
    else:
        return False


def doMove(move):
    # input: [source, sourceIndex, target, cards, remove, turn] --> (remove indicates whether cards has to be removed from source)
    # moves:
    # [source, target, cards, turn] --> normal move (turn indicates wether a card on the pile was turned)
    # [-1] --> Deal new Cards
    # [source, target, turn] -->  remove completed suit from pile source to completed[l] (turn indicates wether a card on the pile was turned)
    global moves, won
    # print(move)
    # print(hash(str(active)+str(move)))
    if move[0] == -2:
        # Deal new Cards
        for i in range(10):
            j = len(stack) - 10 + i
            tmpC = stack[j]

            appendCards(i, [tmpC])
            turnCard(i)
            del stack[j]

        # drawPlayGround()
        moves.append([-1])
        removeCompletedSuit()
    else:
        # Do normal move
        turn = False

        appendCards(move[2], move[3])
        if move[4]:
            removeCards(move[0], move[1])
        if len(active[move[0]]) > 0 and not active[move[0]][-1].isShowCard():
            turnCard(move[0])
            turn = True
        moves.append([move[0], move[1], move[2], move[3], move[4], turn])
        removeCompletedSuit()
        won = isWon()
    # printPlayGround()
    # drawPlayGround()


def undoMove(event):
    global completedSuits
    if len(moves) > 0:
        move = moves[-1]
        if len(move) == 1:
            # unDeal Cards from Stack
            for i in range(10):
                active[i][-1].turn()

                active[i][-1].moveTo(-1, -1)
                stack.append(active[i][-1])

                removeCards(i, len(active[i]) - 1)

        elif len(move) == 3:
            # undo completed Suit
            if move[2]:
                turnCard(move[0])
            appendCards(move[0], completed[move[1]])
            completed[move[1]] = []
            completedSuits = completedSuits - 1



        else:
            # normal move
            removeCards(move[2], len(active[move[2]]) - len(move[3]))
            if move[5]:
                turnCard(move[0])
            appendCards(move[0], move[3])
        del moves[-1]
    if event is not None:
        drawPlayGround()


shuffle()
drawPlayGround()

# table.create_image(30, 200, image=images[0], anchor=NW)
# print(images[0].height())
# c.create_image(30,50, image=img2, anchor=NW)
root.bind('<B1-Motion>', drag)
root.bind('<Button-1>', chooseCard)
root.bind('<ButtonRelease-1>', placeCard)
root.bind('<Button 2>', autoplay)
root.bind('<Button 3>', undoMove)
root.mainloop()

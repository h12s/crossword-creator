import tkinter as tk         #add size of crossword, and display words on side

def display():
    root = tk.Tk()
    root.title("Crossword Generator")
    count = 1
    for i in range(0, len(L), 1):
        for j in range(0, len(L), 1):
            if L[i][j] != ' ':
                canvas = tk.Canvas(root, bg = "white", width = 45, height = 45, bd = 1, highlightthickness = 0, relief = "solid")
                canvas.create_text(23, 23, text = L[i][j], font = ("Helvetica", 14))
                if (i, j) in coords:
                    canvas.create_text(8, 8, text = count, font = ("Helvetica", 8))
                    count += 1
            else:
                canvas = tk.Canvas(root, bg = "black", width = 45, height = 45, bd = 1, highlightthickness = 0, relief = "solid")
            canvas.grid(row = i, column = j)

    if len(skippedWords) > 0:      #prints skipped words with reasons
        print()
        for i in range(1, len(skippedWords), 2):
            print('Skipped word:', skippedWords[i],'\tReason:', skippedWords[i - 1])
    print()

    root.mainloop()
     
def crossword(words, BOARD_SIZE):

    #if possible, places the word horizontally along the center and returns True or False depending on if it could or not
    def placeFirstWord(word):
        if len(word) > BOARD_SIZE:      #could not place word
            global reason
            reason = 'reaches outside grid'
            skippedWords.append(reason)
            skippedWords.append(word)
            return False

        count = 0
        for i in range((BOARD_SIZE // 2) - (len(word) // 2), (BOARD_SIZE // 2) - (len(word) // 2) + len(word), 1):
            global L
            L[BOARD_SIZE // 2 - 1][i] = word[count]
            horizontalTable[BOARD_SIZE // 2 - 1][i] = False
            count += 1

        coords.append((BOARD_SIZE // 2 - 1, (BOARD_SIZE // 2) - (len(word) // 2)))

        return True

    #places the word vertically if possible and returns True or False depending on if it could or not
    def placeWordVertically(word):
        for i in range(0, len(L), 1):
            for j in range(0, len(L), 1):  

                for w in range(0, len(word), 1):    #indices of word
                    if L[i][j] == word[w]:          #intersection point

                        if verticallyLegal(word, w, i, j) == True:    #placing the word if possible

                            if (i - len(word[0:w]), j) not in coords:
                                coords.append((i - len(word[0:w]), j))
                            
                            verticalTable[i][j] = False
                            for up in range(1, len(word[0:w]) + 1, 1):    #going up
                                L[i - up][j] = word[w - up]
                                verticalTable[i - up][j] = False
 
                            for down in range(1, len(word[w:]), 1):    #going down
                                L[i + down][j] = word[w + down]
                                verticalTable[i + down][j] = False

                            return True
                    
        return False


    #places the word horizontally if possible and returns True or False depending on if it could or not
    #Also, the 'reason' getting for why a word can't be placed is done here (as first checks if word could be placed vertically, and if not then horizontally)
    def placeWordHorizontally(word):
        foundMatchingLetter = False 
        for i in range(0, len(L), 1):
            for j in range(0, len(L), 1):
 
                for w in range(0, len(word), 1):    #indices of word
                    if L[i][j] == word[w]:          #intersection point
                        foundMatchingLetter = True

                        if horizontallyLegal(word, w, i, j) == True:    #placing the word if possible

                            if (i, j - len(word[0:w])) not in coords:
                                coords.append((i, j - len(word[0:w])))
                            
                            horizontalTable[i][j] = False
                            for left in range(1, len(word[0:w]) + 1, 1):   #going left
                                L[i][j - left] = word[w - left]
                                horizontalTable[i][j - left] = False

                            for right in range(1, len(word[w:]), 1):    #going right
                                L[i][j + right] = word[w + right]
                                horizontalTable[i][j + right] = False
                        
                            return True

        if foundMatchingLetter == False:     
            global reason
            reason = 'no matching letter'
        elif len(word) > BOARD_SIZE:
            reason = 'reaches outside grid'
        skippedWords.append(reason)
        
        return False                 


    #determines if word can be placed at the desired location legally with the index w of the word being the intersection point
    def verticallyLegal(word, w, i, j):
        if verticalTable[i][j] == False:
            return False
    
        for up in range(0, len(word[0:w]) + 1, 1):    #going up and checking if word can be placed from point of intersection
            if i - up < 0 or i - up > BOARD_SIZE - 1:       #out of bounds
                return False
            elif verticalTable[i - up][j] == False:   #runs into another vertical word
                return False
            elif L[i - up][j] != ' ':
                if L[i - up][j] != word[w - up]:    #is intersection legal
                    return False
                pass
            elif j - 1 < 0:                       #adjacency checking 
                if L[i - up][j + 1] != ' ':       
                    return False
            elif j + 1 > BOARD_SIZE - 1:
                if L[i - up][j - 1] != ' ':
                    return False
            elif L[i - up][j - 1] != ' ' or L[i - up][j + 1] != ' ':
                return False
            elif up == len(word[0:w]):         #last letter going up adjacency checking
                if i - up - 1 >= 0 and i - up - 1 <= BOARD_SIZE - 1:
                    if L[i - up - 1][j] != ' ':
                        return False

        for down in range(0, len(word[w:]), 1):    #going down and checking if word can be placed from point of intersection
            if i + down < 0 or i + down > BOARD_SIZE - 1:    #out of bounds
                return False
            elif verticalTable[i + down][j] == False:   #runs into another vertical word
                return False
            elif L[i + down][j] != ' ':
                if L[i + down][j] != word[w + down]:   #is intersection legal
                    return False
                pass
            elif j - 1 < 0:                     #adjaceny checking
                if L[i + down][j + 1] != ' ':
                    return False
            elif j + 1 > BOARD_SIZE - 1:
                if L[i + down][j - 1] != ' ':
                    return False
            elif L[i + down][j - 1] != ' ' or L[i + down][j + 1] != ' ':
                return False
            elif down == len(word[w:]) - 1:    #last letter going down adjacency checking
                if i + down + 1 >= 0 and i + down + 1 <= BOARD_SIZE - 1:
                    if L[i + down + 1][j] != ' ':
                        return False

        return True


    #determines if word can be placed at the desired location horizontally with the index w of the word being the intersection point
    def horizontallyLegal(word, w, i, j):
        if horizontalTable[i][j] == False:
            global reason
            reason = 'illegal adjacencies'
            return False
    
        for left in range(0, len(word[0:w]) + 1, 1):      #going left and checking if word can be placed from point of intersection
            if j - left < 0 or j - left > BOARD_SIZE - 1:             #out of bounds
                reason = 'reaches oustide grid'
                return False
            elif horizontalTable[i][j - left] == False:    #runs into another horizontal word
                reason = 'illegal adjacencies'
                return False
            elif L[i][j - left] != ' ':
                if L[i][j - left] != word[w - left]:     #is intersection legal
                    reason = 'illegal adjacencies'
                    return False
                pass 
            elif i + 1 > BOARD_SIZE - 1:                            #adjacency checking
                if L[i - 1][j - left] != ' ':
                    reason = 'illegal adjacencies' 
                    return False
            elif i - 1 < 0:
                if L[i + 1][j - left] != ' ':
                    reason = 'illegal adjacencies' 
                    return False
            elif L[i + 1][j - left] != ' ' or L[i - 1][j - left] != ' ':
                reason = 'illegal adjacencies' 
                return False
            elif left == len(word[0:w]):              #last letter going left adjacency checking
                if j - left - 1 >= 0 and j - left - 1 <= BOARD_SIZE - 1:    
                    if L[i][j - left - 1] != ' ':
                        reason = 'illegal adjacencies' 
                        return False
 
        for right in range(0, len(word[w:]), 1):      #going right and checking if word can be placed from point of intersection
            if j + right < 0 or j + right > BOARD_SIZE - 1:       #out of bounds
                reason = 'reaches outside grid'
                return False
            elif horizontalTable[i][j + right] == False:    #runs into another horizontal word
                reason = 'illegal adjacencies'
                return False
            elif L[i][j + right] != ' ':                   
                if L[i][j + right] != word[w + right]:     #is intersection legal
                    reason = 'illegal adjacencies'
                    return False 
                pass
            elif i + 1 > BOARD_SIZE - 1:                         #adjacency checking
                if L[i - 1][j + right] != ' ':
                    reason = 'illegal adjacencies' 
                    return False
            elif i - 1 < 0:
                if L[i + 1][j + right] != ' ':
                    reason = 'illegal adjacencies' 
                    return False
            elif L[i + 1][j + right] != ' ' or L[i - 1][j + right] != ' ':
                reason = 'illegal adjacencies' 
                return False
            elif right == len(word[w:]) - 1:           #last letter going right adjacency checking
                if j + right + 1 >= 0 and j + right + 1 <= BOARD_SIZE - 1:
                    if L[i][j + right + 1] != ' ':
                        reason = 'illegal adjacencies' 
                        return False

        return True


    #print the board along with any skipped words with their reasons beneath it
    def printBoard():
        string = '|'

        print(' ' + '0 1 2 3 4 5 6 7 8 9 ' * 2)
        print(' ' + '_ ' * 20 + ' ')
        
        for i in range(0, len(L), 1):
            for j in range(0, len(L), 1):
                string += L[i][j] + ' '
            print(string[0:-1] + '| ' + str(i))
            string = '|'
            
        print(' ' + '_ ' * 20 + ' ')
        print(' ' + '0 1 2 3 4 5 6 7 8 9 ' * 2)

        if len(skippedWords) > 0:      #prints skipped words with reasons
            print()
            for i in range(1, len(skippedWords), 2):
                print('Skipped word:', skippedWords[i],'\tReason:', skippedWords[i - 1])
        print()


    #the board    
    global L
    L = [([' '] * BOARD_SIZE) for i in range(0, BOARD_SIZE, 1)]
    
    #places taken by vertical words (indicated by False)
    global verticalTable
    verticalTable = [([True] * BOARD_SIZE) for i in range(0, BOARD_SIZE, 1)]
    
    #places taken by horizontal words (indicated by False)
    global horizontalTable
    horizontalTable = [([True] * BOARD_SIZE) for i in range(0, BOARD_SIZE, 1)]
    
    #skipped Words list (the skipped words are placed in odd indices, with the reason being one indice before each word)
    global skippedWords
    skippedWords = []

    #reason for why a word was skipped (is placed in even indices of 'skippedWords')
    global reason
    reason = ''

    #coords of numbers on the board such as "1 across" or "4 down"
    global coords
    coords = []

    verticalWords = []
    horizontalWords = []

    #goes through the list of words, and first tries to place it vertically, and if can't be placed vertically,
    #tries horizontally. That's the reason why the 'reason' getting for a skipped word is done in the horizontal section only.
    f = False
    for i in range(0, len(words), 1):
        if f == False:                         #goes through words until found one that can be legally added as a first word
            f = placeFirstWord(words[i])
        else:
            v = placeWordVertically(words[i])      #could the word be placed vertically
            
            h = True
            
            if v == False:                            #try if the word could be placed horizontally
                h = placeWordHorizontally(words[i])

            if h == False:                          #can not be placed horizontally or vertically so word must be skipped
                skippedWords.append(words[i])

    display()
    #printBoard()


#---------------------------------------------------------------------------------------------

while True:
    print("Welcome, let's generate a crossword puzzle. (Press 'q' or 'Q' to quit)")
    print()
    print("Board size? (Enter an integer, eg. 18 for 18x18 size)")
    global BOARD_SIZE
    BOARD_SIZE = input(">")
    print()
    print("How many words? (Enter an integer)")
    numOfWords = input(">")
    words = []
    for i in range(0, int(numOfWords), 1):
        print()
        print("Enter word " + str(int(i) + 1) + ":")
        words.append(input(">"))

    crossword(words, int(BOARD_SIZE)) 

    print()


#samples
#crossword(["abcdefghijklmnopqrst",
#           "fffffggg",
#           "ttttttttttuuuuuuuuuz",
#           "yzzz",
#           "qqqqqqqqqqqqqqy",
#           "xxxxxxxxxaaaaaaa",
#           "aaaaggg",
#           "xxwwww",
#           "wwwwvvvvve",
#           "vvvvvvvvvvvvq",
#           "mat",
#           "mat",
#           "make",
#           "make",
#           "maker",
#           "remake",
#           "hat"], 20)

#crossword(['clowning', 'apple', 'addle', 'loonular', 'shaun', 'solar', 'astronaut', 'loonoolar', 'prove', 'across', 'no'], 20)
#crossword(['clowning', 'apple', 'add', 'evening', 'eve', 'good', 'gattling', 'night', 'now', 'winner', 'the', 'game', 'hen', 'engine', 'entire', 'wow', 'mansion', 'wega', 'wega'], 20)
#crossword(['clowning', 'apple', 'addle', 'loon', 'incline', 'plan', 'zoo'], 20)



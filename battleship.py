#When run, a player vs. AI game of Battleship will run
#The user will be able to choose from 3 AI difficulties and the players boats are placed given a file

import random
import sys

#setup() function will set up the game and continue to check if game is still going
def setup():
  seed = getSeed() #get seed
  width = getWidth()#get width
  height = getHeight()#get height
  myBoats = input("Enter the name of the file containing your ship placements: ")
  difficulty = getDifficulty() #get difficulty
  with open(myBoats) as file: #open the file with players boat placements
    boat = []
    ships = []
    lines = file.readlines()
    for line in lines:
      boat.append(line)
    for boa in boat:
      good = boa.split(" ")
      ships.append(good) #put each ship and its coord in a list
    boatList = []
    boatList2 = []
    for ship in ships:
      if ship[0] == "X" or ship[0] == "O" or ship[0] == "*":
        sys.exit(0)
      elif int(ship[1]) < 0 or int(ship[2]) < 0 or int(ship[3]) < 0 or int(ship[4]) < 0: #catch negatively placed boats
        print('Error', ship[0], 'is', 'placed', 'outside', 'of', 'the', 'board.', 'Terminating', 'game.')
        sys.exit(0)
      else:
        for boat in boatList:
          if boat == ship[0]:
            print('Error', 'symbol', ship[0], 'is', 'already', 'in', 'use.', 'Terminating', 'game')
            sys.exit(0)
        boatList.append(ship[0])#add the boat to a boat list
        boatList2.append(ship[0])#add the boat to a second boat list
          
  board = buildYourBoard(height, width, ships)
  random.seed(seed) #seed the game
  AIboard = AIboardSetup1(height, width, ships)

  turn = random.randint(0, 1) #get turn
  gameActive = True
  placesToAttack = []
  huntAttacks = []
  hunt = [False]
  for i in range(height):
    for l in range(width):
      placesToAttack.append((i, l)) #make list of all possible attacks

  fakeAIboard = []
  for i in range(height):
    row = []
    for l in range(width):
      row.append("*")
    fakeAIboard.append(row) #make fake board

  firstTime = True
  while gameActive != False:     
    if firstTime == True and turn == 0:
      fakeAIboard = []
      for i in range(height):
        for l in range(width):
          row.append("*")
        fakeAIboard.append(row)
        row = []
      for indexY, (realRow, fakeRow) in enumerate(zip(AIboard, fakeAIboard)):
        for indexX, (real, fake) in enumerate(zip(realRow, fakeRow)):
          if real == "X":
            fakeAIboard[indexY][indexX] = "X"
          elif real == "O":
            fakeAIboard[indexY][indexX] = "O"
      print("Scanning Board")
      printBoard(fakeAIboard)
      print("My Board")
      printBoard(board)


    if turn == 0:
      gameActive = Game(board, AIboard, turn, difficulty, placesToAttack, huntAttacks, width, height, hunt, fakeAIboard, boatList)
      status = isSink(boatList, AIboard) #removed AI from board
      if status[0] == False:
        print(gameActive[1])
      elif status[0] == True:
        print("You sunk my", status[1])
      if gameNotOver(board, AIboard, turn, fakeAIboard) != False:
        turn = (turn + 1) % 2

    if turn == 1:
      gameActive = Game(board, AIboard, turn, difficulty, placesToAttack, huntAttacks, width, height, hunt, fakeAIboard, boatList)
      print("The AI fires at location", str(gameActive[2]))
      status = isSink(boatList2, board) #removed AI from board
      if status[0] == False:
        print(gameActive[1])
      elif status[0] == True:
        print("You sunk my", status[1])
      if gameNotOver(board, AIboard, turn, fakeAIboard) != False:
        turn = (turn + 1) % 2
    fakeAIboard = []
    for i in range(height):
      row = []
      for l in range(width):
        row.append("*")
      fakeAIboard.append(row)
    for indexY, (realRow, fakeRow) in enumerate(zip(AIboard, fakeAIboard)):
      for indexX, (real, fake) in enumerate(zip(realRow, fakeRow)):
        if real == "X":
          fakeAIboard[indexY][indexX] = "X"
        elif real == "O":
          fakeAIboard[indexY][indexX] = "O" 
    print("Scanning Board")
    printBoard(fakeAIboard)
    print("My Board")
    printBoard(board)
    if gameNotOver(board, AIboard, turn, fakeAIboard) == False and turn == 0:
      print("You win!")
      break
    if gameNotOver(board, AIboard, turn, fakeAIboard) == False and turn == 1:
      print("The AI wins.")
      break
    firstTime = False





#Checks to see if boat has sank
def isSink(boatList, board):
  allSpots = []
  for row in board:
    allSpots.extend(row)
  for index, ships in enumerate(boatList):
    if ships in allSpots:
      continue #if certain ship still on board check next
    else:
      sunken = boatList.pop(index) #remove the ship
      return (True, sunken) #say a ship has been sunken
  return (False, None) #ship hasnt sunken
    




#Check if game is over
def gameNotOver(board, AIboard, turn, fakeAIboard):
  if turn == 1:
    for row in board:
      for spot in row:
        if spot != "X" and spot != "O" and spot != "*": #if there is a boat still game not over
          return True
    return False #game over
                  
  if turn == 0:
    for row in AIboard:
      for spot in row:
        if spot != "X" and spot != "O" and spot != "*": #game not over if there is still a boat
          return True
    return False #game over





#Carries out the missle launching based on whose turn and edits the players boards
def Game(board, AIboard, turn, difficulty, placesToAttack, huntAttacks, width, height, hunt, fakeAIboard, boatList):
  if turn == 0:
    attack = getCoord(width, height)
    coord = attack.split(" ")
    if AIboard[int(coord[0])][int(coord[1])] == "*":
      AIboard[int(coord[0])][int(coord[1])] = "O" #if miss mark as miss
      hit = "Miss!"
    elif AIboard[int(coord[0])][int(coord[1])] == "O":
      return Game(board, AIboard, turn, difficulty, placesToAttack, huntAttacks, width, height, hunt, fakeAIboard, boatList)
    elif AIboard[int(coord[0])][int(coord[1])] == "X":
      return Game(board, AIboard, turn, difficulty, placesToAttack, huntAttacks, width, height, hunt, fakeAIboard, boatList)
    else:
      AIboard[int(coord[0])][int(coord[1])] = "X" #if  hit mark as hit
      hit = "Hit!"
    return (AIboard, hit) #return the enemy board and the type of hit

  else:
    #print(placesToAttack)
    if difficulty == 1: #if random difficulty
      attack = random.choice(placesToAttack) #get a location
      placesToAttack.remove(attack) #remove that spot
      coord = attack
      if board[int(coord[0])][int(coord[1])] == "*":
        board[int(coord[0])][int(coord[1])] = "O" #if miss make miss
        hit = "Miss!"
      else:
        board[int(coord[0])][int(coord[1])] = "X" #if hit make  hit
        hit = "Hit!"
    elif difficulty == 2: #smart AI
      if huntAttacks == []: #if no hunt locations
        coord = random.choice(placesToAttack) #get a location randomly
        placesToAttack.remove(coord)
        hunt = [False]
      else: #if places to hunt
        coord = huntAttacks.pop(0) #get first place to hunt
        if hunt[0] == False:
          placesToAttack.remove(coord) #remove it from the random list too
      if hunt[0] == False:
        new = 0
        if board[int(coord[0])][int(coord[1])] == "*":
          board[int(coord[0])][int(coord[1])] = "O" #miss if miss
          hit = "Miss!"
        else:
          board[int(coord[0])][int(coord[1])] = "X" #hit if hit
          hit = "Hit!"
          hunt = [True]
          if (int(coord[0]) - 1) >= 0: #add to hunt list if can be added 
            if (board[int(coord[0]) - 1][int(coord[1])]) != "X" and (board[int(coord[0]) - 1][int(coord[1])]) != "O":
              huntAttacks.append((int(coord[0]) - 1, int(coord[1]))) #add to hunt list if can be added
              new += 1
          
          if (int(coord[0]) + 1) < height: #add to hunt list if can be added
            if (board[int(coord[0]) + 1][int(coord[1])]) != "X" and (board[int(coord[0]) + 1][int(coord[1])]) != "O":
              huntAttacks.append((int(coord[0]) + 1, int(coord[1]))) #add to hunt list if can be added
              new += 1
          
          if (int(coord[1]) - 1) >= 0: #add to hunt list if can be added
            if (board[int(coord[0])][int(coord[1]) - 1]) != "X" and (board[int(coord[0])][int(coord[1]) - 1]) != "O":
              huntAttacks.append((int(coord[0]), int(coord[1]) - 1)) #add to hunt list if can be added
              new += 1
          
          if (int(coord[1]) + 1) < width: #add to hunt list if can be added 
            if (board[int(coord[0])][int(coord[1]) + 1]) != "X" and (board[int(coord[0])][int(coord[1]) + 1]) != "O":
              huntAttacks.append((int(coord[0]), int(coord[1]) + 1)) #add to hunt list if can be added
              new += 1

        for times in range(new): #added a 5
          for index, spot in enumerate(huntAttacks[:-1]):
            if huntAttacks[-1] == spot:
              huntAttacks.pop() #removed duplicated coord in hunt list
              break
          else:
            for index, spot in enumerate(huntAttacks[:-2]):
              if huntAttacks[-2] == spot:
                huntAttacks.pop(-2) #removed duplicated coord in hunt list
                break
            else:
              for index, spot in enumerate(huntAttacks[:-3]):
                if huntAttacks[-3] == spot:
                  huntAttacks.pop(-3) #removed duplicated coord in hunt list
                  break
              else:
                for index, spot in enumerate(huntAttacks[:-4]):
                  if huntAttacks[-4] == spot:
                    huntAttacks.pop(-4) #removed duplicated coord in hunt list
                    break

      else: #hunt true
        if board[int(huntAttacks[0][0])][int(huntAttacks[0][1])] == "*":
          board[int(huntAttacks[0][0])][int(huntAttacks[0][1])] = "O" #miss if miss
          hit = "Miss!"
        else:
          board[int(huntAttacks[0][0])][int(huntAttacks[0][1])] = "X" #hit if hit
          hit = "Hit!"
          hunt = [True]
          if (int(coord[0]) - 1) < 0:
            pass
          elif (board[int(coord[0])][int(coord[1])]) != "X": #add coord to hunt list if can  
            huntAttacks.append((int(coord[0]) - 1, int(coord[1])))
          if (int(coord[0]) + 1) > height:
            pass
          elif (board[int(coord[0]) + 1][int(coord[1])]) != "X": #add coord to hunt list if can  
            huntAttacks.append((int(coord[0]) + 1, int(coord[1])))
          
          if (int(coord[1]) - 1) < 0:
            pass
          elif (board[int(coord[0])][int(coord[1])]) != "X": #add coord to hunt list if can
            huntAttacks.append((int(coord[0]), int(coord[1]) - 1))
          if (int(coord[1]) + 1) > width:
            pass
          elif (board[int(coord[0])][int(coord[1])]) != "X": #add coord to hunt list if can
            huntAttacks.append((int(coord[0]), int(coord[1]) + 1))
                  
    if difficulty == 3: #cheater mode
      hit = "blank"
      coord = "blank"
      for y, row in enumerate(board):
        for x, spot in enumerate(row):
          if spot != "*" and spot != "X": # hit left to right top to bottem
            board[y][x] = "X"
            hit = "Hit!"
            return (board, hit, (y, x))
    return (board, hit, coord) #return the player's board and the location of the attack





#Gets ready to set up the AI's board
def AIboardSetup1(height, width, ships):
  orderedBoats = sorted(getBoats(ships)) #order the boats
  AIboats = []
  AIboard = []
  for i in range(height):
    row = []
    for l in range(width):
      row.append("*")
    AIboard.append(row)
  
  for boat in orderedBoats:
    distance = len(boat[0])
    theBoat = boat[0]
    AIboats.append((theBoat, distance)) #put the boat symbol with its lenght
  z = 0
  a = 0
  overlap = False
  return AIboardSetup2(AIboats, AIboard, width, height, overlap, z, a)





#Set up the AI's board
def AIboardSetup2(AIboats, AIboard, width, height, overlap, z , a):
  for boat in AIboats:
    if overlap == True:
      if a > 0:
        a -= 1
        continue

    direction = random.choice(['vert', 'horz'])
    i = 0
    overlap = False
    
    if direction == 'vert':
      startY = random.randint(0, height - boat[1]) #get valid height
      startX = random.randint(0, width - 1) #get valid width
      
      while i < boat[1]:
        if AIboard[startY + i][startX] != "*":
          overlap = True
          break
        i += 1
      i = 0
      while i < boat[1]:
        if overlap == True:
          break
        AIboard[startY + i][startX] = boat[0][0] #build the boat from the start
        i += 1

    elif direction == 'horz':
      startY = random.randint(0, height - 1) #get valid height
      startX = random.randint(0, width - boat[1]) # get valid width
      
      while i < boat[1]:
        if AIboard[startY][startX + i] != "*":
          overlap = True
          break
        i += 1
      i = 0
      while i < boat[1]:
        if overlap == True:
          break
        AIboard[startY][startX + i] = boat[0][0] #build the boat from the start
        i += 1
  
    if overlap == True:
      a = z
      return AIboardSetup2(AIboats, AIboard, width, height, overlap, z, a)
        
    z += 1
    if direction == 'vert':
      print("Placing ship from", str(startY) + "," + str(startX), "to", str(startY + boat[1] - 1) + "," + str(startX) + ".")
    if direction == 'horz':
      print("Placing ship from", str(startY) + "," + str(startX), "to", str(startY) + "," + str(startX + boat[1] - 1) + ".")
  return AIboard





#Breaks the boats into their components, direction length and symbol
def getBoats(ships):
  myShips = []
  for ship in ships:
    backwards = False
    if int(ship[1]) != int(ship[3]) and int(ship[2]) != int(ship[4]):
      print('Ships', 'cannot', 'be', 'placed', 'diagonally.', 'Terminating', 'game.')
      sys.exit(0) #diagonals

    elif int(ship[1]) != int(ship[3]):
      direction = "Vert"
      if int(ship[1]) < int(ship[3]):
        distance = int(ship[3]) - int(ship[1]) + 1 #get length
      elif int(ship[1]) > int(ship[3]):
        backwards = True
        distance = int(ship[1]) - int(ship[3]) + 1 #get length
        flipX1 = ship[1]
        flipX2 = ship[3]
        ship[1] = flipX2
        ship[3] = flipX1
      else:
        distance = 1
    
    elif int(ship[2]) != int(ship[4]):
      direction = "Horz"
      if int(ship[2]) < int(ship[4]):
        distance = (int(ship[4]) - int(ship[2])) + 1 #get length
      elif int(ship[2]) > int(ship[4]):
        backwards = True
        distance = (int(ship[2]) - int(ship[4])) + 1 #get length
        flipX1 = ship[2]
        flipX2 = ship[4]
        ship[2] = flipX2
        ship[4] = flipX1
      else:
        distance = 1 #get length for one unit ship
            
    elif int(ship[1]) == int(ship[3]) and int(ship[2]) == int(ship[4]):
      direction = None
      distance = 1

    shipPiece = ship[0]
    myShips.append(placeShip(shipPiece, direction, distance, ship[1], ship[2]))
  return myShips        
    




#Places ships in a format to be read
def placeShip(shipPiece, direction, distance, coord1, coord2):
  if direction == "Vert":
    ship = (shipPiece * distance) #make ship
  elif direction == "Horz":
    ship = (shipPiece * distance) #make ship
  else:
    ship = (shipPiece * distance) #make ship
  theShip = [ship, direction, (coord1, coord2)]
  return theShip
    




#Gets valid seed
def getSeed():
  while True:
    try:
      seed = int(input("Enter the seed: "))
      return seed
    except ValueError:
      continue





#Gets valid width
def getWidth():
  while True:
    try:
      num = int(input("Enter the width of the board: "))
      if num <= 0:
        raise ValueError
      return num
    
    except ValueError:
      continue
    except ZeroDivisionError:
      continue





#Gets valid height
def getHeight():
  while True:
    try:
      num = int(input("Enter the height of the board: "))
      if num <= 0:
        raise ValueError
      return num
    except ValueError:
      continue
    except ZeroDivisionError:
      continue





#Gets the game difficulty
def getDifficulty():
  while True:
    print("Choose your AI.\n1. Random\n2. Smart\n3. Cheater")
    try:
      num = int(input("Your choice: "))
      if num > 3 or num < 1:
        raise ValueError
      return num
    except ValueError:
      continue
    except ZeroDivisionError:
      continue





#Gets valid coordinates
def getCoord(width, height):
  while True:
    try:
      num = (input("Enter row and column to fire on separated by a space: "))
      num = num.strip(" ")
      num2 = num.split(" ")
      if len(num2) != 2:
        raise ValueError
      elif int(num2[0]) > (height - 1):
        raise ValueError
      elif int(num2[1]) > (width - 1):
        raise ValueError
      return num
    except ValueError:
      continue





#Builds the player board
def buildYourBoard(height, width, ships):
  myShips = getBoats(ships)
  board = []
  for i in range(height):
    row = []
    for l in range(width):
      row.append("*")
    board.append(row)
  for ship in myShips:
    if ship[1] == "Horz" or ship[1] == None:
      i = 0
      while i < len(ship[0]):
        try:
          if board[int(ship[2][0])][int(ship[2][1]) + i] != "*":
            print('There', 'is', 'already', 'a', 'ship', 'at', 'location', str(int(ship[2][0])) + ", " + str(int(ship[2][1]) + 1) + '.', 'Terminating', 'game.')
            sys.exit(0)
          board[int(ship[2][0])][int(ship[2][1]) + i] = ship[0][0] #build ship from the start
          i +=1
        except IndexError:
          print('Error', ship[0][0], 'is', 'placed', 'outside', 'of', 'the', 'board.', 'Terminating', 'game.')
          sys.exit(0)
    if ship[1] == "Vert":
      i = 0
      while i < len(ship[0]):
        try:
          if board[int(ship[2][0]) + i][int(ship[2][1])] != "*":
            print('There', 'is', 'already', 'a', 'ship', 'at', 'location', str(int(ship[2][0]) + i) + ", " + str(int(ship[2][1])) + '.', 'Terminating', 'game.')
            sys.exit(0)
          board[int(ship[2][0]) + i][int(ship[2][1])] = ship[0][0] #build  the ship from the start
          i +=1
        except IndexError:
          print('Error', ship[0][0], 'is', 'placed', 'outside', 'of', 'the', 'board.', 'Terminating', 'game.')
          sys.exit(0)
    
  return board





#Prints the board
def printBoard(board):
  i = 0
  print("  ", end = "")
  for number in range(len(board[0])):
    print(number, end = " ") #make coords of board
  print("")
  for row in board:
    print(i, end = " ") #make coords of board
    for column in row:
      print(column, end = " ")
    print("")
    i += 1





setup() #call the game
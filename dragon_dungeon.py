from IPython.display import clear_output
from random import randint, choice

class DragonDungeon():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def showGrid(self, player, dragon, door):
        p_coords = player.getCoords()
        dragon_coords = dragon.getCoords()
        d_coords = door.getCoords()
        # how would I instantiate a number of chests automatically based on level number?
        # I'd like to have multiple chests containing random items, including a key needed
        # to unlock the door.
        # chest_coords = [chest.getCoords for chest in chests]

        print(f'Player Coords: {p_coords} \t Lives: {player.getLives()}')
        print(f'Dragon Coords: {dragon_coords}')
        print(f'Door Coords: {d_coords}')

        for row in range(self.rows):
            print('+------' * self.cols + '+')
            for col in range(self.cols):
                if p_coords == [col, row] and col == self.cols - 1:
                    print('|  :)  ', end='|\n')
                elif p_coords == [col, row]:
                    print('|  :)  ', end='')
                elif dragon_coords == [col, row] and col == self.cols - 1:
                    print('| (&)~ ', end='|\n')
                elif dragon_coords == [col, row]:
                    print('| (&)~ ', end='')
                elif d_coords == [col, row] and col == self.cols - 1:
                    print('|[EXIT]', end='|\n')
                elif d_coords == [col, row]:
                    print('|[EXIT]', end='')
                elif col == self.cols - 1:
                    print('|      ', end='|\n')
                else:
                    print('|      ', end='')

            # print bottom border of grid
            if row == self.rows - 1:
                print('+------' * self.cols + '+')

    def checkCollision(self, ob1, ob2):
        return True if ob1.getCoords() == ob2.getCoords() else False

    def handleLoseCondition(self, player):
        if player.getLives() <= 0:
            print('You dead.')
            return True
        return False

    def increaseGridSize(self, row_increase, col_increase):
        self.rows += row_increase
        self.cols += col_increase

class Character():
    def __init__(self, name, lives=3, coords=[0,0]):
        self.name = name
        self.lives = lives
        self.coords = coords

    def getCoords(self):
        return self.coords

    def loseLife(self):
        self.lives -= 1

    def getLives(self):
        return self.lives

    def moveDragon(self, rows, cols):
        # possible moves for dragon
        moves = ['left', 'right', 'up', 'down', 'teleport']
        # select dragon movement at random:
        ans = choice(moves)

        if ans == 'left' and self.coords[0] > 0:
            self.coords[0] -= 1
        elif ans == 'right' and self.coords[0] < cols - 1:
            self.coords[0] += 1 # test moving right
        elif ans == 'up' and self.coords[1] > 0:
            self.coords[1] -= 1
        elif ans == 'down' and self.coords[1] < rows - 1:
            self.coords[1] += 1
        elif ans == 'teleport':
            # teleport!!!!!!!!
            self.coords = [randint(0, cols - 1), randint(0, rows - 1)]
        else:
            pass

    def movePlayer(self):
        '''
            Loop to ask user to move object, handle anything
        '''


        moved = False

        while not moved:
            print("Type 'q' at any time to quit playing...")
            ans = input('Where would you like to move? (left/right/up/down)? ').lower()

            if ans == 'q':
                return True
            elif ans == 'left' and self.coords[0] > 0:
                self.coords[0] -= 1
                moved = True
            elif ans == 'right' and self.coords[0] < cols - 1:
                self.coords[0] += 1
                moved = True
            elif ans == 'up' and self.coords[1] > 0:
                self.coords[1] -= 1
                moved = True
            elif ans == 'down' and self.coords[1] < rows - 1:
                self.coords[1] += 1
                moved = True
            else:
                print("Invalid move. Try again.")

        return False

# define global game variables
level = 0
lives = 3
rows = 5 + level
cols = 5 + level
done = False
won = False

while not done:
    game = DragonDungeon(rows, cols)
    player = Character('Player', lives, [0, 0])
    dragon = Character('Dragon', lives=0, coords=[2, 2])
    door = Character('Door', lives=0, coords=[4, 4])
    playing = True

    while playing:

        game.showGrid(player, dragon, door)

        # handle user movement
        if player.movePlayer() == True:
            playing = False
            done = True


        # handle dragon movement
        dragon.moveDragon(rows, cols)


        clear_output()

        # check for and handle collisions
        if game.checkCollision(player, door):
            # winning condition
            print('Congrats! You beat the level!')
            playing = False
            won = True

        elif game.checkCollision(player, dragon):
            # player loses life
            player.loseLife()
            print('You\'re dragon food.')

            # check if the game is over, handle lose condition if game is over
            if game.handleLoseCondition(player):
                playing = False

    if not done:
        # ask if they would like to keep playing, and increment the level if they won.
        if won and input("Would you like to play the next level (y/n)? ").lower() == 'y':
            level += 1
            rows, cols = rows + level, cols + level
        elif not won and input('Would you like to try again (y/n)'):
            continue
            # TODO: add method to reset all game variables

    else:
        clear_output()
        print("Thanks for playing!")
        done = True

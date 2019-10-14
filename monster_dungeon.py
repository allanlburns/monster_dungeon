from IPython.display import clear_output
from random import randint

class MonsterDungeon():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def showGrid(self, player, monster, door):
        p_coords = player.getCoords()
        m_coords = monster.getCoords()
        d_coords = door.getCoords()

        print(f'Player Coords: {p_coords} \t Lives: {player.getLives()}')
        print(f'Player Coords: {m_coords}')
        print(f'Player Coords: {d_coords}')

        for row in range(self.rows):
            print('+---' * self.cols + '+')
            for col in range(self.cols):
                if p_coords == [col, row] and col == self.cols - 1:
                    print('| p ', end='|\n')
                elif p_coords == [col, row]:
                    print('| p ', end='')
                elif m_coords == [col, row] and col == self.cols - 1:
                    print('| m ', end='|\n')
                elif m_coords == [col, row]:
                    print('| m ', end='')
                elif d_coords == [col, row] and col == self.cols - 1:
                    print('| d ', end='|\n')
                elif d_coords == [col, row]:
                    print('| d ', end='')
                elif col == self.cols - 1:
                    print('|   ', end='|\n')
                else:
                    print('|   ', end='')

            # print bottom border of grid
            if row == self.rows - 1:
                print('+---' * self.cols + '+')

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

    def moveMonster(self, rows, cols):
        self.coords = [randint(0, cols - 1), randint(0, rows - 1)]

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
            elif ans == 'left':
                self.coords[0] -= 1
                moved = True
            elif ans == 'right':
                self.coords[0] += 1
                moved = True
            elif ans == 'up':
                self.coords[1] -= 1
                moved = True
            elif ans == 'down':
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
    game = MonsterDungeon(rows, cols)
    player = Character('Player', lives, [0, 0])
    monster = Character('Monster', lives=0, coords=[2, 2])
    door = Character('Door', lives=0, coords=[4, 4])
    playing = True

    while playing:

        game.showGrid(player, monster, door)

        # handle user movement

        if player.movePlayer() == True:
            playing = False
            done = True


        # handle monster movement

        monster.moveMonster(rows, cols)


        clear_output()

        # check for and handle collisions
        if game.checkCollision(player, door):
            # winning condition
            print('Congrats! You beat the level!')
            playing = False
            won = True

        elif game.checkCollision(player, monster):
            # player loses life
            player.loseLife()
            print('You got eaten by the monster.')

            # check if the game is over, handle lose condition if game is over
            if game.handleLoseCondition(player):
                playing = False

    if not done:
        # ask if they would like to keep playing, and increment the level if they won.
        if won and input("Would you like ot play the next level (y/n)? ").lower() == 'y':
            level += 1
            rows, cols = rows + level, cols + level
        elif not won and input('Woould you like to try again (y/n)'):
            continue
            # TODO: add method to reset all game variables

    else:
        clear_output()
        print("Thanks for playing!")
        done = True

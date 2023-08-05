'''Console spider in Python: for running a game import modulo named "spider" andin your python file print Spider(),
   In argument place number of suits in game (default 4)

How to play:
   1. For a move print two numbers of columns
      (number of column where element(s) that you want to move is(are)
       and column where you want to put elements) (ex. 3 4 - put element(s) from 3 to 4 column)
    Remark: if you want to put element(s) to an empty cell, you will be asked how many elements you need to put
   2. Numbers of columns are printed over the columns
    Remark: column under the number 0 is 10-th column (print 10 to move elements from or to it)
   3. Print "take" to take extra cards (number of extra cards is placed on the left bottom)
   4. Print "undo" to undo your move
About author:
   Author: oleksiysaurin
   Author email: oleksiy.saurin@gmail.com
   Help author: PrivatBank 5169360007329752, MonoBank 5375411502082410
'''


import random
from termcolor import colored
from copy import deepcopy


class _List(list):

    def __contains__(self, item):
        if type(item) in (list, tuple):
            for n in range(len(list(self))):
                if list(self)[n] == item[0]:
                    if all(item[i] == list(self)[n + i] for i in range(len(item))):
                        return True
            return False
        elif item in list(self):
            return True
        else:
            return False


class _E:

    def __init__(self, name, color='blue'):
        self.r = str(name)
        self.opened = False
        self.color = color

    def copy(self):
        return _E(self.r, self.color)

    def __eq__(self, other):
        return self.r == other.r

    def __repr__(self):
        return colored(self.r, f'{self.color}')


class Spider:
    deck = _List([_E('K'), _E('Q'), _E('J'), _E(0), _E(9), _E(8), _E(7), _E(6), _E(5), _E(4), _E(3), _E(2), _E('A')])

    def __init__(self, suits=4):
        self.decks = 8
        self.cards = []
        self.colors = ['blue', 'yellow', 'red', 'green']
        for i in range(suits):
            for j in range(self.decks // suits):
                for k in self.colored_deck(self.colors[i]):
                    self.cards.append(k)
        random.shuffle(self.cards)
        self.columns = []
        self.unused_decks = []
        self.cur_cols = None
        self.create_columns()
        self.full_decks = []
        self.moves = []
        self.und = False
        self.taked_dk = []
        self.start = True
        self.play()

    def create_columns(self):
        for i in range(10):
            column = _List([])
            if i <= 3:
                for j in range(6):
                    column.append(self.cards[6 * i + j])
                    if j == 5:
                        self.cards[6 * i + j].opened = True
            else:
                for j in range(5):
                    if j == 4:
                        self.cards[24 + 5 * (i - 4) + j].opened = True
                    column.append(self.cards[24 + 5 * (i - 4) + j])

            self.columns.append(column)
        for i in range(5):
            dk = []
            for j in range(10):
                dk.append(self.cards[54 + 10 * i + j])
            self.unused_decks.append(dk)

    def play(self):
        self.playing = True
        while self.playing:
            self.print_board()
            self.move()

    def move(self):
        self.start = False
        if not self.und:
            self.moves.append(deepcopy(self.columns))
        self.moved = False
        self.und = False

        while not self.moved:
            mv = input()
            if mv == 'take':
                try:
                    self.take()
                    self.moved = True
                except IndexError:
                    print('All cards have already been taked')
            elif mv == 'undo':
                if not len(self.moves) == 1:
                    self.undo()
                    self.moved = True
                else:
                    print('There have been no moves yet')
            else:
                try:
                    mv = mv.split()
                    in_col1 = int(mv[0]) - 1
                    in_col2 = int(mv[1]) - 1
                    self.moved = True
                    self.chng(in_col1, in_col2)
                except:
                    self.moved = False
                    print('Wrong move. Try again')

    def chng(self, column1, column2):
        a = 0
        while a < len(self.columns[column1]):
            if self.columns[column1]:
                if self.columns[column2]:
                    if [self.columns[column2][-1]] + self.columns[column1][-1 - a::] in Spider.deck and len(set(b.color for b in self.columns[column1][-1-a::])) == 1:
                        self.columns[column2] += self.columns[column1][-1 - a::]
                        for i in range(a + 1):
                            self.columns[column1].pop()
                        self.reload()
                        break
                    a += 1
                else:
                    n = int(input('How many items to put in an empty cell: '))
                    if n <= len([i for i in self.columns[column1] if i.opened]) and list(self.columns[column1][-n::]) in Spider.deck and len(set(b.color for b in self.columns[column1][-n::])) == 1:
                        self.columns[column2] += self.columns[column1][-n::]
                        for i in range(n):
                            self.columns[column1].pop()
                        self.reload()
                    else:
                        self.moved = False
                        print('Wrong move. Try again')
                    break
            else:
                print('It is not possible to remove an item from an empty cell')
                self.moved = False
                break
        else:
            self.moved = False
            print('Wrong move. Try again')

    def undo(self):
        self.und = True
        if self.moves[-2] != 'taked':
            if self.moves[-2] == 'full':
                self.moves.pop(-2)
                self.full_decks.pop()
            self.moves.pop()
            self.columns = deepcopy(self.moves[-1])
        else:
            deck = self.taked_dk.copy()
            self.unused_decks.insert(0, deck)
            self.moves.pop()
            self.moves.pop()
            self.columns = deepcopy(self.moves[-1])
        self.reload()

    def reload(self):
        if len(self.full_decks) == 8:
            self.print_board()
            print('You won!')
            self.playing = False
        for i in self.columns:
            for j in range(len(i)):
                if j == len(i) - 1 and not i[j].opened:
                    i[j].opened = True
        for r in range(len(self.columns)):
            try:
                if list(Spider.deck) in self.columns[r] and len(set(a.color for a in self.columns[r][-13::])) == 1:
                    color = self.columns[r][-1].color
                    for i in range(13):
                        self.columns[r].pop()
                    self.moves.append('full')
                    self.full_decks.append(colored('K', f'{color}'))
                    self.reload()
                    break
            except:
                pass

    def take(self):
        col = self.unused_decks[0]
        self.taked_dk = col.copy()
        for i in range(10):
            self.columns[i].append(col[i])
            col[i].opened = True
        self.unused_decks.pop(0)
        self.moves.append('taked')
        self.reload()

    def print_board(self):
        print('\n')
        if self.start:
            print('About author:\n'
                      'Author: oleksiysaurin\n'
                      'Author email: oleksiy.saurin@gmail.com\n'
                      'Help author: PrivatBank 5169360007329752, MonoBank 5375411502082410\n'
                  '\n'
                  'How to play: \n'
                  '1. For a move print two numbers of columns \n'
                  '   (number of column where element(s) that you want to move is(are)\n'
                  '   and column where you want to put elements) (ex. 3 4 - put element(s) from 3 to 4 column)\n'
                     'Remark: if you want to put element(s) to an empty cell, you will be asked how many elements you need to put\n'
                  '2. Numbers of columns are printed over the columns\n'
                     'Remark: column under the number 0 is 10-th column (print 10 to move elements from or to it)\n'
                  '3. Print "take" to take extra cards (number of extra cards is placed on the left bottom)\n'
                  '4. Print "undo" to undo your move')
            print('')
        print('₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ₀')

        for j in range(max([len(i) for i in self.columns])):
            for i in range(10):
                try:
                    if self.columns[i][j].opened:
                        print(self.columns[i][j], end=' ')
                    else:
                        print('#', end=' ')
                except IndexError:
                    print(' ', end=' ')
            print('\t')

        print()
        print('# ' * len(self.unused_decks), end='  ')
        print(*self.full_decks)
        print()

    @staticmethod
    def colored_deck(clr):
        deck = _List([_E('K'), _E('Q'), _E('J'), _E(0), _E(9), _E(8), _E(7), _E(6), _E(5), _E(4), _E(3), _E(2), _E('A')])
        for i in deck:
            i.color = clr
        return deck


if '__main__' == __name__:
    Spider(1)

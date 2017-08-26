#!/usr/bin/python
from threading import Thread, Lock, Event
import curses
import curses.textpad
import time
import random
import sys
import socket
import urllib
import re

intro_str = [
    '     /\  \        /\  \     /\  \        /\  \         ___       /\  \    ',
    '     \:\  \      /::\  \    \:\  \      /::\  \       /\  \     /::\  \   ',
    '      \:\  \    /:/\:\  \    \:\  \    /:/\:\  \      \:\  \   /:/\ \  \  ',
    '      /::\  \  /::\~\:\  \   /::\  \  /::\~\:\  \     /::\__\ _\:\~\ \  \ ',
    '     /:/\:\__\/:/\:\ \:\__\ /:/\:\__\/:/\:\ \:\__\ __/:/\/__//\ \:\ \ \__\\',
    '    /:/  \/__/\:\~\:\ \/__//:/  \/__/\/_|::\/:/  //\/:/  /   \:\ \:\ \/__/',
    '   /:/  /      \:\ \:\__\ /:/  /        |:|::/  / \::/__/     \:\ \:\__\  ',
    '   \/__/        \:\ \/__/ \/__/         |:|\/__/   \:\__\      \:\/:/  /  ',
    '                 \:\__\                 |:|  |      \/__/       \::/  /   ',
    '                  \/__/                  \|__|                   \/__/    ',
]


class Blocks():
    LN_BLOCK = (
        ((0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0)),
        ((0, 0, 0, 0),
         (1, 1, 1, 1),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0)),
        ((0, 0, 0, 0),
         (1, 1, 1, 1),
         (0, 0, 0, 0),
         (0, 0, 0, 0))
    )
    L_BLOCK = (
        ((0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 1, 0),
         (0, 0, 0, 0)),
        ((0, 0, 0, 0),
         (1, 1, 1, 0),
         (1, 0, 0, 0),
         (0, 0, 0, 0)),
        ((1, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 0, 0, 0)),
        ((0, 0, 1, 0),
         (1, 1, 1, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
    )
    RL_BLOCK = (
        ((1, 0, 0, 0),
         (1, 1, 1, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 1, 0),
         (0, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 0, 0, 0)),
        ((0, 0, 0, 0),
         (1, 1, 1, 0),
         (0, 0, 1, 0),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (0, 1, 0, 0),
         (1, 1, 0, 0),
         (0, 0, 0, 0)),
    )
    S_BLOCK = (
        ((0, 0, 0, 0),
         (0, 1, 1, 0),
         (1, 1, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (0, 1, 1, 0),
         (0, 0, 1, 0),
         (0, 0, 0, 0)),
        ((0, 0, 0, 0),
         (0, 1, 1, 0),
         (1, 1, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (0, 1, 1, 0),
         (0, 0, 1, 0),
         (0, 0, 0, 0)),
    )
    RS_BLOCK = (
        ((0, 0, 0, 0),
         (1, 1, 0, 0),
         (0, 1, 1, 0),
         (0, 0, 0, 0)),
        ((0, 0, 1, 0),
         (0, 1, 1, 0),
         (0, 1, 0, 0),
         (0, 0, 0, 0)),
        ((0, 0, 0, 0),
         (1, 1, 0, 0),
         (0, 1, 1, 0),
         (0, 0, 0, 0)),
        ((0, 0, 1, 0),
         (0, 1, 1, 0),
         (0, 1, 0, 0),
         (0, 0, 0, 0)),
    )
    T_BLOCK = (
        ((1, 1, 1, 0),
         (0, 1, 0, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (1, 1, 0, 0),
         (0, 1, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (1, 1, 1, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 0, 0),
         (0, 1, 1, 0),
         (0, 1, 0, 0),
         (0, 0, 0, 0)),
    )
    SQ_BLOCK = (
        ((0, 1, 1, 0),
         (0, 1, 1, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 1, 0),
         (0, 1, 1, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 1, 0),
         (0, 1, 1, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
        ((0, 1, 1, 0),
         (0, 1, 1, 0),
         (0, 0, 0, 0),
         (0, 0, 0, 0)),
    )
    COLORS = {
        LN_BLOCK: 7,
        L_BLOCK: 2,
        RL_BLOCK: 3,
        S_BLOCK: 4,
        RS_BLOCK: 5,
        T_BLOCK: 6,
        SQ_BLOCK: 7,
    }
    IDS = {
        LN_BLOCK: 1,
        L_BLOCK: 2,
        RL_BLOCK: 3,
        S_BLOCK: 4,
        RS_BLOCK: 5,
        T_BLOCK: 6,
        SQ_BLOCK: 7,
    }
    REVIDS = {v: k for k, v in IDS.items()}


class Tetris():
    '''all the logic for a tetris game
    '''

    def __init__(self, box, stdscr, remote):
        self.playing = False
        self.paused = False
        self.remote = remote
        # graphics
        self.box = box
        self.stdscr = stdscr
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.colors = [[8 for _ in range(10)] for _ in range(20)]

        self.grid_dirty = True

        # pieces
        self.falling_piece = None
        self.holding_piece = None
        self.next_piece = list(Blocks.COLORS.keys())[random.randint(0, 6)]
        self.rot, self.fy, self.fx, self.sy = (0, 0, 0, 0)
        # lines to remove next tick
        self.toremove = []
        self.lines = 0
        # network stuff
        self.garbage = 0
        self.kills = 0
        self.lock = Lock()

    def ready(self, name):
        self.playing = True
        self.stdscr.addstr(rely(0.5) + 11, relx(0.5) + self.remote * 22 - 3,
                           name, curses.color_pair(8))

    def clear_grid(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.colors = [[8 for _ in range(10)] for _ in range(20)]
        self.fy = 0

    def new_piece(self):
        '''chooses a random new piece for the top'''
        self.falling_piece = self.next_piece
        self.next_piece = list(Blocks.COLORS.keys())[random.randint(0, 6)]
        self.rot = 0
        self.fy = -1
        self.fx = 5 - 2
        # you hit the top, reset
        if not self.check_down():
            self.kills += 1
            self.clear_grid()
        self.fy = 0

        self._shadow = []
        self._falling_set = []
        self.calc_dirty()

        if self.kills > 2:
            self.playing = False

    def calc_shadow(self):
        '''calculates where the lookahead piece should go'''
        old_fy = self.fy
        while self.check_down():
            self.fy += 1
        self.sy = self.fy
        self.fy = old_fy

        new_shadow = [(t[0] + self.sy, t[1] + self.fx)
                      for t in self.check_falling_set()]
        for y, x in (set(self._shadow) - set(new_shadow)):
            self.box.addstr(1 + y, 1 + x * 2, '  ', 8)
        self._shadow = new_shadow

    def calc_dirty(self):
        new_falling_set = [(t[0] + self.fy, t[1] + self.fx)
                           for t in self.check_falling_set()]
        for y, x in (set(self._falling_set) - set(new_falling_set)):
            self.box.addstr(1 + y, 1 + x * 2, '  ', 8)
        self._falling_set = new_falling_set
        self.calc_shadow()

    # /////////////////////// CHECK OPERATIONS  //////////////////////////////

    def check_falling_set(self):
        '''creates a set of y,x tuples that you need to check for this piece'''
        return [] if not self.falling_piece else [(y, x) for x in range(4) for y in range(4) if self.falling_piece[self.rot % 4][y][x] == 1]
        # return filter(lambda t: ,
        #         [(y, x) for x in range(4) for y in range(4)]) if self.falling_piece else []

    def check_rot(self):
        '''checks all xy tuples, can't use falling set bc rot is different'''
        for y, x in [(y, x) for x in range(4) for y in range(4)]:
            ay = self.fy + y
            ax = self.fx + x
            # not inside box OR collision
            if (self.falling_piece[(self.rot + 1) % 4][y][x] == 1
                and
                ((ax < 0 or ax >= 10) or
                 (0 <= ay < 20 and
                  0 <= ax < 10
                  and self.grid[ay][ax] == 1))):
                return False
        return True

    def check_side(self, side):
        '''check falling set to see if we can move this piece left or right'''
        for y, x in self.check_falling_set():
            ay = self.fy + y
            ax = self.fx + x + side
            # not inside box OR collision
            if (((ax < 0 or ax >= 10) or
                 (0 <= ay < 20 and
                  0 <= ax < 10
                  and self.grid[ay][ax] == 1))):
                return False
        return True

    def check_down(self):
        '''can we move this piece down?'''
        for y, x in self.check_falling_set():
            ay = self.fy + y + 1
            ax = self.fx + x
            if ((ay >= 20 or
                 (0 <= ay < 20 and
                  0 <= ax < 10
                  and self.grid[ay][ax] == 1))):
                return False
        return True

    def commit_piece(self):
        '''commit piece to grid, set lines to remove'''
        for y, x in self.check_falling_set():
            ay = self.fy + y
            ax = self.fx + x
            if (0 <= ay < 20 and
                    0 <= ax < 10):
                self.grid[ay][ax] = self.falling_piece[self.rot % 4][y][x]
                self.colors[ay][ax] = Blocks.COLORS[self.falling_piece]
        for y in range(20):
            line = True
            for x in range(10):
                if self.grid[y][x] == 0:
                    line = False
                    break
            if line:
                self.toremove.append(y)
                self.colors[y] = [1] * 10
        self.grid_dirty = True

    def hold_piece(self):
        if self.holding_piece:
            self.holding_piece, self.falling_piece = self.falling_piece, self.holding_piece
        else:
            self.holding_piece = self.falling_piece
            self.falling_piece = Blocks.COLORS.keys()[random.randint(0, 6)]
        self.calc_shadow()

    def remove_lines(self):
        '''remove the lines from grid you set last tick'''
        for y in self.toremove:
            self.colors.remove(self.colors[y])
            self.colors.insert(0, [8] * 10)
            self.grid.remove(self.grid[y])
            self.grid.insert(0, [0] * 10)
            self.lines += 1
        self.toremove = []
        self.grid_dirty = True

    def add_garbage(self):
        for y in range(1, 20):
            self.grid[y - 1] = self.grid[y]
            self.colors[y - 1] = self.colors[y]
        self.grid[-1] = [1] * 10
        self.colors[-1] = [1] * 10
        self.grid[-1][random.randint(0, 9)] = 0
        self.garbage += 1

    # /////////////////////// DRAWING TO SCREEN  /////////////////////////////

    def draw(self, iters=None):
        '''draw all grid, falling piece, and shadow'''
        if self.grid_dirty:
            self.draw_grid(self.box)
            self.grid_dirty = False

        if not self.playing:
            self.box.addstr(11, 7, "WAITING", curses.color_pair(8))

        if self.playing and self.remote != 1:
            self.draw_shadow(self.box)

        self.draw_falling_piece(self.box)
        self.draw_next_piece(self.stdscr)
        self.draw_holding_piece(self.stdscr)

        if self.paused:
            self.stdscr.addstr(rely(0.5), relx(0.5) + 12 + self.remote * 22,
                               "paused", curses.color_pair(8))
        else:
            self.stdscr.addstr(rely(0.5), relx(0.5) + 12 + self.remote * 22,
                               "lines: %i" % self.lines, curses.color_pair(8))

        self.stdscr.addstr(rely(0.5) + 1, relx(0.5) + 12 + self.remote * 22,
                           "KO'd:  %i" % self.kills, curses.color_pair(8))
        if iters:
            self.stdscr.addstr(rely(0.5) + 2, relx(0.5) + 12 + self.remote * 22,
                               ("iters:  %i" % iters).ljust(10), curses.color_pair(8))
        self.box.refresh()

    def draw_grid(self, box):
        box.box()
        for y in range(20):
            for x in range(10):
                box.addstr(1 + y, 1 + x * 2, '  ',
                           curses.color_pair(self.colors[y][x]
                                             if self.grid[y][x] == 1 else 8))

    def draw_falling_piece(self, box):
        if self.falling_piece:
            for ay, ax in self._falling_set:
                if (0 <= ay < 20 and
                        0 <= ax < 10):
                    box.addstr(1 + ay, 1 + ax * 2, '  ',
                               curses.color_pair(Blocks.COLORS[self.falling_piece]))

    def draw_next_piece(self, stdscr):
        if self.next_piece:
            for y, x in [(y, x) for x in range(4) for y in range(4)]:
                stdscr.addstr(y + rely(0.5) - 10, x * 2 + relx(0.5) + 12 + self.remote * 22, '  ',
                              curses.color_pair(Blocks.COLORS[self.next_piece]
                                                if self.next_piece[0][y][x] == 1 else 8))

    def draw_holding_piece(self, stdscr):
        if self.holding_piece:
            for y, x in [(y, x) for x in range(4) for y in range(4)]:
                stdscr.addstr(y + rely(0.5) - 5, x * 2 + relx(0.5) + 12 + self.remote * 22, '  ',
                              curses.color_pair(Blocks.COLORS[self.holding_piece]
                                                if self.holding_piece[0][y][x] == 1 else 8))

    def draw_shadow(self, box):
        if self.falling_piece is None:
            return
        for sy, sx in self._shadow:
            # if (0 <= ay < 20 and
            #     0 <= ax < 10):
            box.addstr(1 + sy, 1 + sx * 2, '[]', curses.color_pair(8))

    # /////////////////////// NETWORKING  ////////////////////////////////

    def serialize(self):
        fullgrid = [str(self.grid[i / 10][i % 10]) for i in range(200)]
        fullcolors = [str(self.colors[i / 10][i % 10]) for i in range(200)]
        for y, x in self.check_falling_set():
            fullgrid[10 * (self.fy + y) + (self.fx + x)] = str(1)
            fullcolors[10 * (self.fy + y) + (self.fx + x)
                       ] = str(Blocks.COLORS[self.falling_piece])

        return ':'.join((str(self.lines),
                         str(self.kills),
                         str(Blocks.IDS.get(self.next_piece, "n")),
                         str(Blocks.IDS.get(self.holding_piece, "n")),
                         ''.join(fullgrid),
                         ''.join(fullcolors))) + '/'

    def deserialize(self, msg):
        self.lines = int(msg[0]) if int(msg[0]) < 1000 else self.lines
        self.kills = int(msg[1]) if int(msg[1]) < 1000 else self.kills
        self.next_piece = None if msg[2] == 'n' else Blocks.REVIDS[int(msg[2])]
        self.holding_piece = None if msg[
            3] == 'n' else Blocks.REVIDS[int(msg[3])]
        self.grid = [[int(msg[4][y * 10 + x]) for x in range(10)]
                     for y in range(20)]
        self.colors = [[int(msg[5][y * 10 + x])
                        for x in range(10)] for y in range(20)]


class NetworkConnection(Thread):
    '''run the network connection on another thread'''

    def __init__(self, game, other, socket):
        Thread.__init__(self)
        self.game = game
        self.other = other
        self.socket = socket
        self.stopped = Event()

    def run(self):
        # wait for start signal
        while 1:
            if self.stopped.isSet():
                break

            msg = self.socket.recv(500)
            if msg.startswith("ready"):
                with self.other.lock:
                    self.other.ready(msg.split('/')[0].split(':')[1])
                # move to next loop
                break

            time.sleep(0.1)

        while 1:
            if self.stopped.isSet():
                break

            msg = self.socket.recv(500)
            if msg.endswith("stop"):
                with self.game.lock:
                    self.game.playing = False
                with self.other.lock:
                    self.other.playing = False
                break

            # update game with data
            with self.other.lock:
                try:
                    self.other.deserialize(msg.split('/')[0].split(':'))
                except:
                    pass

            time.sleep(0.1)


def loop(stdscr, socket):
    stdscr.nodelay(1)
    other = None

    if socket:
        box = curses.newwin(22, 22, rely(0.5) - 11, relx(0.5) - 11 - 22)
        game = Tetris(box, stdscr, -1)
        box2 = curses.newwin(22, 22, rely(0.5) - 11, relx(0.5) - 11 + 22)
        other = Tetris(box2, stdscr, 1)
        thread = NetworkConnection(game, other, socket)
        thread.daemon = True
        thread.start()
    else:
        # normal single player
        box = curses.newwin(22, 22, rely(0.5) - 11, relx(0.5) - 11)
        game = Tetris(box, stdscr, 0)

    state = 0
    iters = 0
    last_iters = 0

    while 1:
        # with game.lock:
        # wait until other person is ready as well
        # time.sleep(0.02)

        if state == 0:
            if socket:
                key = stdscr.getch()
                if key == ord(' '):
                    socket.send("ready:%s/" % name)
                    game.ready(name)

                with other.lock:
                    game.draw()
                    other.draw()
                    if game.playing and other.playing:
                        state = 1
            else:
                # go right ahead
                key = stdscr.getch()
                if key == ord(' '):
                    state = 1
                    game.ready(name)
                game.draw()

            # if ready was set here, one time action
            if state == 1:
                game.kills = 0
                if socket:
                    with other.lock:
                        other.kills = 0
                game.new_piece()
                last_update = time.time()

        if state == 1:
            dirty = False
            drop = False
            fast = False
            wait = 0.1

            key = stdscr.getch()
            if key == ord('q'):
                return
            elif key == ord('p'):
                if game.paused:
                    game.paused = False
                else:
                    game.paused = True

            if not game.paused:
                if key == ord('c'):
                    game.hold_piece()
                elif key == ord(' '):
                    game.fy = game.sy
                    dirty = True
                    drop = True
                elif key == curses.KEY_DOWN:
                    game.rot += 1
                    dirty = True
                elif key == curses.KEY_LEFT and game.check_side(-1):
                    game.fx -= 1
                    dirty = True
                elif key == curses.KEY_RIGHT and game.check_side(1):
                    game.fx += 1
                    dirty = True
                elif key == curses.KEY_UP and game.check_rot():
                    game.rot += 1
                    dirty = True

                if drop or time.time() - last_update > (0.05 if fast else wait):
                    last_update = time.time()
                    game.remove_lines()
                    if not game.check_down():
                        game.commit_piece()
                        game.new_piece()
                    game.fy += 1
                    dirty = True

                    last_iters = iters
                    iters = 0

                if dirty:
                    game.calc_dirty()

            if socket:
                pass
                # if dirty:
                #     socket.send(game.serialize())
                # with other.lock:
                #     other.draw()
                #     game.draw()
                #     # add garbage when the other gets lines
                #     for x in range(other.lines - game.garbage):
                #         game.add_garbage()
            else:
                iters += 1
                game.draw(last_iters)

            if not game.playing:
                state = 2

        # ending sequence game not playing
        if state == 2:
            state = 0
            game.playing = False
            game.clear_grid()
            try:
                other.playing = False
                other.clear_grid()
            except AttributeError:
                pass
            if socket:
                try:
                    socket.send('stop')
                except:
                    # this is okay, just means we received a signal to stop
                    # and we are just now exiting the game loop
                    # the important thing is that we are stopped
                    # OR we could set a flag that we WERE stopped and not
                    # send this
                    print('EXIT')

                thread.stopped.set()
                thread.join()
                # restart this thread
                thread = NetworkConnection(game, other, socket)
                thread.daemon = True
                thread.start()


relx = lambda frac: int(curses.COLS * frac)
rely = lambda frac: int(curses.LINES * frac)

name = sys.argv[1] if len(sys.argv) > 1 else "Player 1"
addr = sys.argv[2] if len(sys.argv) > 2 else None
port = int(sys.argv[3]) if len(sys.argv) > 3 else 8765


def get_local_ip():
    '''find your own IP but gets only local address'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    host = s.getsockname()
    s.close()
    return host


def get_public_ip():
    return tuple(re.findall("\"ip\":\"([\d\.]+)\"",
                            urllib.URLopener().open('http://jsonip.com/').read()) + [0])


def intro(stdscr):
    curses.curs_set(0)
    stdscr.border()
    x, y = relx(.5) - len(intro_str[0]) // 2, rely(.5) - len(intro_str) // 2 - 6
    m = [1] * 14 + [2] * 13 + [3] * 10 + [4] * 13 + [5] * 11 + [7] * 16
    for i in range(len(intro_str)):
        y += 1
        for j in range(len(intro_str[i])):
            c = curses.color_pair(m[j + 1] if i > 5 and i < 8 else m[j])
            stdscr.addstr(y, x + j, intro_str[i][j], c)

    win = curses.newwin(5, 5, 5, 5)
    tb = curses.textpad.Textbox(win, insert_mode=True)
    # text = tb.edit()

    stdscr.getch()
    stdscr.refresh()
    stdscr.clear()

    # cofirm info
    stdscr.border()
    x, y = relx(.5) - 20, rely(.5) - 6
    stdscr.addstr(y, x + 4, "NAME:".ljust(20) + name, curses.color_pair(1))
    stdscr.refresh()

    # ask for multiplayer or single player
    multiplayer = False
    stdscr.addstr(
        y + 7, x + 4, "(m) for MULTIPLAYER / any other key for SINGLE PLAYER ", curses.color_pair(1))
    key = stdscr.getch()
    if key == ord('m'):
        multiplayer = True
    stdscr.addstr(y + 1, x + 4, "GAMEMODE:".ljust(20) +
                  ("MULTIPLAYER" if multiplayer else "SINGLE PLAYER"), curses.color_pair(1))

    if multiplayer:
        play_multi(stdscr)
    else:
        stdscr.addstr(
            y + 7, x + 4, "(q) to quit / any key to START".ljust(60), curses.color_pair(1))
        key = stdscr.getch()
        if key == ord('q'):
            return

        stdscr.refresh()
        stdscr.clear()
        set_solid_colors()
        loop(stdscr, None)


def play_multi(stdscr):
    x, y = relx(.5) - 20, rely(.5) - 6
    try:
        stdscr.addstr(y + 2, x + 4, "PUBLIC IP:".ljust(20) +
                      "%s:%i" % get_public_ip(), curses.color_pair(1))
    except:
        stdscr.addstr(y + 2, x + 4, "PUBLIC IP:".ljust(20) +
                      "ERR: Not Found", curses.color_pair(1))
    try:
        stdscr.addstr(y + 3, x + 4, "LOCAL IP:".ljust(20) + "%s:%i" %
                      get_local_ip(), curses.color_pair(1))
    except:
        stdscr.addstr(y + 3, x + 4, "LOCAL IP:".ljust(20) +
                      "ERR: Not Found", curses.color_pair(1))

    # create socket and listen
    # taken from sSMTP server mp3
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if addr:
        # client
        stdscr.addstr(y + 7, x + 4, "(x) any key to connect to %s:%i".ljust(60) %
                      (addr, port), curses.color_pair(1))
        stdscr.getch()
        stdscr.addstr(y + 6, x + 4, "Connecting to %s:%i" %
                      (addr, port), curses.color_pair(1))
        stdscr.addstr(y + 7, x + 4, "(^c) to quit".ljust(60),
                      curses.color_pair(1))
        stdscr.refresh()
        try:
            s.connect((addr, port))
        except:
            stdscr.addstr(
                y + 6, x + 4, "Connection Failed.".ljust(60), curses.color_pair(1))
            stdscr.refresh()
            time.sleep(3)
            return

        stdscr.addstr(y + 6, x + 4, "Connected!".ljust(40),
                      curses.color_pair(1))
        stdscr.refresh()
        stdscr.clear()
        set_solid_colors()
        loop(stdscr, s)

    else:
        # server
        stdscr.addstr(
            y + 7, x + 4, "(x) any key to start server".ljust(60), curses.color_pair(1))
        stdscr.getch()
        stdscr.addstr(
            y + 6, x + 4, "Server waiting for connection.", curses.color_pair(1))
        stdscr.addstr(y + 7, x + 4, "(^c) to quit".ljust(60),
                      curses.color_pair(1))
        stdscr.refresh()
        try:
            s.bind(('', port))
            s.listen(5)
            (clientsocket, address) = s.accept()
        except:
            stdscr.addstr(
                y + 6, x + 4, "Connection Failed.".ljust(60), curses.color_pair(1))
            stdscr.refresh()
            time.sleep(3)
            return

        stdscr.addstr(y + 6, x + 4, "Connected!".ljust(40),
                      curses.color_pair(1))
        stdscr.refresh()
        stdscr.clear()
        set_solid_colors()
        loop(stdscr, clientsocket)

    # for server you need to send another socket


def set_normal_colors():
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)


def set_solid_colors():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)


def cli(stdscr):
    # curses.use_default_colors()
    set_normal_colors()
    intro(stdscr)

if __name__ == '__main__':
    stdscr = curses.wrapper(cli)

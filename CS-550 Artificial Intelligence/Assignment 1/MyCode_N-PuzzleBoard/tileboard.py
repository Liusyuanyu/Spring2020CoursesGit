import random
import copy
import math

from basicsearch_lib.board import Board

class TileBoard(Board):
    def __init__(self, n, multiple_solutions=False, force_state=None,
                 verbose=False):
        """"TileBoard(n, multiple_solutions
        Create a tile board for an n puzzle.
        
        If multipleSolutions are true, the solution need not
        have the space in the center.  This defaults to False but
        is automatically set to True when there is no middle square 
        
        force_state can be used to initialize an n puzzle to a desired
        configuration.  No error checking is done.  It is specified as
        a list with n+1 elements in it, 1:n and None in the desired order.

        verbose is a boolean for turning on debugging
        """
        
        self.verbose = verbose  # not debug state, up to you to use it
        
        self.boardsize = int(math.sqrt(n+1))
        if math.sqrt(n+1) != self.boardsize:
            raise ValueError("Bad board size\n" +
                "Must be one less than an odd perfect square 8, 24, ...")

        # initialize parent
        super().__init__(self.boardsize, self.boardsize)

        # Compute solution states
        # todo:  Set self.goals to a list of solution tuples
        # If multiple_solutions is true, None can be anywhere:
        # [(None,1,2,3,...), (1,None,2,3,...), (1,2,None,3,...)]
        # Otherwise, must be the last square:  [(1,2,3,...,None)]

        # todo:  Determine inital state and make sure that it is solvable

        # todo:  Populate the board using self.place
        #        It would be wise to track the empty square location as well
        #        as it will make action generation easier

        #Create a solution list
        tilesize = n+1
        self.goals = []
        if(multiple_solutions):
            for ind in range(tilesize):
                tile_list = list(range(1,tilesize,1))
                tile_list.insert(ind,None)
                self.goals += [tuple(tile_list.copy())]
        else:
            tile_list = list(range(1,tilesize,1))
            tile_list +=[None]
            self.goals += [tuple(tile_list.copy())]
        
        #Create a initial tileboard
        is_solvable = False
        tile_list = list(range(1,tilesize,1))
        tile_list +=[None]
        while(not is_solvable):
            random.shuffle(tile_list)
            is_solvable=self.solvable(tile_list)
        
        #Populate the board using self.place
        rows = self.get_rows()
        cols = self.get_cols()
        for row in range(rows):
            for col in range(cols):
                self.place(row, col, tile_list[row*cols+col])
        
    def solvable(self, tiles, verbose=False):
        """solvable - Determines if a puzzle is solvable

            Given a list of tiles, determine if the N-puzzle is solvable.
            You do not need to know how to do this, but the calculation
            is based on the inversion order.

            for each number in the list of tiles,
               How many following numbers are less than that one
               e.g. [13, 10, 11, 6, 5, 7, 4, 8, 1, 12, 14, 9, 3, 15, 2, None]
               Example:  Files following 9:  [3, 15, 2, None]
               Two of these are smaller than 9, so the inversion order
                   for 9 is 2

            A puzzle's inversion order is the sum of the tile inversion
            orders.  For puzzles with even numbers of rows and columns,
            the row number on which the blank resides must be added.
            Note that we need not worry about 1 as there are
            no tiles smaller than one.

            See Wolfram Mathworld for further explanation:
                http://mathworld.wolfram.com/15Puzzle.html
            and http://www.cut-the-knot.org/pythagoras/fifteen.shtml

            This lets us know if a problem can be solved.  The inversion
            order modulo 2 is invariant across moves.  This means that
            when we make a legal move, the inversion order will always
            be even or odd.  The solution state always has an even
            inversion order, so any puzzle with an odd inversion
            number cannot be solved.
        """

        inversionorder = 0
        # Make life easy, remove None
        reduced = [t for t in tiles if t is not None]
        # Loop over all but last (no tile after it)
        for idx in range(len(reduced)-1):
            value = reduced[idx]
            after = reduced[idx+1:]  # Remaining tiles
            smaller = [x for x in after if x < value]
            numtiles = len(smaller)
            inversionorder = inversionorder + numtiles
            if verbose:
                print("idx {} value {} tail {} #smaller {} sum: {}".format(
                    idx, value, after, numtiles, inversionorder))

        # Even number of rows must take the blank position into account
        if self.get_rows() % 2 == 0:
            if verbose:
                print("Even # rows, adding for position of blank")
            inversionorder = inversionorder + \
                math.floor(tiles.index(None) / self.boardsize)+1

        solvable = inversionorder % 2 == 0  # Solvable if even
        return solvable
                                
    def __hash__(self):
        "__hash__ - Hash the board state"
        
        # Convert state to a tuple and hash
        return hash(self.state_tuple())
    
    def __eq__(self, other):
        #"__eq__ - Check if objects equal:  a == b"
        # todo:  Determine if two board configurations are equivalent
        # raise NotImplementedError("Check ==")
        return self.__hash__()==hash(other)
            
    def state_tuple(self):
        return tuple([self.get(row,col) for row in range(self.get_rows()) for col in range(self.get_cols())])
#         "state_tuple - Return board state as a single tuple"
#         raise NotImplementedError(
#             "You must create a tuple based on the board state")

    def get_actions(self):
        rows = self.get_rows()
        cols = self.get_cols()
        hole=[]
        for row in range(rows):
            for col in range(cols):
                if self.get(row,col) is None:
                    hole = (row, col)
                    break
        possible_move = []
        if hole[0] -1 >= 0:
            possible_move +=[[-1,0]]
        if hole[0] +1 < rows:
            possible_move +=[[1,0]]
        if hole[1] -1 >= 0:
            possible_move +=[[0,-1]]
        if hole[1] +1 < cols:
            possible_move +=[[0,1]]
        return  possible_move
#         "Return row column offsets of where the empty tile can be moved"
#         raise NotImplementedError("Return list of valid actions")

            
    def move(self, offset):
        #Swap tiles
        hole=[]
        for row in range(self.get_rows()):
            for col in range(self.get_cols()):
                if self.get(row,col) is None:
                    hole = (row, col)
                    break
        new_hole = (hole[0]+offset[0],hole[1]+offset[1])
        
        self.place(hole[0], hole[1], self.get(new_hole[0], new_hole[1]))
        self.place(new_hole[0], new_hole[1], None)
        
        return self
#         "move - Move the empty space by [delta_row, delta_col] and return new board"
#         # Hint:  Be sure to use deepcopy
#         raise NotImplementedError("Return new TileBoard with action applied")

    
    def solved(self):
#         for goal in self.goals:
#             if self.__eq__(goal):
#                 return True
#         return False
        
        return hash(self.state_tuple()) in [hash(i) for i in self.goals]
#         "solved - Is the puzzle solved?  Returns boolean"
#         raise NotImplementedError("Puzzle in solved state?")

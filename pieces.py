import numpy as np

class Piece:
    """
    Base class for pieces on the board. 
    
    A piece holds a reference to the board, its color and its currently located cell.
    In this class, you need to implement two methods, the "evaluate()" method and the "get_valid_cells()" method.
    """
    def __init__(self, board, white):
        """
        Constructor for a piece based on provided parameters

        :param board: Reference to the board this piece is placed on
        :type board: :ref:class:`board`
        """
        self.board = board
        self.white = white
        self.cell = None



    def is_white(self):
        """
        Returns whether this piece is white

        :return: True if the piece white, False otherwise
        """
        return self.white
    
    def cell_valid_and_empty(self, cell):
        return self.board.cell_is_valid_and_empty(cell) 

    def can_enter_cell(self, cell):
        """
        Shortcut method to see if a cell on the board can be entered.
        Simply calls :py:meth:`piece_can_enter_cell <board.Board.piece_can_enter_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the provided cell can enter, False otherwise
        """
        return self.board.piece_can_enter_cell(self, cell)

    def can_hit_on_cell(self, cell):
        """
        Shortcut method to see if this piece can hit another piece on a cell.
        Simply calls :py:meth:`piece_can_hit_on_cell <board.Board.piece_can_hit_on_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the piece can hit on the provided cell, False otherwise
        """
        return self.board.piece_can_hit_on_cell(self, cell)

    def evaluate(self):
        """
        **TODO** Implement a meaningful numerical evaluation of this piece on the board.
        This evaluation happens independent of the color as later, values for white pieces will be added and values for black pieces will be substracted. 
        
        **HINT** Making this method *independent* of the pieces color is crucial to get a *symmetric* evaluation metric in the end.
         
        - The pure existance of this piece alone is worth some points. This will create an effect where the player with more pieces on the board will, in sum, get the most points assigned. 
        - Think of other criteria that would make this piece more valuable, e.g. movability or whether this piece can hit other pieces. Value them accordingly.
        
        :return: Return numerical score between -infinity and +infinity. Greater values indicate better evaluation result (more favorable).
        """
        # TODO: Implement
        # wenn die Figur andere Figuren schlagen kann, dann wird der Wert von der gegenerischen Figur dazugerechent macht das Sinn
        # falls gar kein move möglich ist keine punkte außer Figur value hinzufügen 

        pawn_value = 1
        knight_value = 3 
        bishop_value = 3
        rook_value = 5
        queen_value = 9
        king_value = 100000

        pawn_hit = 10
        knight_hit = 30
        bishop_hit = 30
        rook_hit = 50
        queen_hit = 90
        king_hit = 1000000 # hier ist nh 0 mehr als oben

        # punkte für alle meiner Figuren die noch stehen -> ------------------------------------------------------------------
        if isinstance(self, Pawn) == True:
            self.value = pawn_value
        elif isinstance(self, Knight) == True: 
            self.value = knight_value
        elif isinstance(self, Bishop) == True: 
            self.value = bishop_value
        elif isinstance(self, Rook) == True:
            self.value = rook_value
        elif isinstance(self, Queen) == True:
            self.value = queen_value
        elif isinstance(self, King) == True:
            self.value = king_value
 
        # punkte für hits gegnerischer Figuren -> ---------------------------------------------------------------------
        # white - pieces ...................................
        # if self.white == True:
        valid_cells = self.get_valid_cells()
        for cell in valid_cells:  # iterate over valid cells for given piece
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # das ist das Problem :
            # check which piece was on cell the current piece is on
            # evaluate the current board config. before placing the piece there 
            # # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            piece_in_valid_cell = self.board.get_cell(cell)   # get piece thats on the cell 
            if isinstance(piece_in_valid_cell, Pawn) == True:
                self.value += pawn_hit    
            elif isinstance(piece_in_valid_cell, Knight) == True:
                self.value += knight_hit
            elif isinstance(piece_in_valid_cell, Bishop) == True:
                self.value += bishop_hit
            elif isinstance(piece_in_valid_cell, Rook) == True:
                self.value += rook_hit
            elif isinstance(piece_in_valid_cell, Queen) == True:
                self.value += queen_hit
            elif isinstance(piece_in_valid_cell, King) == True:
                self.value += king_hit
            elif piece_in_valid_cell == None:
                continue

        # black pieces ....................................
        # if self.white == False:
        #     valid_cells = self.get_valid_cells()
        #     for cell in valid_cells:  # iterate over valid cells for given piece
        #         piece_in_valid_cell = self.board.get_cell(cell)   # get piece thats on the cell 
        #         if isinstance(piece_in_valid_cell, Pawn) == True:
        #             self.value -= pawn_hit    
        #         elif isinstance(piece_in_valid_cell, Knight) == True:
        #             self.value -= knight_hit
        #         elif isinstance(piece_in_valid_cell, Bishop) == True:
        #             self.value -= bishop_hit
        #         elif isinstance(piece_in_valid_cell, Rook) == True:
        #             self.value -= rook_hit
        #         elif isinstance(piece_in_valid_cell, Queen) == True:
        #             self.value -= queen_hit
        #         elif isinstance(piece_in_valid_cell, King) == True:
        #             self.value -= king_hit
        #         elif piece_in_valid_cell == None:
        #             continue
        

        # Punkteabzug für wenn der eigene König nicht mehr auf dem Feld steht -> ---------------
        # Moment vllt muss das doch nicht, weil bei minmax wird das schon geregelt (special case: no more moves left)
        # erster Versuch
        # count = 0
        # meine_figuren = []
        # my_pieces = self.board.iterate_cells_with_pieces(self.white)
        # for piece in my_pieces:
        #     meine_figuren.append(piece)
        # for piece in my_pieces:
        #     if isinstance(piece, King) == False: 
        #         count += 1
        #     else:
        #         continue
        # if count == len(meine_figuren):  # count sollte diesselbe länge wie meine figuren haben wenns keinen king mehr gibt
        #     self.value -= 100000000000


        # zweiter Versuch 
        # current_position = self.cell
        # opposing_pieces = self.board.iterate_cells_with_pieces(not self.white)
        # for piece in opposing_pieces:
        #     if isinstance(piece, King) == True:
        #         opposing_king_position = piece.cell
        #         # das klappt net 
        # if (current_position == opposing_king_position).all():
        #     self.value += 100000000000
            
        # pro Feld was erreichbar ist +10 Punkt -> ---------------------------------------------------------------
        self.value += (10 * len(valid_cells)) 

        # vllt noch ab reihe 4/5 kommen so 1-2 Punkte drauf für gute Position aufm Brett oder so???

        return self.value

    def get_valid_cells(self):
        """
        **TODO** Return a list of **valid** cells this piece can move into. 
        
        A cell is valid if 
          a) it is **reachable**. That is what the :py:meth:`get_reachable_cells` method is for and
          b) after a move into this cell the own king is not (or no longer) in check.

        **HINT**: Use the :py:meth:`get_reachable_cells` method of this piece to receive a list of reachable cells.
        Iterate through all of them and temporarily place the piece on this cell. Then check whether your own King (same color)
        is in check. Use the :py:meth:`is_king_check_cached` method to test for checks. If there is no check after this move, add
        this cell to the list of valid cells. After every move, restore the original board configuration. 
        
        To temporarily move a piece into a new cell, first store its old position (self.cell) in a local variable. 
        The target cell might have another piece already placed on it. 
        Use :py:meth:`get_cell <board.BoardBase.get_cell>` to retrieve that piece (or None if there was none) and store it as well. 
        Then call :py:meth:`set_cell <board.BoardBase.set_cell>` to place this piece on the target cell and test for any checks given. 
        After this, restore the original configuration by placing this piece back into its old position (call :py:meth:`set_cell <board.BoardBase.set_cell>` again)
        and place the previous piece also back into its cell. 
        
        :return: Return True 
        """
        # TODO: Implement
        valid_cells = []
        reachable_cells = self.get_reachable_cells()
        for zelle in reachable_cells:
            old_position = self.cell
            piece_on_cell_i_want_to_move_to = self.board.get_cell(zelle)  # could also be None
            self.board.set_cell(zelle, self)    # das piece was wir uns angucken auf die erste Zelle gestellt die wir ausprobieren
            if self.board.is_king_check_cached(self.white) == False:
                # macht das hier überhaupt Sinn, bitte erlösen sie mich
                if isinstance(self.cell, King) == True: # King bewegt sich nicht solange er nicht im Schach steht !!!!
                    continue
                else:
                    valid_cells.append(zelle)
            else:
                continue   # das steht hier weil hiermit Rook bei meinen evaluated moves an erster Stelle steht 
            # aber so genau versteh ich das nicht?
            # heißt das die schleife läuft ohne das nicht weiter oder wie oder was
            
            # restore original config.  # set.cell sets cell thats left behind to None
            self.board.set_cell(old_position, self)          
            if piece_on_cell_i_want_to_move_to != None:
                self.board.set_cell(zelle, piece_on_cell_i_want_to_move_to)

            
        
        return valid_cells

class Pawn(Piece):  # Bauer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanik for `pawns <https://de.wikipedia.org/wiki/Bauer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Pawns can move only forward (towards the opposing army). Depening of whether this piece is black of white, this means pawn
        can move only to higher or lower rows. Normally a pawn can only move one cell forward as long as the target cell is not occupied by any other piece. 
        If the pawn is still on its starting row, it can also dash forward and move two pieces at once (as long as the path to that cell is not blocked).
        Pawns can only hit diagonally, meaning they can hit other pieces only the are one cell forward left or one cell forward right from them. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the pawn movability mechanics. 

        **NOTE**: For all you deep chess experts: Hitting `en passant <https://de.wikipedia.org/wiki/En_passant>`_ does not need to be implemented.
        
        :return: A list of reachable cells this pawn could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        reachable_cells_white = []
        reachable_cells_black = []
        row, col = self.cell
        # WHITE PIECES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        if self.is_white() == True:
            #FORWARD ---------------------------------------------
            forward_moves = [(row + 1 , col)]    
            if row == 1:                      # Startposition checken
                if self.cell_valid_and_empty((row + 1, col)) == True:   # weg zum zweiten feld muss frei sein
                    forward_moves.append((row + 2 , col)) # add dash 
            for zelle in forward_moves:            # über mögliche forward moves iterieren und checken ob die möglich sind, wenn ja zur Liste adden
                if self.cell_valid_and_empty(zelle) == True:
                    reachable_cells_white.append(zelle)
            row += 1                          # das steht hier weil das sonst mit dem Startposition Ding gemessed hätte
            #DIAGONAL ---------------------------------------------
            diagonal_hit = [(row, col + 1), (row, col - 1)]
            for zelle in diagonal_hit:
                if self.can_hit_on_cell(zelle) == True:
                    reachable_cells_white.append(zelle)
        
            return reachable_cells_white
        
        # BLACK PIECES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        if self.is_white() == False:
            #FORWARD -------------------------------------------
            forward_moves = [(row - 1, col)]
            if row == 6:                    # Startposition checken
                if self.cell_valid_and_empty((row - 1, col)) == True:
                    forward_moves.append((row - 2, col))  # add dash
            for zelle in forward_moves:
                if self.cell_valid_and_empty(zelle) == True:
                    reachable_cells_black.append(zelle)
            row -= 1
            #DIAGONAL -------------------------------------------
            diagonal_hit = [(row, col + 1), (row, col - 1)]
            for zelle in diagonal_hit:
                if self.can_hit_on_cell(zelle) == True:
                    reachable_cells_black.append(zelle)

            return reachable_cells_black

class Rook(Piece):  # Turm
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `rooks <https://de.wikipedia.org/wiki/Turm_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Rooks can move only horizontally or vertically. They can move an arbitrary amount of cells until blocked by an own piece
        or an opposing piece (which they could hit and then being stopped).

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this rook could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        reachable_cells = []
        row , col = self.cell 
        #HORIZONTAL MOVES ---------------------------------------------------
        while True: #rechts --------- 
            col += 1
            if self.cell_valid_and_empty((row, col)) == True:  # move until theres a piece blocking the way
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:  # check which color
                reachable_cells.append((row, col))        # replace the opposing piece then stop
                break 
            else:
                break  
        row , col = self.cell                                   # stop if its the same color
        while True: #links -----------
            col -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #VERTIKAL MOVES -----------------------------------------------------
        while True: #vorne/oben -------------
            row += 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else: 
                break
        row , col = self.cell
        while True: #hinten/unten -------------
            row -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break 
            else:
                break
        
        return reachable_cells


class Knight(Piece):  # Springer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `knights <https://de.wikipedia.org/wiki/Springer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Knights can move in a special pattern. They can move two rows up or down and then one column left or right. Alternatively, they can
        move one row up or down and then two columns left or right. They are not blocked by pieces in between. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this knight could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        reachable_cells = []
        row, col = self.cell
        # wir gehen im Uhrzeigersinn 
        # starting with two straight up and one right, then one up and two right und immer so weiter 
        every_reachable_cell = [(row + 2, col + 1), (row + 1, col + 2), (row - 1, col + 2), (row - 2, col + 1), (row - 2, col - 1), (row - 1, col -2), (row + 1, col - 2), (row + 2, col - 1)]
        for zelle in every_reachable_cell:
            if self.can_enter_cell(zelle) == True:   # cell has to be either valid+empty / valid+opposing piece
                reachable_cells.append(zelle)

        return reachable_cells
    

class Bishop(Piece):  # Läufer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `bishop <https://de.wikipedia.org/wiki/L%C3%A4ufer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Bishops can move diagonally an arbitrary amount of cells until blocked.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this bishop could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        # im Uhrzeigersinn
        reachable_cells = []
        row, col = self.cell
        #RECHTSOBEN/VORNE ----------------------------------------
        while True:
            col += 1
            row += 1
            if self.cell_valid_and_empty((row, col)) == True:  # move until a piece blocks the way
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:   #check color
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #RECHTSUNTEN/HINTEN ---------------------------------------
        while True:
            col += 1
            row -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #LINKSUNTEN/HINTEN ----------------------------------------
        while True:
            col -= 1
            row -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #LINKSOBEN/VORNE ------------------------------------------
        while True:
            col -= 1
            row += 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        
        return reachable_cells

class Queen(Piece):  # Königin
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `queen <https://de.wikipedia.org/wiki/Dame_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Queens can move horizontally, vertically and diagonally an arbitrary amount of cells until blocked. They combine the movability
        of rooks and bishops. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this queen could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        # im Uhrzeigersinn
        reachable_cells = []
        row , col = self.cell
        #VERTIKAL - STRAIGHT UP -------------------------------------
        while True:
            row += 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell  # NO FUCKING WAAAAAY YX BFDIOASDIOHA
        #DIAGONAL - RECHTSOBEN -------------------------------------- #das hier geht im test schief MÖP MÖP 
        while True:
            row += 1
            col += 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #HORIZONTAL - RECHTS ----------------------------------------
        while True:
            col += 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #DIAGONAL - RECHTSUNTEN ---------------------------------------
        while True:
            row -= 1
            col += 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #VERTIKAL - STRAIGHT DOWN --------------------------------------
        while True:
            row -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #DIAGONAL - LINKSUNTEN -------------------------------------------
        while True:
            row -= 1
            col -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #HORIZONTAL - LINKS -------------------------------------------
        while True:
            col -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        row , col = self.cell
        #DIAGONAL - LINKSOBEN ----------------------------------------
        while True:
            row += 1
            col -= 1
            if self.cell_valid_and_empty((row, col)) == True:
                reachable_cells.append((row, col))
            elif self.can_hit_on_cell((row, col)) == True:
                reachable_cells.append((row, col))
                break
            else:
                break
        
        return reachable_cells
    # test sagt mir diese Implementierung ist falsch aber das ist doch genauso wie oben...

class King(Piece):  # König
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `king <https://de.wikipedia.org/wiki/K%C3%B6nig_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Kings can move horizontally, vertically and diagonally but only one piece at a time.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this king could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        # im Uhrzeigersinn
        reachable_cells = []
        row, col = self.cell
        every_reachable_cell = [(row + 1, col), (row + 1, col + 1), (row, col + 1), (row - 1, col + 1), (row - 1, col), (row - 1, col - 1), (row, col - 1), (row + 1, col - 1)]
        for zelle in every_reachable_cell:
            if self.can_enter_cell(zelle) == True:
                reachable_cells.append(zelle)
        
        return reachable_cells
"""
Some of the classes will include

Spot- This class represents one block of the 8*8 grid and another optional piece.

Piece- This class is the basic building block of the system, every piece will be placed on a spot.

From class piece, we can also create other class children which include, King, Queen, Knight and Bishop. 
These are the abtract operations in the game.

Board- The class board is the 8*8 of the boxes containing all the active chess pieces

Player- Player class represents the participants playing the game and are the ones making the game complete.

Move- This class represents the game moves containing the starting and ending spots. 
This class will also help to keep track of the player who made the move.
"""

# -*- coding: utf-8 -*-
"""
Module containing the basic class Piece, as well as a children class for each type of pieces in the chess game.
"""
# TODO: If your system does not correctly display the unicode characters of the chess game,
# set this constant (global variable) to False
USE_UNICODE = True


class Piece:
    """
    A basic class representing a piece of the chess game. It is this class which is inherited below to provide
    one class per type of piece (Pawn, Rook, etc.).

    Attributes:
        color (str): The color of the piece, either 'white' or 'black'.
        can_jump (bool): Whether or not the piece can "jump" over other pieces on a chessboard.

    Args:
        color (str): The color with which to create the piece.
        can_jump (bool): The value with which the attribute can_jump must be initialized.

    """
    def __init__(self, color, can_jump):
        # Validation if the received color is valid.
        assert color in ('white', 'black')

        # Creation of the attributes with the received values.
        self.color = color
        self.can_jump = can_jump

    def is_white(self):
        """
        Returns whether or not the piece is white.

        Returns:
            bool: True if the piece is white, and False else.

        """
        return self.color == 'white'

    def is_black(self):
        """
        Returns whether or not the piece is black.

        Returns:
            bool: True if the piece is black, and False else.

        """
        return self.color == 'black'

    def can_move_to(self, source_position, target_position):
        """
        Checks whether, according to the rules of chess, the piece can move from one position to another.

        A position is a two-character string.
            The first character is a letter between a and h, representing the column of the chessboard.
            The second character is a number between 1 and 8, representing the row of the chessboard.

        Args:
            source_position (str): The source position, following the above format. For example, 'a8', 'f3', etc.
            target_position (str): The target position, following the above format. For example, 'b6', 'h1', etc.

        Warning:
            Since we are in the basic class and not in one of the children's classes, we don't know
            (yet) how this piece moves. This method is thus to be redefined in each of the
            children's classes.

        Warning:
            As the Piece class is independent of the chessboard (and therefore we don't know if a piece is "in the
            path"), we must ignore the content of the chessboard: we concentrate only on the rules of movement
            of the pieces.

        Returns:
            bool: True if the move is valid following the rules of the piece, and False otherwise.

        """
        # An exception is thrown (more on this later) indicating that this code has not been implemented. Do not touch
        # to this method: reimplement it in children's classes!
        raise NotImplementedError

    def can_make_a_takeover_to(self, source_position, target_position):
        """
        Checks whether, according to the rules of chess, the piece can "eat" (make a takeover) an enemy piece.
        For most pieces the rule is the same, so the method can_move_to is called.
        If this is not the case for a certain piece, we can simply redefine this method to program
        the rule.

        Args:
            source_position (str): The source position, following the above format. For example, 'a8', 'f3', etc.
            target_position (str): The target position, following the above format. For example, 'b6', 'h1', etc.

        Returns:
            bool: True if the takover is valid following the rules of the piece, and False otherwise.

        """
        return self.can_move_to(source_position, target_position)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_to(self, source_position, target_position):
        source_column, target_column = ord(source_position[0]), ord(target_position[0])
        source_row, target_row = int(source_position[1]), int(target_position[1])

        # A pawn moves on the same column.
        if target_column != source_column:
            return False

        """
        If the pawn has never moved, it may move two squares. Otherwise, only one square.
        Note that this is the only place where we refer to the size of the chessboard.
        To make our classes of pieces truly independent of this size, we could
        for example add an attribute n_deplacements, which will be incremented if the piece 
        moves.
        """
        difference = source_row - target_row
        if self.is_white():
            if source_row == 2:
                return difference in (-1, -2)
            else:
                return difference == -1

        else:
            if source_row == 7:
                return difference in (1, 2)
            else:
                return difference == 1

    def can_make_a_takeover_to(self, source_position, target_position):
        source_column, target_position = ord(source_position[0]), ord(target_position[0])
        source_row, target_row = int(source_position[1]), int(target_position[1])

        # Le pion fait une prise en diagonale, d'une case seulement, et la direction dépend
        # de sa couleur.
        if target_position not in (source_column - 1, source_column + 1):
            return False

        if self.is_white():
            return target_row == source_row + 1

        else:
            return target_row == source_row - 1

    def __repr__(self):
        """
        Redefines how a pawn is displayed on the screen. We use the constant USE_UNICODE
        to determine how to display the pawn.

        Returns:
            str: The string representing the pawn.

        """
        if self.is_white():
            if USE_UNICODE:
                return '\u2659'
            else:
                return 'PB'
        else:
            if USE_UNICODE:
                return '\u265f'
            else:
                return 'PN'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_to(self, source_position, target_position):
        source_column, target_column = source_position[0], target_position[0]
        source_row, target_row = source_position[1], target_position[1]

        # A rook moves on the same row or line, regardless of direction
        if target_column != source_column and source_row != target_row:
            return False

        # On the other hand, it cannot stay there.
        if source_column == target_column and source_row == target_row:
            return False

        return True

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2656'
            else:
                return 'TB'
        else:
            if USE_UNICODE:
                return '\u265c'
            else:
                return 'TN'


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, True)

    def can_move_to(self, source_position, target_position):
        source_column, target_column = ord(source_position[0]), ord(target_position[0])
        source_row, target_row = int(source_position[1]), int(target_position[1])

        # Un cavalier se déplace en "L", alors l'une de ses coordonnées soit varier de 1, et l'autre de 2.
        column_distance = abs(source_position - target_position)
        row_distance = abs(source_row - target_row)

        if column_distance == 1 and row_distance == 2:
            return True

        if column_distance == 2 and row_distance == 1:
            return True

        return False

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2658'
            else:
                return 'CB'
        else:
            if USE_UNICODE:
                return '\u265e'
            else:
                return 'CN'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_to(self, source_position, target_position):
        # A bishop moves diagonally, i.e. the distance between rows and columns must be the same.
        source_column, target_column = ord(source_position[0]), ord(target_position[0])
        source_row, target_row = int(source_position[1]), int(target_position[1])

        if abs(source_column - target_column) != abs(source_row - target_row):
            return False

        # On the other hand, he can't do a sur-place.
        if source_column == target_column and source_row == target_row:
            return False

        return True

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2657'
            else:
                return 'FB'
        else:
            if USE_UNICODE:
                return '\u265d'
            else:
                return 'FN'


class King(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_to(self, source_position, target_position):
        #A king can move one square, on a line, row or column.
        source_column, target_column = ord(source_position[0]), ord(target_position[0])
        source_row, target_row = int(source_position[1]), int(target_position[1])

        column_distance = abs(source_column - target_column)
        row_distance = abs(source_row - target_row)

        if row_distance != 1 and column_distance != 1:
            return False

        return True

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2654'
            else:
                return 'RB'
        else:
            if USE_UNICODE:
                return '\u265a'
            else:
                return 'RN'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_to(self, source_position, target_position):
        # A move for a queen is valid if she moves in a row, column or diagonal.
        # Note that we use the methods directly from a class, passing as first
        # argument the current object (self). It would have been "cleaner" to create new functions
        # common to Tower, Bishop and Queen classes to avoid making these calls from the class.
        return Rook.can_move_to(self, source_position, target_position) or \
            Rook.can_move_to(self, source_position, target_position)

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2655'
            else:
                return 'DB'
        else:
            if USE_UNICODE:
                return '\u265b'
            else:
                return 'DN'

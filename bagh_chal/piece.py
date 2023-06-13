import pygame


class Piece:
    def __init__(self):
        pass

    def get_all_valid_moves(self, board, previous_circle, circle):
        if board.turn == "g":
            correct_moves = self.get_valid_moves(board, previous_circle, circle)
            extra_correct_moves = []
            correct_intermediate_moves = []
        elif board.turn == "t":
            correct_moves = self.get_valid_moves(board, previous_circle, circle)
            (
                extra_correct_moves,
                correct_intermediate_moves,
            ) = self.get_extra_valid_moves(
                correct_moves,
                board,
                previous_circle,
            )
        return correct_moves, extra_correct_moves, correct_intermediate_moves

    def move(selected_piece, previous_circle, next_circle, board_config):
        previous_circle.occupying_piece = None
        next_circle.occupyibg_piece = selected_piece
        # now update the board
        if selected_piece.notation == "t":
            # if next_circle in selected_piece.goat_neighbour_and_extra_valid_move
            selected_piece.check_and_kill(previous_circle, next_circle)

    def goat_cascade(
        self,
        previous_circle,
        moved_circle,
        goat_circles,
        board,
    ):
        for goat_circle in goat_circles:
            if previous_circle.x == moved_circle.x == goat_circle.x:
                self.do_this(goat_circle, board)

            elif previous_circle.y == moved_circle.y == goat_circle.y:
                self.do_this(goat_circle, board)

            elif (previous_circle.x + 1, previous_circle.y + 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x + 1, goat_circle.y + 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)

            elif (previous_circle.x - 1, previous_circle.y - 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x - 1, goat_circle.y - 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)

            elif (previous_circle.x + 1, previous_circle.y - 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x + 1, goat_circle.y - 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)

            elif (previous_circle.x - 1, previous_circle.y + 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x - 1, goat_circle.y + 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)

    def do_this(self, goat_circle, board):
        board.goat_group.remove(goat_circle.circle.occupying_piece)
        goat_circle.circle.occupying_piece = None
        board.board_config[goat_circle.x][goat_circle.y].piece = None
        # board.goats -= 1
        board.goats_killed += 1

    def get_valid_moves(self, board, previous_circle, circle):
        for position in board.restricted_positions:
            if (previous_circle.x, previous_circle.y) == position.position:
                valid_moves = position.valid_neighbours

        for position in board.unrestricted_positions:
            if (previous_circle.x, previous_circle.y) == position.position:
                valid_moves = position.valid_neighbours

        return valid_moves

    def get_extra_valid_moves(self, valid_positions, board, previous_circle):
        extra_valid_moves = []

        intermediate_positions = set()  # position will be "killable" goats
        for valid_position in valid_positions:
            if valid_position.piece and valid_position.piece.notation == "g":
                valid_for_goat = [
                    valid_neighbour
                    for valid_neighbour in valid_position.valid_neighbours
                    if valid_neighbour.piece == None
                ]

                self.check_for_intermediate_positions(
                    board,
                    valid_for_goat,
                    intermediate_positions,
                    valid_position,
                    previous_circle,
                    extra_valid_moves,
                    valid_positions,
                )

        return extra_valid_moves, intermediate_positions

    def check_for_intermediate_positions(
        self,
        board,
        valid_for_goat,
        intermediate_positions,
        valid_position,
        previous_circle,
        extra_valid_moves,
        valid_positions,
    ):
        for position in valid_for_goat:
            if position.x == previous_circle.x == valid_position.x:
                extra_valid_moves.append(position)
                intermediate_positions.add(valid_position)

            elif position.y == previous_circle.y == valid_position.y:
                extra_valid_moves.append(position)
                intermediate_positions.add(valid_position)

            elif (previous_circle.x + 1, previous_circle.y + 1) == (
                valid_position.position
            ) and (valid_position.x + 1, valid_position.y + 1) == (position.position):
                extra_valid_moves.append(position)
                intermediate_positions.add(valid_position)
            elif (previous_circle.x - 1, previous_circle.y - 1) == (
                valid_position.position
            ) and (valid_position.x - 1, valid_position.y - 1) == (position.position):
                extra_valid_moves.append(position)
                intermediate_positions.add(valid_position)
            elif (previous_circle.x + 1, previous_circle.y - 1) == (
                valid_position.position
            ) and (valid_position.x + 1, valid_position.y - 1) == (position.position):
                extra_valid_moves.append(position)
                intermediate_positions.add(valid_position)
            elif (previous_circle.x - 1, previous_circle.y + 1) == (
                valid_position.position
            ) and (valid_position.x - 1, valid_position.y + 1) == (position.position):
                extra_valid_moves.append(position)
                intermediate_positions.add(valid_position)
        return (
            extra_valid_moves,
            intermediate_positions,
        )

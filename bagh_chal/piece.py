import pygame


class Piece:
    def __init__(self):
        pass

    def move(
        self,
        board,
        circle,
        window,
        x,
        y,
        game_settings,
        previous_circle,
        Tiger,
        selected_tiger,
    ):
        (valid_moves, extra_valid_moves, intermediate_moves) = self.get_valid_moves(
            board, previous_circle, circle
        )
        valid_moves.extend(extra_valid_moves)
        if (circle.x, circle.y) in [
            valid_move.position for valid_move in valid_moves
        ] and circle.occupying_piece == None:
            board.tiger_group.remove(selected_tiger)
            board.board_config[previous_circle.x][previous_circle.y].piece = None
            previous_circle.occupying_piece = None

            tiger = Tiger(*circle.center, x, y)
            board.tiger_group.add(tiger)
            board.board_config[x][y].position = (x, y)
            board.board_config[x][y].abs_position = circle.center
            board.board_config[x][y].circle = circle
            board.board_config[x][y].piece = tiger
            circle.occupying_piece = tiger
            circle.occupying_piece = tiger
            self.goat_cascade(
                previous_circle,
                circle,
                intermediate_moves,
                board,
            )
            board.update_board(board.board_config, window)
            board.selected_piece = None
            return True

    def goat_cascade(
        self,
        previous_circle,
        moved_circle,
        goat_circles,
        board,
    ):
        for goat_circle in goat_circles:
            print("ma yaha xu")
            print(
                previous_circle.x,
                previous_circle.y,
                "\n",
                goat_circle.x,
                goat_circle.y,
                "\n",
                moved_circle.x,
                moved_circle.y,
            )
            if previous_circle.x == moved_circle.x == goat_circle.x:
                self.do_this(goat_circle, board)
                print("I have happend")
            elif previous_circle.y == moved_circle.y == goat_circle.y:
                self.do_this(goat_circle, board)
                print("I have happend")
            elif (previous_circle.x + 1, previous_circle.y + 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x + 1, goat_circle.y + 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)
                print("I have happend")
            elif (previous_circle.x - 1, previous_circle.y - 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x - 1, goat_circle.y - 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)
                print("I have happend")
            elif (previous_circle.x + 1, previous_circle.y - 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x + 1, goat_circle.y - 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)
                print("I have happend")
            elif (previous_circle.x - 1, previous_circle.y + 1) == (
                goat_circle.x,
                goat_circle.y,
            ) and (goat_circle.x - 1, goat_circle.y + 1) == (
                moved_circle.x,
                moved_circle.y,
            ):
                self.do_this(goat_circle, board)
                print("I have happend")

    def do_this(self, goat_circle, board):
        board.goat_group.remove(goat_circle.circle.occupying_piece)
        goat_circle.circle.occupying_piece = None
        board.board_config[goat_circle.x][goat_circle.y].piece = None

    def get_valid_moves(self, board, previous_circle, circle):
        for position in board.restricted_positions:
            if (previous_circle.x, previous_circle.y) == position.position:
                valid_moves = position.valid_neighbours

        for position in board.unrestricted_positions:
            if (previous_circle.x, previous_circle.y) == position.position:
                valid_moves = position.valid_neighbours
        # if the turn is still of tiger
        valid_positions = valid_moves
        extra_valid_moves = []
        # print(valid_positions)

        intermediate_positions = set()  # position will "killable" goats
        for valid_position in valid_positions:
            if valid_position.piece and valid_position.piece.notation == "g":
                valid_for_goat = [
                    valid_neighbour
                    for valid_neighbour in valid_position.valid_neighbours
                    if valid_neighbour.piece == None
                ]
                (
                    valid_positions,
                    extra_valid_moves,
                    intermediate_positions,
                ) = self.get_extra_valid_moves(
                    valid_for_goat,
                    intermediate_positions,
                    valid_position,
                    previous_circle,
                    extra_valid_moves,
                    valid_positions,
                )
                return valid_positions, extra_valid_moves, intermediate_positions

    def get_extra_valid_moves(
        self,
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
            # valid position = goat
            # position = new position
            # previous circle = tiger
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
            valid_positions,
            extra_valid_moves,
            intermediate_positions,
        )

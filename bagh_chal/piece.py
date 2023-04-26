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
    ):
        valid_moves, extra_valid_moves = self.get_valid_moves(
            board, previous_circle, circle
        )
        valid_moves = valid_moves.extend(extra_valid_moves)

        if (circle.x, circle.y) in [
            valid_move.position for valid_move in valid_moves
        ] and circle.occupying_piece == None:
            for each_tiger in board.tiger_group:
                if (each_tiger.x, each_tiger.y) == (
                    previous_circle.x,
                    previous_circle.y,
                ):
                    board.tiger_group.remove(each_tiger)
                    board.board_config[previous_circle.x][
                        previous_circle.y
                    ].piece = None
                    previous_circle.occupying_piece = None
            tiger = Tiger(*circle.center, x, y)
            board.tiger_group.add(tiger)
            board.board_config[x][y].position = (x, y)
            board.board_config[x][y].abs_position = circle.center
            board.board_config[x][y].circle = circle
            board.board_config[x][y].piece = tiger
            circle.occupying_piece = tiger
            board.update_board(board.board_config, window)
            board.selected_piece = None
            return True

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
        for valid_position in valid_positions:
            print(valid_position.piece)
            if valid_position.piece.notation == "g":
                valid_for_goat = [
                    valid_neighbour
                    for valid_neighbour in valid_position.valid_neighbours
                    if valid_neighbour.piece == None
                ]
                for position in valid_for_goat:
                    if position.x == previous_circle.x == valid_position.x:
                        extra_valid_moves.append(position)
                    elif position.y == previous_circle.y == valid_position.y:
                        extra_valid_moves.append(position)
                    # valid position = goat
                    # position = new position
                    # previous circle = tiger
                    elif (previous_circle.x + 1, previous_circle.y + 1) == (
                        valid_position.position
                    ) and (valid_position.x + 1, valid_position.y + 1) == (
                        position.position
                    ):
                        extra_valid_moves.append(position)
                    elif (previous_circle.x - 1, previous_circle.y - 1) == (
                        valid_position.position
                    ) and (valid_position.x - 1, valid_position.y - 1) == (
                        position.position
                    ):
                        extra_valid_moves.append(position)
                    elif (previous_circle.x + 1, previous_circle.y - 1) == (
                        valid_position.position
                    ) and (valid_position.x + 1, valid_position.y - 1) == (
                        position.position
                    ):
                        extra_valid_moves.append(position)
                    elif (previous_circle.x - 1, previous_circle.y + 1) == (
                        valid_position.position
                    ) and (valid_position.x - 1, valid_position.y + 1) == (
                        position.position
                    ):
                        extra_valid_moves.append(position)

        return valid_moves, extra_valid_moves

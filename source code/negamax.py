import chess.svg
import chess.polyglot
import chess.pgn
import chess.engine
import piece_tables


class NegamaxEngine:
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth

    def evaluation(self):
        """
        evaluate current position.
        :return: node score.
        """
        if self.board.is_checkmate():
            if self.board.turn:
                return -9999
            else:
                return 9999
        if self.board.is_stalemate():
            return 0
        if self.board.is_insufficient_material():
            return 0

        # Khởi tạo giá trị đánh và các yếu tố khác như số quân được bảo vệ và số tốt thông
        material_value = 0
        protected_pieces = 0
        passed_pawns = 0

        # Tính số quân bị tấn công và số quân tốt thông
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                if piece.color:
                    if self.board.is_attacked_by(chess.BLACK, square):
                        protected_pieces -= 1
                    if piece.piece_type == chess.PAWN and not self.board.attacks(square):
                        passed_pawns -= 1
                else:
                    if self.board.is_attacked_by(chess.WHITE, square):
                        protected_pieces += 1
                    if piece.piece_type == chess.PAWN and not self.board.attacks(square):
                        passed_pawns += 1

        # Quantity of remaining pieces:
        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))
        # Piece val was: 100, 320, 330, 500, 900

        material = 100 * (wp - bp) + 300 * (wn - bn) + 330 * (wb - bb) + 550 * (wr - br)
        + 1000 * (wq - bq) + protected_pieces * 5 + passed_pawns * 30

        pawn_sq = sum([piece_tables.TABLE_PAWN_MAIN[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        pawn_sq += sum([-piece_tables.TABLE_PAWN_MAIN[chess.square_mirror(i)]
                        for i in self.board.pieces(chess.PAWN, chess.BLACK)])

        knight_sq = sum([piece_tables.TABLE_KNIGHT_MAIN[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        knight_sq += sum([-piece_tables.TABLE_KNIGHT_MAIN[chess.square_mirror(i)]
                         for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])

        bishop_sq = sum([piece_tables.TABLE_BISHOP_MAIN[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishop_sq += sum([-piece_tables.TABLE_BISHOP_MAIN[chess.square_mirror(i)]
                         for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rook_sq = sum([piece_tables.TABLE_ROOK_MAIN[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rook_sq += sum([-piece_tables.TABLE_ROOK_MAIN[chess.square_mirror(i)]
                        for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queen_sq = sum([piece_tables.TABLE_QUEEN_MAIN[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queen_sq += sum([-piece_tables.TABLE_QUEEN_MAIN[chess.square_mirror(i)]
                        for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        king_sq = sum([piece_tables.TABLE_KING_MAIN[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        king_sq += sum([-piece_tables.TABLE_KING_MAIN[chess.square_mirror(i)]
                       for i in self.board.pieces(chess.KING, chess.BLACK)])

        evaluation = material + pawn_sq + knight_sq + bishop_sq + rook_sq + queen_sq + king_sq

        return evaluation if self.board.turn else -evaluation

    def negamax(self, depth_left):
        """
        Searches the best move using NegaMax implementation of Minimax.
        :param depth_left: search depth remaining.
        :return: best score found.
        """
        if depth_left == 0:                        # If max depth or terminal node reached:
            return self.evaluation()               # Return current leaf eval.

        best_score = -9999
        for move in self.board.legal_moves:        # For every position:
            self.board.push(move)                  # Get current move
            score = -self.negamax(depth_left - 1)  # Call opponent, switching sign of return value
            self.board.pop()                       # Undo move

            best_score = max(score, best_score)    # Compare returned and existing score values, storing highest

        return best_score

    def search_controller(self):
        """
        Controls the NegaMax search.
        :return: best move found.
        """
        best_move = chess.Move.null()
        best_value = -99999                         # Set as INF (essentially)

        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = -self.negamax(self.depth - 1)

            if board_value > best_value:
                best_value = board_value
                best_move = move

            self.board.pop()

        return best_move

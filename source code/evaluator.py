import piece_tables
import constants
import chess


def evaluator(board, result):
    """
    Evaluate movement.
    :param board: board state.
    :param result: transposition table result.
    :return:
    """
    if not result == "*":                 # If entry exists and is determined:
        if result[0] == "1":              # If entry begins with 1 (player win or draw (1/2-1/2)):
            evaluation = 0 if result[1] == "/" else constants.MAX_SCORE  # If result is '1/2-1/2', eval. = 0, else MAX
        else:                             # If result doesn't begin with 1 (opponent win)
            evaluation = -constants.MAX_SCORE  # Set evaluation as negative of max_score -(100*100)
        if not board.turn:                # If not turn turn:
            evaluation = -evaluation      # Reverse evaluation
        return evaluation

    doubled_pawns = 0
    white_pawns = set({})
    white_pawn_files = [0 for i in range(8)]
    black_pawns = set({})
    black_pawn_files = [0 for i in range(8)]

    for i in range(8):
        b = 0
        w = 0
        for j in range(8):
            if str(board.piece_at(8 * j + i)) == 'P':
                white_pawn_files[i] = 1
                w += 1
                white_pawns.add(j * 8 + i)
            elif str(board.piece_at(8 * j + i)) == 'p':
                black_pawn_files[i] = 1
                black_pawns.add(j * 8 + i)
                b += 1
        if w > 1:
            doubled_pawns += w - 1
        if b > 1:
            doubled_pawns -= b - 1

    w_safe = set({})
    b_safe = set({})

    null_added = False

    if not board.turn:
        null_added = True
        board.push(chess.Move.null())

    for move in board.pseudo_legal_moves:
        if int(move.from_square) in white_pawns:
            w_safe.add(int(move.from_square))

    if null_added:
        board.pop()
        null_added = False
    else:
        board.push(chess.Move.null())
        null_added = True

    for move in board.pseudo_legal_moves:
        if int(move.from_square) in black_pawns:
            b_safe.add(int(move.from_square))
    if null_added:
        board.pop()

    blocked_pawns = len(white_pawns) - len(w_safe) - (len(black_pawns) - len(b_safe))

    isolated_pawns = 0

    for pawn in white_pawns:
        file = chess.square_file(pawn)
        iso = 0
        if file > 0:
            if white_pawn_files[file - 1] != 0:
                iso += 1

        if file < 7:
            if white_pawn_files[file + 1] != 0:
                iso += 1
        if iso == 0:
            isolated_pawns += 1

    for pawn in black_pawns:
        file = chess.square_file(pawn)
        iso = 0
        if file > 0:
            if black_pawn_files[file - 1] != 0:
                iso += 1

        if file < 7:
            if black_pawn_files[file + 1] != 0:
                iso += 1
        if iso == 0:
            isolated_pawns -= 1


    # Quantity of remaining pieces:
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 300 * (wn - bn) + 330 * (wb - bb) + 550 * (wr - br) + 1000 * (wq - bq)

    pawn_sq = sum([piece_tables.TABLE_PAWN_MAIN[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawn_sq += sum([-piece_tables.TABLE_PAWN_MAIN[chess.square_mirror(i)]
                    for i in board.pieces(chess.PAWN, chess.BLACK)])
    knight_sq = sum([piece_tables.TABLE_KNIGHT_MAIN[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knight_sq += sum([-piece_tables.TABLE_KNIGHT_MAIN[chess.square_mirror(i)]
                      for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishop_sq = sum([piece_tables.TABLE_BISHOP_MAIN[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishop_sq += sum([-piece_tables.TABLE_BISHOP_MAIN[chess.square_mirror(i)]
                      for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rook_sq = sum([piece_tables.TABLE_ROOK_MAIN[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rook_sq += sum([-piece_tables.TABLE_ROOK_MAIN[chess.square_mirror(i)]
                    for i in board.pieces(chess.ROOK, chess.BLACK)])
    queen_sq = sum([piece_tables.TABLE_QUEEN_MAIN[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queen_sq += sum([-piece_tables.TABLE_QUEEN_MAIN[chess.square_mirror(i)]
                     for i in board.pieces(chess.QUEEN, chess.BLACK)])
    king_sq = sum([piece_tables.TABLE_KING_MAIN[i] for i in board.pieces(chess.KING, chess.WHITE)])
    king_sq += sum([-piece_tables.TABLE_KING_MAIN[chess.square_mirror(i)]
                    for i in board.pieces(chess.KING, chess.BLACK)])
    score_mobility = board.legal_moves.count()
    board.push(chess.Move.null())
    score_mobility -= board.legal_moves.count()
    board.pop()

    if not board.turn:
        score_mobility *= -1

    castling_score = 0;
    # Add castling evaluation
    if board.has_kingside_castling_rights(chess.WHITE):
        castling_score += 80
    if board.has_queenside_castling_rights(chess.WHITE):
        castling_score += 80
    if board.has_kingside_castling_rights(chess.BLACK):
        castling_score -= 80
    if board.has_queenside_castling_rights(chess.BLACK):
        castling_score -= 80

    material_score = material + pawn_sq + knight_sq + bishop_sq + rook_sq + queen_sq + king_sq
    evaluation = castling_score +score_mobility + \
            material_score + \
            - 15 * (doubled_pawns + 0.5 * isolated_pawns + 0.5 * blocked_pawns)
    # print(castling_score)
    # print(evaluation)
    return evaluation if board.turn else -evaluation

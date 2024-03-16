import os

WINDOW_TITLE = 'Chess'
LOGO = 'Images/logo.ico'

ALGORITHM_LIST = ['MTD(f)']
DEPTH_LIST = [2, 3, 4, 5]

# State 1: Pre-Game. GUI elements outside of in-game.
PREGAME_MENU_BAR = [['Menu', ['Start Game', ['Play as White', 'Play as Black'], 'Close Application']],
                    ['Settings', ['Change Search Depth']],
                    ['Display Settings', ['Preview Themes', 'Default Theme', 'Select Theme', 'Select Board Colours']],
                    ['Timer Settings', ['Timer Settings']]]
STATE_PREGAME = "Pre-Game - Ready!"

# State 2: In-Game. GUI elements for during gameplay
IN_GAME_MENU_BAR = [['&Menu', ['End Game']]]

STATE_PLAYER_MOVE = "In-Game - Your Move!"
STATE_ENGINE_MOVE = "In-Game - Thinking..."
START_PIECES_NUM = 16

COLOUR_LIST = ['Green', 'Wood', 'Pink', 'Black']

EXACT_SCORE = 0
LOWER_BOUND_SCORE = 1
UPPER_BOUND_SCORE = 2

# Identifiers for each chess piece
BLANK = 0
PAWN_B = 1
KNIGHT_B = 2
BISHOP_B = 3
ROOK_B = 4
KING_B = 5
QUEEN_B = 6
PAWN_W = 7
KNIGHT_W = 8
BISHOP_W = 9
ROOK_W = 10
KING_W = 11
QUEEN_W = 12

# Layout for chess_board
INIT_BOARD = [[ROOK_B, KNIGHT_B, BISHOP_B, QUEEN_B, KING_B, BISHOP_B, KNIGHT_B, ROOK_B],
              [PAWN_B, ] * 8,
              [BLANK, ] * 8,
              [BLANK, ] * 8,
              [BLANK, ] * 8,
              [BLANK, ] * 8,
              [PAWN_W, ] * 8,
              [ROOK_W, KNIGHT_W, BISHOP_W, QUEEN_W, KING_W, BISHOP_W, KNIGHT_W, ROOK_W]]

# Import chess piece images
IMG_PATH = 'Images'  # Path to images
IMG_BLANK = os.path.join(IMG_PATH, 'blank.png')
IMG_PAWN_B = os.path.join(IMG_PATH, 'b_pawn.png')
IMG_PAWN_W = os.path.join(IMG_PATH, 'w_pawn.png')
IMG_ROOK_B = os.path.join(IMG_PATH, 'b_rook.png')
IMG_ROOK_W = os.path.join(IMG_PATH, 'w_rook.png')
IMG_KNIGHT_B = os.path.join(IMG_PATH, 'b_knight.png')
IMG_KNIGHT_W = os.path.join(IMG_PATH, 'w_knight.png')
IMG_BISHOP_B = os.path.join(IMG_PATH, 'b_bishop.png')
IMG_BISHOP_W = os.path.join(IMG_PATH, 'w_bishop.png')
IMG_QUEEN_B = os.path.join(IMG_PATH, 'b_queen.png')
IMG_QUEEN_W = os.path.join(IMG_PATH, 'w_queen.png')
IMG_KING_B = os.path.join(IMG_PATH, 'b_king.png')
IMG_KING_W = os.path.join(IMG_PATH, 'w_king.png')

PIECE_IMAGES = {BISHOP_B: IMG_BISHOP_B, BISHOP_W: IMG_BISHOP_W, PAWN_B: IMG_PAWN_B, PAWN_W: IMG_PAWN_W,
                KNIGHT_B: IMG_KNIGHT_B, KNIGHT_W: IMG_KNIGHT_W, ROOK_B: IMG_ROOK_B, ROOK_W: IMG_ROOK_W,
                KING_B: IMG_KING_B, KING_W: IMG_KING_W, QUEEN_B: IMG_QUEEN_B, QUEEN_W: IMG_QUEEN_W, BLANK: IMG_BLANK}

CLICKED_LIGHT_COLOUR = '#00A35A'                # Colour if light square clicked
CLICKED_DARK_COLOUR = '#008148'                 # Colour if dark square clicked

"""game Constants"""
HIGHLIGHT_LIGHT = '#80DED9'                     # Colour to highlight potential moves - light sq
HIGHLIGHT_DARK = '#3CCDC6'                      # Colour to highlight potential moves - dark sq
STARTER_PGN = {'Event': 'Player vs Engine',   # Starting PGN tags
               'White': 'Player',
               'Black': 'Engine'}

"""evaluator Constants"""
PAWN_SCORE = 100                # Piece value a pawn
MAX_SCORE = PAWN_SCORE * 100    # Maximum score awarded in static evaluation
"""Value of each piece: (old vals shown to side)"""
PIECE_VALUE = [100,             # PAWN:   100
               300,             # KNIGHT: 400
               330,             # BISHOP: 410
               550,             # ROOK: 600
               1000,            # QUEEN: 1200
               0]               # KING: 0
PHASE_POINTS = [0, 1, 1, 2, 4, 0]

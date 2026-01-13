
import pandas as pd 
import chess 
import chess.pgn

from pathlib import Path 
import sys 
PROJECT_ROOT = Path.cwd().parent
sys.path.append(str(PROJECT_ROOT))


from src.features_engineering.encoding import encode_title, safe_int
from src.features_engineering.time_features import clock_str_to_seconds, extract_clock_from_comment, parse_time_control





# function to create the full dataset 
def df_pgn_full(pgn, ID_Game_Start: int = 0):

    ID_Game = ID_Game_Start

    rows = []

    
    while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            board = game.board()

            # Player names
            white_name = game.headers.get("White", "")
            black_name = game.headers.get("Black", "")

            # Elo
            white_elo = safe_int(game.headers.get("WhiteElo"))
            black_elo = safe_int(game.headers.get("BlackElo"))

            # Detect if Magnus plays this game
            if white_name == "Carlsen, Magnus":
                
                MagnusElo = white_elo
                OpponentName = black_name
                OpponentElo = black_elo
                OpponentTitle_raw = game.headers.get("BlackTitle", "")
            elif black_name == "Carlsen, Magnus":
               
                MagnusElo = black_elo
                OpponentName = white_name
                OpponentElo = white_elo
                OpponentTitle_raw = game.headers.get("WhiteTitle", "")
            else:
                continue

            # Time control
            TimeControl = game.headers.get("TimeControl", "Unknown")
            TimeTotal, Increment = parse_time_control(TimeControl)

            # Initial clocks
            ClockWhite = TimeTotal
            ClockBlack = TimeTotal

            # Last time spent per side
            last_white_spend = 0
            last_black_spend = 0

            node = game
            ID_move = 0

            while node.variations:
                next_node = node.variation(0)
                move = next_node.move
                turn = board.turn  # True = White plays

                ID_move += 1

                player_is_white = (turn == chess.WHITE)

                # Player name (real names, no "Opponent")
                PlayerName = white_name if player_is_white else black_name
                PlayerElo = white_elo if player_is_white else black_elo
                PlayerTitle_raw = (
                    game.headers.get("WhiteTitle", "")
                    if player_is_white
                    else game.headers.get("BlackTitle", "")
                )

                # Encode titles
                PlayerTitle = encode_title(PlayerTitle_raw)
                OpponentTitle = encode_title(OpponentTitle_raw)

                # Clocks before
                PlayerTime_before = ClockWhite if player_is_white else ClockBlack
                OpponentTime_before = ClockBlack if player_is_white else ClockWhite

                # Extract clock after move
                raw_clock = extract_clock_from_comment(next_node.comment)
                if raw_clock is not None:
                    new_clock = clock_str_to_seconds(raw_clock)
                else:
                    new_clock = PlayerTime_before

                # --- Secure clocks ---
                PlayerTime_before = PlayerTime_before or 0
                OpponentTime_before = OpponentTime_before or 0
                Increment = Increment or 0

                # Extract clock after move
                raw_clock = extract_clock_from_comment(next_node.comment)
                if raw_clock is not None:
                    new_clock = clock_str_to_seconds(raw_clock)
                else:
                    new_clock = PlayerTime_before

                # Time spend
                TimeSpent = max(0, PlayerTime_before - new_clock + Increment)

                # --- Time features ---
                TimeRatio = PlayerTime_before / (OpponentTime_before + 1)
                TimePressure = int(PlayerTime_before < 15)
                MoveTimeFraction = TimeSpent / (PlayerTime_before + 1)


                # time_spend_before = last spend by THIS player
                time_spent_before = (
                    last_white_spend if player_is_white else last_black_spend
                )

                # opponent time spent at previous move
                OpponentTimeSpend = (
                    last_black_spend if player_is_white else last_white_spend
                )

                # Update last time spent
                if player_is_white:
                    last_white_spend = TimeSpent
                else:
                    last_black_spend = TimeSpent

                # Update clocks
                if player_is_white:
                    ClockWhite = new_clock
                else:
                    ClockBlack = new_clock

                # Board BEFORE move
                FEN_before = board.fen()

                # Opponent previous-move effects
                OppIsCaptured = int(board.is_capture(move))
                OppIsCheck = int(board.gives_check(move))
                is_variant_win = 1 if board.is_variant_win() else 0
                is_variant_loss = 1 if board.is_variant_loss() else 0

                # Number of legal moves
                NumLegalMoves = sum(1 for _ in board.legal_moves)

                # Apply move
                board.push(move)
                FEN_after = board.fen()

                # --- Move types ---
                is_castling = int(board.is_castling(move))
                is_promotion = int(move.promotion is not None)
                is_en_passant = int(board.is_en_passant(move))

                # --- Phase ---
                if board.fullmove_number <= 15:
                    Phase = 0
                elif board.fullmove_number <= 40:
                    Phase = 1
                else:
                    Phase = 2




                # Row
                rows.append({
                    "ID_game": ID_Game,
                    "ID_move": ID_move,

                    "PlayerName": PlayerName,
                    "PlayerSide": int(player_is_white),
                    "PlayerElo": PlayerElo,
                    "PlayerTitle": PlayerTitle,

                    "MagnusElo": MagnusElo,
                    "OpponentElo": OpponentElo,
                    "OpponentTitle": OpponentTitle,
                    "OpponentName": OpponentName,

                    "PlayerTimeLeft": PlayerTime_before,
                    "OpponentTimeLeft": OpponentTime_before,

                    "Phase": board.fullmove_number,  # simple phase indicator

                    "TimeControl": TimeControl,
                    "TimeTotal": TimeTotal,
                    "Increment": Increment,

                    "IsVariantWin": is_variant_win,
                    "IsVariantLoss": is_variant_loss,

                    "IsCapture": OppIsCaptured,
                    "IsCheck": OppIsCheck,

                    "OppIsCaptured": OppIsCaptured,
                    "OppIsCheck": OppIsCheck,

                    "NumLegalMoves": NumLegalMoves,
                    "FEN": FEN_before,
                    "FEN_after": FEN_after,

                    "OpponentTimeSpent": OpponentTimeSpend,
                    "TimeSpent": TimeSpent,
                    "time_spent_before": time_spent_before,

                    "Phase": Phase,

                    "TimeRatio": TimeRatio,
                    "TimePressure": TimePressure,
                    "MoveTimeFraction": MoveTimeFraction,

                    "IsCastling": is_castling,
                    "IsPromotion": is_promotion,
                    "IsEnPassant": is_en_passant,
})
                

                node = next_node

            ID_Game += 1

    return pd.DataFrame(rows), ID_Game

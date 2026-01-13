from pathlib import Path
import os
import chess
import chess.svg


def download_boards(df, output_dir):
    """
    Generate chess board SVG images from FEN strings.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing at least the columns:
        - 'FEN'
        - 'ID_game'
        - 'ID_move'
    output_dir : str or Path
        Directory where SVG boards will be saved.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean existing files
    for file in output_dir.glob("*.svg"):
        file.unlink()
    print("Old board images successfully deleted.")

    # Generate boards
    for _, row in df.iterrows():
        fen = row.get("FEN")
        if fen is None:
            continue

        try:
            board = chess.Board(fen)
        except ValueError:
            # Skip invalid FENs silently
            continue

        svg_board = chess.svg.board(board)

        filename = f"game_{int(row['ID_game'])}_move_{int(row['ID_move'])}.svg"
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            f.write(svg_board)

    print(f"New board images successfully saved in {output_dir}")

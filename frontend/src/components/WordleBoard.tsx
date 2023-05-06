import React, { useState } from 'react';
import './WordleBoard.css';
import getSuggestedGuesses from '../utils/getSuggestedGuesses';
import SuggestedGuesses from "./SuggestedGuesses";
import {Word} from "../Interfaces/Word";

const BOARD_ROWS = 6;
const BOARD_COLS = 5;
const BG_COLORS = ['gray', 'yellow', 'green'];

const WordleBoard: React.FC = () => {
  const [board, setBoard] = useState<string[][]>(
    Array.from({ length: BOARD_ROWS }, () => Array(BOARD_COLS).fill(''))
  );
  const [cellBackgrounds, setCellBackgrounds] = useState<string[][]>(
    Array.from({ length: BOARD_ROWS }, () => Array(BOARD_COLS).fill(BG_COLORS[0]))
  );
  const [activeRow, setActiveRow] = useState(0);
  const [suggestions, setSuggestions] = useState<Word[]>([]);


  const handleInputChange = (row: number, col: number, value: string) => {
    if (row === activeRow) {
      const newBoard = [...board];
      newBoard[row][col] = value.toUpperCase();
      setBoard(newBoard);
    }
  };

  const handleCellClick = (row: number, col: number) => {
    if (row === activeRow) {
      const newCellBackgrounds = [...cellBackgrounds];
      const currentColorIndex = BG_COLORS.indexOf(newCellBackgrounds[row][col]);
      newCellBackgrounds[row][col] = BG_COLORS[(currentColorIndex + 1) % BG_COLORS.length];
      setCellBackgrounds(newCellBackgrounds);
    }
  };

  const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    if (activeRow < BOARD_ROWS - 1) {
      setActiveRow(activeRow + 1);
    }
    const guessData = board.slice(0, activeRow + 1).map(row => row.join(''));

    const feedbackData = cellBackgrounds.slice(0, activeRow + 1).map(row =>
      row
        .map(color => {
          if (color === 'gray') return '*';
          if (color === 'yellow') return 'y';
          if (color === 'green') return 'g';
          return '';
        })
        .join('')
    );

    const newSuggestions = await getSuggestedGuesses(guessData, feedbackData);
    setSuggestions(newSuggestions);
  };

  return (
    <div className="WordleBoard">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="WordleRowContainer">
          <div className="WordleRow">
            {row.map((letter, colIndex) => (
              <input
                key={colIndex}
                className="WordleCell"
                style={{ backgroundColor: cellBackgrounds[rowIndex][colIndex] }}
                type="text"
                maxLength={1}
                value={letter}
                onChange={(e) => handleInputChange(rowIndex, colIndex, e.target.value)}
                onClick={() => handleCellClick(rowIndex, colIndex)}
                disabled={rowIndex !== activeRow}
              />
            ))}
          </div>
          <button onClick={handleSubmit} disabled={rowIndex !== activeRow}>
            Submit
          </button>
        </div>
      ))}
      <SuggestedGuesses suggestions={suggestions} />
    </div>
  );
};

export default WordleBoard;

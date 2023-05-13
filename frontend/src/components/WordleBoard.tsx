import React, { useState, useEffect, useRef } from 'react';
import './WordleBoard.css';
import getSuggestedGuesses from '../utils/getSuggestedGuesses';
import SuggestedGuesses from "./SuggestedGuesses";
import {Word} from "../Interfaces/Word";

const BOARD_ROWS = 6;
const BOARD_COLS = 5;
const BG_COLORS = ['gray', 'yellow', 'green'];

const WordleBoard: React.FC = () => {
  const initialBoardState: string[][] = Array.from({length: 6}, () => Array(5).fill(''));
  const [board, setBoard] = useState<string[][]>(
    initialBoardState
  );
  const initialCellBackgrounds: string[][] = Array.from({ length: BOARD_ROWS }, () => Array(BOARD_COLS).fill(BG_COLORS[0]));
  const [cellBackgrounds, setCellBackgrounds] = useState<string[][]>(initialCellBackgrounds);
  const [activeRow, setActiveRow] = useState(0);
  const [suggestions, setSuggestions] = useState<Word[]>([]);

  const firstInputRef = useRef<HTMLInputElement>(null);
  const inputRefs = useRef<(HTMLInputElement | null)[][]>(
    Array.from({ length: 6 }, () => Array.from({ length: 5 }, () => null))
  );
  const [isSubmitEnabled, setIsSubmitEnabled] = useState<boolean>(false);
  const handleReset = () => {
    setBoard(initialBoardState);
    setCellBackgrounds(initialCellBackgrounds);
    setSuggestions([]);
    setActiveRow(0);
    if (firstInputRef.current) {
      firstInputRef.current.focus();
    }
  };

  useEffect(() => {
    if (firstInputRef.current) {
      firstInputRef.current.focus();
    }
  }, [suggestions]);

  useEffect(() => {
    const activeRowData = board[activeRow];
    const allCellsFilled = activeRowData.every((cell) => cell !== '');
    setIsSubmitEnabled(allCellsFilled);
  }, [board, activeRow]);

  useEffect(() => {
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        const firstEmptyCell: HTMLInputElement | null = document.querySelector('.WordleCell:empty>input');
        firstEmptyCell?.focus();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    // Cleanup
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);


  const handleInputChange = (row: number, col: number, value: string) => {
    if (row === activeRow) {
      const newBoard = [...board];
      newBoard[row][col] = value.toUpperCase();
      setBoard(newBoard);
    }

    // Move focus to the next cell if not at the end
    if (col < BOARD_COLS) {
      inputRefs.current[row][col + 1]?.focus();
    } else if (row < BOARD_ROWS) {
      inputRefs.current[row + 1][0]?.focus();
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

  const submitGuess = async () => {
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

  const handleSubmit = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    submitGuess();
  };


  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, rowIndex: number, colIndex: number) => {
    if (e.key === 'Enter') {
      submitGuess();
    } else if (e.key === 'Backspace') {
      if (isSubmitEnabled) {
        inputRefs.current[rowIndex][BOARD_COLS - 1]?.focus();
      } else if (colIndex === 1) {
        firstInputRef.current?.focus()
      } else {
        inputRefs.current[rowIndex][colIndex - 1]?.focus();
      }
      // Delete the last letter in the row and move focus to the previous cell
      setBoard((prevBoard) => {
        const newBoard = [...prevBoard];
        if (isSubmitEnabled) {
          newBoard[rowIndex][BOARD_COLS - 1] = '';
        } else {
          newBoard[rowIndex][colIndex - 1] = '';
        }
        return newBoard;
      });
    }
  };



  return (
    <div className="WordleBoard">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="WordleRowContainer">
          <div className="WordleRow">
            {row.map((letter, colIndex) => (
              <input
                key={`cell-${rowIndex}-${colIndex}`}
                className="WordleCell"
                style={{ backgroundColor: cellBackgrounds[rowIndex][colIndex] }}
                ref={rowIndex === activeRow && colIndex === 0 ? firstInputRef : (el) => (inputRefs.current[rowIndex][colIndex] = el)}
                type="text"
                maxLength={1}
                value={letter}
                onChange={(e) => handleInputChange(rowIndex, colIndex, e.target.value)}
                onClick={() => handleCellClick(rowIndex, colIndex)}
                onMouseDown={(e) => e.preventDefault()}
                onSelect={(e) => e.preventDefault()}
                disabled={rowIndex !== activeRow}
                onKeyDown={(e) => handleKeyDown(e, rowIndex, colIndex)}
              />
            ))}
          </div>
          <button onClick={handleSubmit} disabled={rowIndex !== activeRow || !isSubmitEnabled} >
            Submit
          </button>
        </div>
      ))}
      <button onClick={handleReset}>Reset</button>
      <SuggestedGuesses suggestions={suggestions} />
    </div>
  );
};

export default WordleBoard;

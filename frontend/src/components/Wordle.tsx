import React from 'react';
import WordleBoard from "./WordleBoard";

const Wordle: React.FC = () => {
  return (
    <div className="Wordle">
      <h1>Wordle Guess Suggestor</h1>
      <WordleBoard />
    </div>
  );
};

export default Wordle;

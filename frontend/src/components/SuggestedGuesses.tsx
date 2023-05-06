import React from 'react';
import {Word} from "../Interfaces/Word";

interface SuggestedGuessesProps {
  suggestions: Word[];
}
const SuggestedGuesses: React.FC<SuggestedGuessesProps> = ({ suggestions }) => {
  return (
    <ul>
        {suggestions.length ? suggestions.map(word => (
            <li key={word.id}>{word.word} - {word.score} - {word.info_gain}</li>
        )) : "No suggestions"}
    </ul>
  );
}

export default SuggestedGuesses;

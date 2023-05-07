import React from 'react';
import {Word} from "../Interfaces/Word";
import './SuggestedGuesses.css';

interface SuggestedGuessesProps {
  suggestions: Word[];
}
const SuggestedGuesses: React.FC<SuggestedGuessesProps> = ({ suggestions }) => {
    return (
        <div className="SuggestedGuesses">
          <h3>Suggested Guesses</h3>
            {suggestions.length === 0 && <p>No suggestions yet</p>}
            {suggestions && suggestions.length > 0 && (
              <table>
                <thead>
                  <tr>
                    <th>Word</th>
                    <th>Overall Score</th>
                    <th>Information Gained</th>
                  </tr>
                </thead>
                <tbody>
                  {suggestions.map((suggestion, index) => (
                    <tr key={suggestion.id}>
                      <td>{suggestion.word}</td>
                      <td>{suggestion.score.toFixed(2)}</td>
                      <td>{suggestion.info_gain.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
        </div>
  );
};

export default SuggestedGuesses;

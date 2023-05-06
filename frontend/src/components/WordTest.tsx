import React, { useEffect, useState } from 'react';
import api from '../axiosConfig';

interface Word {
  id: number;
  word: string;
  score: number;
  info_gain: number;
}


function WordList(): JSX.Element {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [words, setWords] = useState<Word[]>([]);

  useEffect(() => {
    api.post<Word[]>('suggest/', {
        guesses: ['saner', 'glint', 'ocean'],
        feedback: ['*yyy*', '***y*', '**gyy']
      })
      .then(res => {
        setWords(res.data);
        setIsLoading(false);
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <ul>
      {isLoading ?
          <p>Loading...</p> : words.length ? words.map(word => (
        <li key={word.id}>{word.word} - {word.score} - {word.info_gain}</li>
               
      )) : <p>No words found</p>}
    </ul>
  );
}

export default WordList;

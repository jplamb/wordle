import React, { useEffect, useState } from 'react';
import api from '../api';

interface Word {
  id: number;
  word: string;
  was_answer: boolean;
}

function WordList(): JSX.Element {
  const [words, setWords] = useState<Word[]>([]);

  useEffect(() => {
    api.get<Word[]>('http://127.0.0.1:8000/words/')
      .then(res => setWords(res.data))
      .catch(err => console.log(err));
  }, []);

  return (
    <ul>
      {words.map(word => (
        <li key={word.id}>{word.word}</li>
      ))}
    </ul>
  );
}

export default WordList;

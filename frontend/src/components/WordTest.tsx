import React, { useEffect, useState } from 'react';
import api from '../axiosConfig';

interface Word {
  id: number;
  word: string;
  was_answer: boolean;
}


function WordList(): JSX.Element {
  const [words, setWords] = useState<Word[]>([]);

  useEffect(() => {
    api.get<Word[]>('words/')
      .then(res => setWords(res.data))
      .catch(err => console.log(err));
  }, []);

  console.log(`words: ${words}`);

  return (
    <ul>
      {words.map(word => (
        <li key={word.id}>{word.word}</li>
      ))}
    </ul>
  );
}

export default WordList;

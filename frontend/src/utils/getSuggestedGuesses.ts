import api from '../axiosConfig';
import {Word} from "../Interfaces/Word";

async function getSuggestedGuesses(guesses: string[], feedback: string[]): Promise<Word[]> {
    console.log(`Retrieving suggested guesses for ${guesses} with feedback ${feedback}`);
  const response = await api.post<Word[]>('suggest/', {
        guesses, feedback,
      })

  return response.data;
}

export default getSuggestedGuesses;

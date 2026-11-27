import {gradeExercise} from './lib.js';

// Source-complete revisions must not display scores belonging to older,
// independently numbered practice questions. Stored records remain untouched.
export function currentAttemptResults(exercise,attempt,answers={}){
 if(!attempt?.results)return null;
 if(exercise.contentRevision&&attempt.contentRevision!==exercise.contentRevision)return gradeExercise(exercise,answers);
 return attempt.results;
}

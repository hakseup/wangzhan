export function compareExercises(sort,attempts,a,b){
 if(sort==='title')return a.title.localeCompare(b.title,'fr');
 if(sort==='progress')return Number(!!attempts[b.id])-Number(!!attempts[a.id]);
 if(sort==='unpracticed')return Number(!!attempts[a.id])-Number(!!attempts[b.id]);
 return 0;
}

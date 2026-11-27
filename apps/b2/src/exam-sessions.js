export function examSessions(exercise){
 const text=[exercise.source,exercise.examSessionLabel].filter(Boolean).join('；');
 const dates=[...new Set([...text.matchAll(/(\d{4})年(\d{1,2})月/g)].map(m=>`${m[1]}-${Number(m[2])}`))].sort((a,b)=>{const [ay,am]=a.split('-').map(Number),[by,bm]=b.split('-').map(Number);return ay-by||am-bm;});
 return dates.length?dates.map(date=>{const [year,month]=date.split('-');return `${year}年${month}月场`;}).join('、'):'国外考过，国内暂未考过';
}

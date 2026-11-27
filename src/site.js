// 胡桃法语门户的可编辑内容。
// 题库练习板块的数字来自真实题库（构建时生成 bank-stats.json）；
// 其余板块目前只有版式，下面带 sample: true 的条目都是占位示例，之后直接替换成正式内容即可。
import stats from './bank-stats.json';

export const NAV=[
 {id:'',zh:'首页',fr:'Accueil'},
 {id:'apprendre',zh:'系统学习',fr:'Apprendre'},
 {id:'lire',zh:'阅读精听',fr:'Lire & écouter'},
 {id:'exercer',zh:'题库练习',fr:"S'exercer"},
 {id:'professeurs',zh:'找老师',fr:'Professeurs'},
];

export const HERO={line1:'Un petit pas,',line2:'chaque jour.'};

// 今日推送（一词 / 一句 / 新闻）
export const TODAY={
 word:{sample:true,fr:'la flânerie',ipa:'[flɑnʁi]',pos:'n.f.',theme:'城市生活',zh:'闲逛、漫步；带着好奇心在城里随意走走。',example:'« Paris se découvre par la flânerie. »'},
 sentence:{sample:true,fr:'« Il n’est jamais trop tard pour apprendre. »',zh:'学习永远不嫌晚。',note:'il n’est jamais trop tard pour + inf.：做某事永远不晚'},
 news:[
  {sample:true,title:'Les cafés gardent leurs terrasses l’hiver',level:'B1',minutes:3,audio:true},
  {sample:true,title:'Le télétravail redessine les villes moyennes',level:'B2',minutes:6,audio:false},
  {sample:true,title:'Sommeil : ce que la recherche a vraiment prouvé',level:'C1',minutes:8,audio:true},
 ],
};

// 题库：DELF B2 与 DALF C1 为真实题库，其余等级预留位置。
export const BANKS=[
 {id:'b2',exam:'DELF',level:'B2',href:'/b2/',image:'/images/card-b2.webp',total:stats.b2.total,categories:stats.b2.categories,storageKey:'noix-delf-b2-v1',note:'兑换码开通 · 账号云端同步',
  parts:[['long','长听力'],['short','短听力'],['reading1','阅读 1'],['reading2','阅读 2'],['writing','写作'],['speaking','口语']]},
 {id:'c1',exam:'DALF',level:'C1',href:'/c1/',image:'/images/card-c1.webp',total:stats.c1.total,categories:stats.c1.categories,storageKey:'noix-dalf-c1-v1',note:'11 月 24 日更新版 · 登录后自动备份',
  parts:[['long','长听力'],['short','短听力'],['reading','阅读'],['writing','写作'],['speaking','口语']]},
];
export const UPCOMING_BANKS=[{exam:'DELF',level:'A2'},{exam:'DELF',level:'B1'}];

// 系统学习（版式占位）
export const LEVELS=['A1','A2','B1','B2','C1','C2'];
export const LEARN={
 tracks:[
  {id:'grammaire',fr:'Grammaire',zh:'分级语法',desc:'从冠词到虚拟式，每课配例句与小练习。',icon:'book'},
  {id:'vocabulaire',fr:'Vocabulaire',zh:'主题词汇',desc:'按生活场景组织的词汇单元。',icon:'layers'},
  {id:'conjugaison',fr:'Conjugaison',zh:'动词变位',desc:'常用动词变位表与变位训练。',icon:'repeat'},
  {id:'phonetique',fr:'Phonétique',zh:'语音发音',desc:'音素、连读与语调。',icon:'mic'},
 ],
 lessons:Array.from({length:6},(_,i)=>({sample:true,no:i+1,fr:'Leçon '+(i+1),zh:'课程标题待填写',level:'B1',minutes:20})),
 units:['城市生活','工作职场','教育','环境','健康','科技','文化艺术','社会'].map(name=>({sample:true,name,words:0})),
};

// 阅读精听（版式占位）
export const READ={
 filters:['全部','社会','文化','科技','环境','经济','生活'],
 articles:Array.from({length:6},(_,i)=>({sample:true,id:i,title:'Titre de l’article',zh:'文章标题待填写',level:['B1','B2','C1'][i%3],minutes:[3,5,8][i%3],topic:['社会','文化','科技'][i%3],audio:i%2===0})),
 dictations:Array.from({length:4},(_,i)=>({sample:true,id:i,title:'Dictée '+(i+1),segments:0})),
};

// 找老师（版式占位）
export const TEACHERS={
 filters:['全部','DELF/DALF 备考','口语陪练','写作批改','零基础入门'],
 list:Array.from({length:6},(_,i)=>({sample:true,id:i,name:'老师姓名',tagline:'一句话介绍待填写',tags:['标签','标签'],languages:'中文 / Français',price:null,video:true})),
 steps:[['看视频','先看老师的介绍视频'],['约时间','选择合适的上课时段'],['一对一','线上一对一上课'],['课后回顾','课后笔记与作业']],
};

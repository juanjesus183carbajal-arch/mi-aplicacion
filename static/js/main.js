let memFirst=null,memLock=false,memMoves=0,memPairs=0;
function startMemory(){
 const board=document.getElementById("memory-board");if(!board)return;
 memFirst=null;memLock=false;memMoves=0;memPairs=0;
 document.getElementById("moves").textContent="0";document.getElementById("pairs").textContent="0/6";
 document.getElementById("memory-msg").textContent="Voltea dos tarjetas para comenzar.";
 const values=["⭐","📚","🚀","🧠","🎮","👑"];[...values,...values].sort(()=>Math.random()-.5).forEach(v=>{
  const b=document.createElement("button");b.className="memory-card";b.textContent="❔";b.dataset.v=v;b.onclick=()=>flipMemory(b);board.appendChild(b);
 });
}
function flipMemory(card){
 if(memLock||card.classList.contains("done")||card===memFirst)return;
 card.textContent=card.dataset.v;card.classList.add("open");
 if(!memFirst){memFirst=card;return;}
 memMoves++;document.getElementById("moves").textContent=memMoves;
 if(memFirst.dataset.v===card.dataset.v){memFirst.classList.add("done");card.classList.add("done");memFirst=null;memPairs++;document.getElementById("pairs").textContent=memPairs+"/6";
  if(memPairs===6)document.getElementById("memory-msg").textContent="¡Lo lograste! Encontraste todas las parejas. 🎉";
 }else{memLock=true;let prev=memFirst;memFirst=null;setTimeout(()=>{prev.textContent="❔";card.textContent="❔";prev.classList.remove("open");card.classList.remove("open");memLock=false;},700);}
}
let qIndex=0,qScore=0,qAnswer=0;
function makeQuestion(){
 const a=Math.floor(Math.random()*12)+2,b=Math.floor(Math.random()*10)+2,ops=["+","−","×"],op=ops[Math.floor(Math.random()*3)];
 qAnswer=op==="+"?a+b:op==="−"?Math.abs(a-b):a*b;
 document.getElementById("question").textContent=`${a} ${op} ${b} = ?`;document.getElementById("qnum").textContent=(qIndex+1)+"/5";
 document.getElementById("score").textContent=qScore;document.getElementById("answer").value="";document.getElementById("feedback").textContent="";
}
document.addEventListener("DOMContentLoaded",()=>{
 const form=document.getElementById("math-form");if(!form)return;makeQuestion();
 form.addEventListener("submit",e=>{e.preventDefault();const val=Number(document.getElementById("answer").value);
 if(val===qAnswer){qScore+=20;document.getElementById("feedback").textContent="¡Correcto! +20 puntos ⭐";}else{document.getElementById("feedback").textContent="La respuesta era "+qAnswer+". ¡Sigue practicando!";}
 form.querySelector("button").disabled=true;document.getElementById("next").hidden=false;
 });
});
function nextQuestion(){
 qIndex++;if(qIndex>=5){document.getElementById("question").textContent="¡Reto terminado!";document.getElementById("math-form").hidden=true;document.getElementById("next").hidden=true;document.getElementById("feedback").textContent="Terminaste el reto. Puntos obtenidos: "+qScore;return;}
 document.getElementById("math-form").querySelector("button").disabled=false;document.getElementById("next").hidden=true;makeQuestion();
}


function startSubjectMemory(subject){
 const board=document.getElementById("memory-board");if(!board)return;
 let pairs=subject==="lengua"?[["📖","Comprender"],["✍️","Escribir"],["🔤","Palabra"],["📝","Texto"],["💬","Diálogo"],["🔎","Idea"]]:
 [["➕","Suma"],["➖","Resta"],["✖️","Multiplica"],["➗","Divide"],["📐","Geometría"],["％","Porcentaje"]];
 let cards=pairs.flatMap((p,i)=>[{id:i,label:p[0]},{id:i,label:p[1]}]).sort(()=>Math.random()-.5);
 let first=null,lock=false,moves=0,found=0;board.innerHTML="";
 document.getElementById("moves").textContent="0";document.getElementById("pairs").textContent="0/6";
 document.getElementById("memory-msg").textContent="Encuentra las parejas relacionadas.";
 cards.forEach(item=>{let b=document.createElement("button");b.className="memory-card";b.textContent="❔";b.dataset.id=item.id;b.dataset.label=item.label;b.onclick=()=>{
  if(lock||b.classList.contains("done")||b===first)return;
  b.textContent=b.dataset.label;b.classList.add("open");
  if(!first){first=b;return;}
  moves++;document.getElementById("moves").textContent=moves;
  if(first.dataset.id===b.dataset.id){first.classList.add("done");b.classList.add("done");first=null;found++;document.getElementById("pairs").textContent=found+"/6";if(found===6)document.getElementById("memory-msg").textContent="¡Completaste el memorama! 🎉";}
  else{lock=true;let old=first;first=null;setTimeout(()=>{old.textContent="❔";b.textContent="❔";old.classList.remove("open");b.classList.remove("open");lock=false;},800);}
 };board.appendChild(b);});
}
let subjectItems=[],subjectIndex=0,subjectScore=0,subjectAnswer="";
function startSubjectChallenge(subject){
 subjectItems=subject==="lengua"?[
  {q:"¿Qué palabra es sinónimo de feliz?",a:"alegre",alts:["triste","oscuro"]},
  {q:"¿Qué signo cierra una pregunta?",a:"?",alts:["!"," ."]},
  {q:"¿Cómo se llama la idea más importante de un texto?",a:"principal",alts:["decorativa","secundaria"]},
  {q:"Completa: Las palabras opuestas son…",a:"antonimos",alts:["sinonimos","verbos"]},
  {q:"¿Qué usamos para separar elementos de una lista?",a:"coma",alts:["punto final","guion largo"]}
 ]:[
  {q:"¿Cuánto es 8 × 7?",a:"56",alts:["54","64"]},
  {q:"¿Cuánto es 25% de 100?",a:"25",alts:["20","50"]},
  {q:"Resuelve: x + 6 = 10. x =",a:"4",alts:["16","6"]},
  {q:"¿Cuánto es 3/5 + 1/5? (escribe 4/5)",a:"4/5",alts:["3/10","2/5"]},
  {q:"Área de un rectángulo de 5 × 4:",a:"20",alts:["9","18"]}
 ];
 subjectIndex=0;subjectScore=0;renderSubjectQuestion();
}
function renderSubjectQuestion(){
 const item=subjectItems[subjectIndex];subjectAnswer=item.a;
 document.getElementById("question").textContent=item.q;
 document.getElementById("qnum").textContent=(subjectIndex+1)+"/5";
 document.getElementById("score").textContent=subjectScore;
 document.getElementById("answer").value="";
 document.getElementById("feedback").textContent="";
 document.getElementById("math-form").hidden=false;
 document.getElementById("math-form").querySelector("button").disabled=false;
 document.getElementById("next").hidden=true;
}
function nextSubjectQuestion(){
 subjectIndex++;
 if(subjectIndex>=5){document.getElementById("question").textContent="¡Reto terminado!";document.getElementById("math-form").hidden=true;document.getElementById("next").hidden=true;document.getElementById("feedback").textContent="Puntos obtenidos: "+subjectScore+" de 50. ¡Buen trabajo!";return;}
 renderSubjectQuestion();
}
document.addEventListener("DOMContentLoaded",()=>{
 const form=document.getElementById("math-form");if(!form)return;
 form.addEventListener("submit",e=>{e.preventDefault();let val=document.getElementById("answer").value.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/\s+/g,"");
 let expected=subjectAnswer.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/\s+/g,"");
 if(val===expected){subjectScore+=10;document.getElementById("feedback").textContent="¡Correcto! +10 puntos ⭐";}
 else{document.getElementById("feedback").textContent="Respuesta correcta: "+subjectAnswer+". ¡Sigue practicando!";}
 form.querySelector("button").disabled=true;document.getElementById("next").hidden=false;
 });
});

let b_movie = document.querySelector("#bMovie");
let s_movie = document.querySelector("#inlineFormInputGroup");
let n_movie = document.querySelector("#nMovie");


/*
b_movie.addEventListener("click",function() {count_click("b");});
s_movie.addEventListener("focus",function() {count_click("s");});
n_movie.addEventListener("click",function() {count_click("n");});
*/
b_movie.addEventListener("click",b_click)
s_movie.addEventListener("click",s_click)
n_movie.addEventListener("click",n_click)

let count={
  btn: 0,
  search: 0,
  navi: 0,
}

function b_click(ev){
  ev.preventDefault();
  count.btn++;
  console.log(count);
}
function s_click(ev){
  count.search++;
  console.log(count);
}
function n_click(ev){
  ev.preventDefault();
  count.navi++;
  console.log(count);
}


function count_click(flag){
  if(flag == "b")
  {count.btn++;}
  else if(flag == "s")
  {count.search++;}
  else(flag == "n")
  {count.navi++;}
  console.log(count);
}


/*
let upc = document.querySelector("#upcoming");
let rec = document.querySelector("#recommend");

upc.addEventListener("mouseenter",enter);
upc.addEventListener("mouseleave",leave);
rec.addEventListener("mouseenter",enter);
rec.addEventListener("mouseleave",leave);


function enter(){
  console.log("mouseEnter");
}

function leave(){
  console.log("mouseLeave");
}
*/
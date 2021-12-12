var s_tab1 = document.querySelector("#s_tab1")
var s_tab2 = document.querySelector("#s_tab2")
var s_tab3 = document.querySelector("#s_tab3")
var s_tab4 = document.querySelector("#s_tab4")
var s_tab5 = document.querySelector("#s_tab5")
var s_tab6 = document.querySelector("#s_tab6")
var s_tab7 = document.querySelector("#s_tab7")
var s_tab8 = document.querySelector("#s_tab8")

var title = document.querySelector("#title")

var inlist = document.querySelector("#inList")

//console.log(entries)

function visi(){
  s_tab4.style.visibility="visible";
  s_tab5.style.visibility="visible";
  s_tab6.style.visibility="visible";
  s_tab7.style.visibility="visible";
  s_tab8.style.visibility="visible";
}
function first_select(type){
  if(type == "genre"){
    //console.log(type,s_tab1,s_tab2,s_tab3)
    visi()
    s_tab1.innerHTML='太空歌剧'
    s_tab2.innerHTML='太空冒险'
    s_tab3.innerHTML='社会科幻'
    s_tab4.innerHTML='机器人'
    s_tab5.innerHTML='赛博格'
    s_tab6.innerHTML='时空旅行'
    s_tab7.innerHTML='超人类'
    s_tab8.innerHTML='未来恐惧'

  }
  else if(type == "time"){
    //console.log(type,s_tab1,s_tab2,s_tab3)
    visi()
    s_tab1.innerHTML='2020s'
    s_tab2.innerHTML='2010s'
    s_tab3.innerHTML='2000s'
    s_tab4.innerHTML='1990s'
    s_tab5.innerHTML='1980s'
    s_tab6.innerHTML='1970s'
    s_tab7.innerHTML='1960s'
    s_tab8.innerHTML='其他'
  }
  else{
    //console.log(type,s_tab1,s_tab2,s_tab3)
    s_tab1.innerHTML='美国'
    s_tab2.innerHTML='日本'
    s_tab3.innerHTML='其他'
    s_tab4.style.visibility="hidden";
    s_tab5.style.visibility="hidden";
    s_tab6.style.visibility="hidden";
    s_tab7.style.visibility="hidden";
    s_tab8.style.visibility="hidden";
  }
}

//var src_test = document.querySelector("#src_test")
function second_select(content){
  title.innerHTML=content;
  //inlist.src="{{url_for('innerList',type='"+ content +"')}}"
  //inlist.src = "&lcub"+"&lcub"+"url_for('innerList',type='"+content+"')"+"&rcub"+"&rcub"
  //inlist.src = encodeURI("{{url_for('innerList',type='"+ content + "')}}")
  //console.log(src_test.innerHTML)
  //src_test.innerHTML = "{{url_for('innerList',type ='"+ content +"')}}"
  //console.log(src_test.innerHTML)
}
# Replace this line in the html:
# function chk(id,fair){let i=document.getElementById(id);let b=document.getElementById(id+'_b');let v=parseFloat(i.value);if(!isNaN(v)&&v>fair){b.style.display='inline';b.innerText='VALUE '+v+'>'+fair;}else{b.style.display='none';}}}

# With this:
html = html.replace("function chk", """
function chk(id,fair){
  let i=document.getElementById(id);
  let b=document.getElementById(id+'_b');
  let v=parseFloat(i.value);
  if(!isNaN(v)){
    let edge = ((v/fair)-1)*100;
    if(v>fair){
      b.style.display='inline';
      b.style.background='#00ff88';
      b.innerText='VALUE '+v+'>'+fair+' (+'+edge.toFixed(1)+'%)';
    } else {
      b.style.display='inline';
      b.style.background='#ff4444';
      b.style.color='#fff';
      b.innerText='NO VALUE '+edge.toFixed(1)+'%';
    }
  }
}
""")

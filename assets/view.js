CTFd._internal.challenge.data = undefined;

CTFd._internal.challenge.preRender = function() {
};

CTFd._internal.challenge.postRender = function() {
  setTimeout(()=>{
    document.querySelector(".challenge-desc ul").setAttribute("x-init",'submission=[]')
    document.querySelectorAll(".challenge-desc li").forEach((el, index)=>{
      radio = el.innerText.match(/^\(\s*\)\s*(.*)$/)
      checkbox = el.innerText.match(/^\[\s*\]\s*(.*)$/)
      letters = "ABCDEFGHIJKLMNOPQRST"
      if (radio) {
        el.innerHTML = "<input class=\"form-check-input\" " +
            "type=\"radio\" " +
            "x-model=\"submission\" " +
            "id=\"option_"+ index +"\" " +
            "value=\""+ letters[index] +"\">" +
            "<label class=\"form-check-label\" for=\"option_"+ index +"\">" +
            letters[index] + '. ' +
            radio[1] +
            "</label>"
      } else if (checkbox) {
        // TODO: some thing wrong, the checkbox checks all automatically.
        el.innerHTML = "<input class=\"form-check-input\" " +
            "type=\"checkbox\" " +
            "name=\"submission\"" +
            "x-model=\"submission\" " +
            "id=\"option_"+ index +"\" " +
            "value=\""+ letters[index] +"\">" +
            "<label class=\"form-check-label\" for=\"option_"+ index +"\">" +
            letters[index] + '. ' +
            checkbox[1] +
            "</label>"
      }
      // el.style.display = "block"
      el.className = "form-check"
    })
  },200);
  // document.querySelector("#challenge-submit").onclick = CTFd._internal.challenge.submit
};

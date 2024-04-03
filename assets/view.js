CTFd._internal.challenge.data = undefined;

CTFd._internal.challenge.preRender = function() {
};

CTFd._internal.challenge.postRender = function() {
  setTimeout(()=>{
    document.querySelectorAll(".challenge-desc ul").forEach((ul, index)=>{
      foundRadio = false
      foundCheckbox = false
      ul.querySelectorAll(".challenge-desc li").forEach((el, index)=> {
        radio = el.innerHTML.match(/^\(\s*\)\s*([\w\W]*)$/)
        checkbox = el.innerHTML.match(/^\[\s*\]\s*([\w\W]*)$/)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if (radio) {
          el.innerHTML = "<input class=\"form-check-input\" " +
              "type=\"radio\" " +
              "x-model=\"submission\" " +
              "id=\"option_" + index + "\" " +
              "value=\"" + letters[index] + "\">" +
              "<label class=\"form-check-label\" for=\"option_" + index + "\">" +
              letters[index] + '. ' +
              radio[1] +
              "</label>"
          el.className = "form-check"
          foundRadio = true
        } else if (checkbox) {
          // TODO: some thing wrong, the checkbox checks all automatically.
          el.innerHTML = "<input class=\"form-check-input\" " +
              "type=\"checkbox\" " +
              "name=\"submission\"" +
              "x-model=\"submission\" " +
              "id=\"option_" + index + "\" " +
              "value=\"" + letters[index] + "\">" +
              "<label class=\"form-check-label\" for=\"option_" + index + "\">" +
              letters[index] + '. ' +
              checkbox[1] +
              "</label>"
          el.className = "form-check"
          foundCheckbox = true
        } else {
          return false
        }
        // el.style.display = "block"
      })
      if (foundCheckbox) {
        ul.setAttribute("x-init",'submission=[]')
      }
      if (foundRadio) {
        ul.setAttribute("x-init",'submission=""')
      }
    })
  },200);
  // document.querySelector("#challenge-submit").onclick = CTFd._internal.challenge.submit
};

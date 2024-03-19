CTFd._internal.challenge.data = undefined;

CTFd._internal.challenge.preRender = function() {
  document.querySelectorAll(".challenge-desc li").forEach((el, index)=>{
    matches = el.innerText.match(/^\(\s*\)\s*(.*)$/)
    if (matches) {
      el.innerHTML = "<div class=\"form-check\"><input class=\"form-check-input\" " +
          "type=\"radio\" " +
          "name=\"answer\" " +
          "id=\"answer_"+ index +"\" " +
          "value=\""+ matches[1] +"\">" +
          "<label class=\"form-check-label\" for=\"answer_"+ index +"\">" +
          matches[1] +
          "</label></div>"
      el.style.display = "block"
      el.onchange = () => {
        CTFd.lib.$("#challenge-input")
            .val(CTFd.lib.$("input[name=answer]:checked").val())
            .trigger('keyup', CTFd.lib.$("input[name=answer]:checked").val() // 不知道为什么。。。。
      }
    }
  })
};

CTFd._internal.challenge.postRender = function() {
};

const textarea = document.querySelectorAll(".form-control2");

for (let i = 0; i < textarea.length; i++) {
  const counter = document.querySelectorAll(".count");

  counter[i].textContent = textarea[i].textContent.length;

  const counting = e => {
    let text = e.target.value;
    let count = text.length;

    counter[i].textContent = count;
  };

  ["keydown", "click"].forEach(event =>
    textarea[i].addEventListener(event, counting)
  );
}

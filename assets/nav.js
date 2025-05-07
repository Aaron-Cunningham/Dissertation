document.addEventListener("DOMContentLoaded", function () {
  function resetButtonColors() {
    // for each nav button, set background color to white
    document.querySelectorAll(".nav-button").forEach((button) => {
      button.style.backgroundColor = "white";
      button.style.color = "black";
    });
  }

  function setActiveButton(button) {
    // reset all button colors
    resetButtonColors();
    // set the clicked button to active
    button.style.backgroundColor = "#ED393B";
    button.style.color = "white";
  }

  setTimeout(() => {
    // add event listener to each nav button
    document.querySelectorAll(".nav-button").forEach((button) => {
      // when clicked set the active button
      button.addEventListener("click", function () {
        // set the active button
        setActiveButton(this);
      });
    });
  }, 1000); // ensures dash renders
});

document.addEventListener('DOMContentLoaded', function() {

   
})

function read_more() {
  var dots = document.getElementById("dots");
  var moreText = document.getElementById("readmore");
  var btnText = document.getElementById("readmore-btn");

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more";
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less";
    moreText.style.display = "inline";
  }
}
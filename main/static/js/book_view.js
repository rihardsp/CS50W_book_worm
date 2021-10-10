document.addEventListener('DOMContentLoaded', function() {


  //document.querySelector('#btn - submit_blog_form').addEventListener('click', () => submit_blog);
  //document.querySelector('#btn-submit_blog_form').addEventListener('click', submit_blog);
  var submitBlogButton = document.getElementById('btn_submit_blog_form');
  var alertField = document.getElementById('alert_field');
  var textField = document.getElementById('blog_text');
  var titleField = document.getElementById('blog_title');
  document.addEventListener('input', function(e) {
    if (alertField.style.display == 'inline') {
      if (e.target) {
        if (e.target.id == 'blog_title' || e.target.id == 'blog_text') {
          alertField.style.display = 'none';
        }
      }
    }
  });


  submitBlogButton.addEventListener('click', function() {

    let blogTitle = titleField.value;
    let blogText = textField.value;
    let bookKey = submitBlogButton.name;
    console.log(blogText, blogTitle, bookKey)
    /* alerts
    <divclass="alert alert-warning" role="alert">
      This is a warning alert—check it out!
      class="alert alert-warning fade show"
    </div>
    */

    if (blogTitle == "" || blogTitle == null) {
      alertField.style.display = 'inline';
      alertField.className = "alert alert-warning fade show";
      alertField.innerHTML = "Please enter blogs title!";
    }
    else if (blogText == "" || blogText == null) {
      alertField.style.display = 'inline';
      alertField.className = "alert alert-warning fade show";
      alertField.innerHTML = "Please enter text!";
    }
    else if (blogText != "" && blogText != null && blogTitle != "" && blogTitle != null) {
      fetch('/save_post', {
        method: 'POST',
        body: JSON.stringify({
          book_key: bookKey,
          blog_title: blogTitle,
          blog_text: blogText
        })
      }).then(response => {

        if (response.status = 201) {
          textField.disabled = true;
          titleField.disabled = true;
          submitBlogButton.disabled = true;
          alertField.style.display = 'inline';
          alertField.className = "alert alert-success fade show";
          alertField.innerHTML = `Blog saved successfully!`;
        }
        else {
          textField.disabled = true;
          titleField.disabled = true;
          submitBlogButton.disabled = true;
          alertField.style.display = 'inline';
          alertField.className = "alert alert-warning fade show";
          alertField.innerHTML = `Something went horribly wrong, please contact site administrator!`;
        }
      });

    }
  });

  var addRemoveButton = document.getElementById("btn_library");
  addRemoveButton.addEventListener('click', function() {

    let bookKey = addRemoveButton.value;
    let bookInLibrary = addRemoveButton.name;

    fetch('/library-toggle', {
        method: 'POST',
        body: JSON.stringify({
          book_key: bookKey,
          book_in_library: bookInLibrary
        })
      }).then(response => response.json())
      .then(data => {

        if (data["name"] == true) {
          addRemoveButton.innerHTML = "Remove from my library";
          addRemoveButton.name = "True";
        }
        else if (data["name"] == false) {
          addRemoveButton.innerHTML = "Save to my library";
          addRemoveButton.name = "False";
        }
        else {
          addRemoveButton.innerHTML = "Please reload the page!";
          addRemoveButton.style = "colour: red";
        }
      });
  });

});


function read_more() {
  // Used directly from HTML 
  var dots = document.getElementById("dots");
  var moreText = document.getElementById("readmore");
  var btnText = document.getElementById("readmore-btn");

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more";
    moreText.style.display = "none";
  }
  else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less";
    moreText.style.display = "inline";
  }
}

document.addEventListener('DOMContentLoaded', function() {


  //document.querySelector('#btn - submit_blog_form').addEventListener('click', () => submit_blog);
  //document.querySelector('#btn-submit_blog_form').addEventListener('click', submit_blog);
  var submit_blog_button = document.getElementById('btn_submit_blog_form')
  var alertfield = document.getElementById('alert_field')
  var textfield = document.getElementById('blog_text')
  var titlefield = document.getElementById('blog_title')
  document.addEventListener('input', function(e) {
    if (alertfield.style.display == 'inline') {
      if (e.target) {
        if (e.target.id == 'blog_title' || e.target.id == 'blog_text') {
          alertfield.style.display = 'none'
        }
      }
    }
  })


  submit_blog_button.addEventListener('click', function() {

    let blog_title = titlefield.value
    let blog_text = textfield.value
    let book_key = submit_blog_button.name
    console.log(blog_text, blog_title, book_key)
    /* alerts
    <divclass="alert alert-warning" role="alert">
      This is a warning alert—check it out!
      class="alert alert-warning fade show"
    </div>
    */

    if (blog_title == "" || blog_title == null) {
      alertfield.style.display = 'inline';
      alertfield.className = "alert alert-warning fade show"
      alertfield.innerHTML = "Please enter blogs title!"
    }
    else if (blog_text == "" || blog_text == null) {
      alertfield.style.display = 'inline';
      alertfield.className = "alert alert-warning fade show"
      alertfield.innerHTML = "Please enter text!"
    }
    else if (blog_text != "" && blog_text != null && blog_title != "" && blog_title != null) {
      fetch('/save_post', {
        method: 'POST',
        body: JSON.stringify({
          book_key: book_key,
          blog_title: blog_title,
          blog_text: blog_text
        })
      }).then(response => {

        if (response.status = 201) {
          textfield.disabled = true;
          titlefield.disabled = true;
          submit_blog_button.disabled = true;
          alertfield.style.display = 'inline';
          alertfield.className = "alert alert-success fade show"
          alertfield.innerHTML = `Blog saved successfully!`
        }
        else {
          textfield.disabled = true;
          titlefield.disabled = true;
          submit_blog_button.disabled = true;
          alertfield.style.display = 'inline';
          alertfield.className = "alert alert-warning fade show"
          alertfield.innerHTML = `Something went horribly wrong, please contact site administrator!`
        }
      })

    }
  });

  var add_remove_button = document.getElementById("btn_library")
  add_remove_button.addEventListener('click', function() {

    let book_key = add_remove_button.value
    let book_in_library = add_remove_button.name

    fetch('/library-toggle', {
        method: 'POST',
        body: JSON.stringify({
          book_key: book_key,
          book_in_library: book_in_library
        })
      }).then(response => response.json())
      .then(data => {

        if (data["name"] == true) {
          add_remove_button.innerHTML = "Remove from my library"
          add_remove_button.name = "True"
        }
        else if (data["name"] == false) {
          add_remove_button.innerHTML = "Save to my library"
          add_remove_button.name = "False"
        }
        else {
          add_remove_button.innerHTML = "Please reload the page!"
          add_remove_button.style = "colour: red"
        }
      });
  })

})


function read_more() {
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

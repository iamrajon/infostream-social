document.addEventListener("DOMContentLoaded", function() {
    var likeButtons = document.querySelectorAll(".like-button");
  
    for (var i = 0; i < likeButtons.length; i++) {
      likeButtons[i].addEventListener("click", function(e) {
        e.preventDefault();
  
        var postId = this.getAttribute("data-post-id");
        var liked = this.querySelector("i.fa-heart");
  
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "{% url 'like-post' %}", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
  
        xhr.onreadystatechange = function() {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
              var response = JSON.parse(xhr.responseText);
              if (response.liked) {
                liked.classList.remove("fa-regular");
                liked.classList.add("fa-solid");
                liked.style.color = "#fb0404";
              } else {
                liked.classList.remove("fa-solid");
                liked.classList.add("fa-regular");
                liked.style.color = "red";
              }
              this.querySelector("span").innerText = response.like_count;
            } else {
              console.log(xhr.status + ": " + xhr.responseText);
            }
          }
        }.bind(this);
  
        xhr.send("post_id=" + postId);
      });
    }
  });



document.getElementById("check-btn").addEventListener("click", myAction);

function myAction(){
    console.log("Button clicked..");
}
  
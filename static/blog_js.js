
// Not currently implemented.
$(".rating").on("click", function() {
    var rating = this.getAttribute("id");
    var data = "rating=" + rating;
    var counter = this.nextSibling.nextSibling;
    var error_id = "error-" + rating.split("-")[1];
    var error = document.getElementById(error_id);
    var this_button = $(this);

    $.ajax({
        type: "POST",
        url: "/rate",
        data: data,
        success: function(data) {
            if(data.stat == "ok") {
                counter.textContent = data.count;
                this_button.addClass(rating.split("-")[0]);
            } else if(data.stat == "not_logged_in") {
                error.textContent = "You must be logged in to rate a post.";
            } else if(data.stat == "rate_your_own") {
                error.textContent = "You can't rate your own post!";
            }
        }
    });
})

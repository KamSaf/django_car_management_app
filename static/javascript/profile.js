$(function() {
    $(".delete-profile-button").on("click", function() {
      var modal = new bootstrap.Modal(document.getElementById("confirm_delete_modal"));
      modal.show();
    });
});

$(function() {
    $(".edit-profile-button").on("click", function() {
      var modal = new bootstrap.Modal(document.getElementById("edit_profile_modal"));
      modal.show();
    });

  $(".save-edit-profile-button").on("click", function(event) {
    console.log('dupa');
    event.preventDefault();
    console.log($('form').serializeArray());
      $.ajax({
        type: "POST",
        url: "edit_user/",
        data: $('form').serializeArray(),
        success: function(response) {
          console.log(response);
          let errors = "";
          if (response['errors']){
            response['errors'].forEach(error => {errors += error});
          }
          if (errors){
            $('#submit_info').html(errors).prop('style', 'display: block;');
          }
        }
      });
  });
});
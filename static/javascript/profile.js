function clearErrors(){
  $('#submit_info').prop('style', 'display: none;');
  $('.is-invalid').removeClass('is-invalid');
}

$(function() {
    $(".clear-errors").on("click", function() {
      clearErrors();
      $('#data_edit_success').prop('style', 'display: none;');

    });
});

$(function() {
  var modal = new bootstrap.Modal(document.getElementById("edit_profile_modal"));

  $(".save-edit-profile-button").on("click", function(event) {
    event.preventDefault();
    clearErrors();
      $.ajax({
        type: "POST",
        url: "edit_user/",
        data: $('form').serializeArray(),
        success: function(response) {
          $('#id_current_password').val('');
          let errors = "";
          if (response['errors']){
            for (key in response['errors']){
              $('#' + key).addClass('is-invalid');
              if (response['errors'][key].length > 0){
                errors += response['errors'][key] + '<br>';
              }
            }
          }
          if (errors){
            $('#submit_info').html(errors).prop('style', 'display: block;');
          } else {
            var $userData = $('#user_data');
            var $navbar = $('#navbar');
            $userData.load($userData.data('refresh-url'));
            $navbar.load($navbar.data('refresh-url'));
            $('#data_edit_success').prop('style', 'display: block;');
            modal.hide();
          }
        }
      });
  });
});
$(function() {
  var modal = new bootstrap.Modal(document.getElementById("edit_profile_modal"));

  $(".save-edit-profile-button").on("click", function(event) {

    event.preventDefault();
    clearErrors();

    var fieldsToValidate = ['#id_username', '#id_email', '#id_current_password'];
    var fieldsValid = true;

    for (var i = 0; i < fieldsToValidate.length; i++) {
      var field = $(fieldsToValidate[i]);
      if (!field.val()) {
        field.addClass('is-invalid');
        fieldsValid = false;
      }
    }
    
    if (!fieldsValid) {
      $('#submit_info').html("<b>Required</b> fields must not be left blank.").prop('style', 'display: block;');
      return;
    }
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
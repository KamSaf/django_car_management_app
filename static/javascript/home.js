$(function(){
    $(".new-workshop-main").on("click", function() {
        $('#new_workshop_close_modal_button')
            .removeAttr('data-bs-target')
            .removeAttr('data-bs-toggle')
            .attr('data-bs-dismiss', 'modal')
            .html('Close');
    });

    $(".new-workshop-embedded").on("click", function() {
        $('#new_workshop_close_modal_button')
            .attr('data-bs-target', '#workshops_list_modal')
            .attr('data-bs-toggle', 'modal')
            .removeAttr('data-bs-dismiss')
            .html('Go back');
    });
});

$(function() {  
    $(".save-new-workshop-button").on("click", function(event) {
      event.preventDefault();
      clearErrors();

      var fieldsToValidate = ['#id_name', '#id_city', '#id_address', '#id_phone_number', '#id_profession'];
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
          url: $(this).data('url'),
          data: $('form').serializeArray(),
          success: function(response) {
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
            //   var $userData = $('#user_data');
            //   var $navbar = $('#navbar');
            //   $userData.load($userData.data('refresh-url'));
            //   $navbar.load($navbar.data('refresh-url'));
            //   $('#data_edit_success').prop('style', 'display: block;');
              modal.hide();
            }
          }
        });
    });
  });
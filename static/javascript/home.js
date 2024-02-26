function checkIfValidPhoneNumber(phoneNumber){
  if (phoneNumber.length != 9){
    return false
  }
  for (char of phoneNumber) {
    if (isNaN(char)){
      return false;
    }
    return true;
  };
}

function clearWorkshopForm(){
  clearErrors();
  var fieldsToClear = ['#id_name', '#id_city', '#id_address', '#id_phone_number', '#id_profession'];
  for (var i = 0; i < fieldsToClear.length; i++) {
    $(fieldsToClear[i]).val('');
  }
};


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
  var modal = new bootstrap.Modal(document.getElementById("new_workshop_modal"));

    $(".save-new-workshop").on("click", function(event) {
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

      if (!checkIfValidPhoneNumber($('#id_phone_number').val())){
        $('#id_phone_number').addClass('is-invalid');
        $('#submit_info').html("Invalid phone number.").prop('style', 'display: block;');
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
              // odświeżanie obu list warsztatów
              // wiadomość z przyciskiej OK (do odrzucenia)
              clearWorkshopForm();
              modal.hide();
            }
          }
        });
    });
});

$(document).ready(function(){
  $('#new_workshop_modal').on('hidden.bs.modal', function () {
    clearWorkshopForm();
  });
});

$(function() {  
    $(".show-workshop-details").on("click", function() {
      var url = $(this).data('url');
      var $modalContent = $('#workshop_details_modal_content');
      $modalContent.load(url);
    });
});
// Function for phone number field validation
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

// Function for clearing current form errors and entered data
function clearWorkshopForm(){
  clearErrors();
  var fieldsToClear = ['#id_name', '#id_city', '#id_address', '#id_phone_number', '#id_profession'];
  for (var i = 0; i < fieldsToClear.length; i++) {
    $(fieldsToClear[i]).val('');
  }
};

// Function for workshop form data validation
function validateWorkshopData(submit_info_box_id){
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
    $('#' + submit_info_box_id).html("<b>Required</b> fields must not be left blank.").prop('style', 'display: block;');
    return false;
  }

  if (!checkIfValidPhoneNumber($('#id_phone_number').val())){
    $('#id_phone_number').addClass('is-invalid');
    $('#' + submit_info_box_id).html("Invalid phone number.").prop('style', 'display: block;');
    return false;
  }
  return true;
};

// Function for handling workshop create/edit errors and refreshing workshops lists
function workshopsHandleResponse(response, modal, submit_info_box_id){
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
    console.log($('#' + submit_info_box_id));
    $('#' + submit_info_box_id).html(errors).prop('style', 'display: block;');
  } else {
    // odświeżanie obu list warsztatów
    // wiadomość z przyciskiej OK (do odrzucenia)
    clearWorkshopForm();
    modal.hide();
  }
};

// Function altering modals buttons based on the way it was opened
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


// ################## jQuery #########################

// Handles new workshop creation request
$(function() {  
  var modal = new bootstrap.Modal(document.getElementById("new_workshop_modal"));

    $(".save-new-workshop").on("click", function(event) {
      event.preventDefault();

      if (!validateWorkshopData('new_workshop_submit_info')){
        return;
      }

      $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: $('form').serializeArray(),
        success: function(response) {
          workshopsHandleResponse(response, modal, 'new_workshop_submit_info');
        }
      });
    });
});

// Clears workshop form when leaving modal
$(function(){
  $('#new_workshop_modal').on('hidden.bs.modal', function () {
    clearWorkshopForm();
  });
});

// Loads content of the workshop details modal
$(function() {  
    $(".show-workshop-details").on("click", function() {
      var url = $(this).data('url');
      var $modalContent = $('#workshop_details_modal_content');
      $modalContent.load(url);
    });
});

// Handles workshop edit request
$(function() {
  var modal = new bootstrap.Modal(document.getElementById("workshop_details_modal"));

  $('#workshop_details_modal').on('click', '.save-edit-workshop-data', function(event) {
    event.preventDefault();
  
    if (!validateWorkshopData('edit_workshop_submit_info')){
      return;
    }
  
    $.ajax({
      type: "POST",
      url: $(this).data('url'),
      data: $('form').serializeArray(),
      success: function(response) {
        workshopsHandleResponse(response, modal, 'edit_workshop_submit_info');
      }
    });
  });
});
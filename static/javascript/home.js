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

// Function for clearing form errors and entered data
function clearForm(form_id){
  clearErrors();
  $('#' + form_id + ' *').filter(':input').not($("input:hidden")).each(function(){
    $(this).val('');
  });
};

// Function for workshop form data validation
function validateWorkshopData(submit_info_box_id, form_id){
  clearErrors();
  var fieldsToValidate = ['#id_name', '#id_city', '#id_address', '#id_phone_number', '#id_profession'];
  var fieldsValid = true;

  for (var i = 0; i < fieldsToValidate.length; i++) {
    var field = $('#' + form_id + ' ' +fieldsToValidate[i]);
    if (!field.val()) {
      field.addClass('is-invalid');
      fieldsValid = false;
    }
  }
  
  if (!fieldsValid) {
    $('#' + submit_info_box_id).html("<b>Required</b> fields must not be left blank.").prop('style', 'display: block;');
    return false;
  }

  if (!checkIfValidPhoneNumber($('#' + form_id + ' #id_phone_number').val())){
    $('#' + form_id + ' #id_phone_number').addClass('is-invalid');
    $('#' + submit_info_box_id).html("Invalid phone number.").prop('style', 'display: block;');
    return false;
  }
  return true;
};

// Function for refreshing workshops lists
function refreshWorkshopsLists(){
  $('#workshops_list').load($('#workshops_list').data('url'));
  $('#favourite_workshops_list').load($('#favourite_workshops_list').data('url'));
}

// Function for handling ajax response
function handleAjaxResponse(response, modal, submit_info_box_id, form_id){
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
    $('#' + submit_info_box_id).html(errors).prop('style', 'display: block;');
  } else {
    clearForm(form_id);
    if (modal){
      modal.hide();
    }
  }
};





// Altering new workshop modal close button based on the way it was opened
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

// Clears workshop form when leaving modal
$(function(){
  $('#new_workshop_modal').on('hidden.bs.modal', function () {
    clearForm('new_workshop_form');
  });
});

// Loads content of the workshop details modal
$(function() {  
    $('.workshop-list').on('click', '.show-workshop-details', function(){
      var url = $(this).data('url');
      $('#workshop_details_modal_content').load(url);
    });
});

// Assigns redirect action to dismissing workshop details modal
$(function(){
  $('#workshops_list_modal').on('click', '.set-modal-redirect', function(){
    $('#workshop_details_modal').data('modal-redirect', true);
    $('.redirect-to-workshop-list').html('Go back');
  });
});

// Handling wheter to close modal or redirect to previous one
$(function() {
  var modal = new bootstrap.Modal($("#workshop_details_modal"));

  $('#workshop_details_modal').on('click', '.redirect-to-workshop-list', function() {
    modal.hide();
    if ($('#workshop_details_modal').data('modal-redirect') == true){
      var newModal = new bootstrap.Modal($("#workshops_list_modal"));
      newModal.show();
      $('#workshop_details_modal').removeData('modal-redirect');
    }
  });
});

// Workshops filtering reset
$(function(){
  $('.reset-workshop-filter').on('click', function(){
    $('#workshops_list').load($('#workshops_list').data('url'));
  });
});

// Workshops filtering
$(function(){
  $('.apply-workshop-filter').on('click', function(event){
    event.preventDefault();
    $('#workshops_list').load($('#workshops_list').data('url') + $('#workshop_filter_category').val() + '/' + $('#workshop_filter_phrase').val());
  });
});

// Entries details load
$(function(){
  $('#entries_list').on('click', '.entry-details', function(){
    $('#entry_details_modal_content').load($(this).data('url'));
  });
});

// Entries filtering
$(function(){
  $('.apply-entries-filter').on('click', function(event){
    event.preventDefault();
    let url = [$(this).data('url').slice(0, -1)];
    let args = [$('#entries_category_filter').val(), $('#entries_search_phrase').val()]

    args.forEach(function(element) {
      element !== "" ? url.push(element) : url.push('__null');
    });
    console.log(url.join('/'));
    $('#entries_list').load(url.join('/'));
  });
});

// // Reminders details load
// $(function(){
//   $('#entries_list').on('click', '.entry-details', function(){
//     $('#entry_details_modal_content').load($(this).data('url'));
//   });
// });

// Handles new workshop creation request
$(function() {  
  var modal = new bootstrap.Modal($("#new_workshop_modal"));

    $(".save-new-workshop").on("click", function(event) {
      event.preventDefault();

      if (!validateWorkshopData('new_workshop_submit_info', 'new_workshop_form')){
        return false;
      }

      $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: $('#new_workshop_form').serializeArray(),
        success: function(response) {
          handleAjaxResponse(response, modal, 'new_workshop_submit_info', 'new_workshop_form', 'new_workshop_form');
          refreshWorkshopsLists();
          var message = $(
            '<div id="workshop_message" class="alert alert-success" role="alert" style="display: block;">\
              Workshop created!\
              <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>'
          );
          modal.hide();
          if ($('#workshop_details_modal').data('modal-redirect') == true){
            var newModal = new bootstrap.Modal($("#workshops_list_modal"));
            newModal.show();
            $('#workshop_details_modal').removeData('modal-redirect');
            clearForm('new_workshop_form');
            $('#workshops_list_messages_box').append(message);
          } else {
            $('#messages_box').append(message);
          }
        }
      });
    });
});

// Handles workshop edit request
$(function() {
  var modal = new bootstrap.Modal($("#workshop_details_modal"));

  $('#workshop_details_modal').on('click', '.save-edit-workshop-data', function(event) {
    event.preventDefault();
  
    if (!validateWorkshopData('edit_workshop_submit_info', 'edit_workshop_form')){
      return false;
    }
  
    $.ajax({
      type: "POST",
      url: $(this).data('url'),
      data: $('#edit_workshop_form').serializeArray(),
      success: function(response) {
        handleAjaxResponse(response, modal, 'edit_workshop_submit_info', 'edit_workshop_form');
        refreshWorkshopsLists();
        var message = $(
          '<div id="workshop_message" class="alert alert-success" role="alert" style="display: block;">\
            Workshop data edited!\
            <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
          </div>'
        );
        $('#workshop_data').load($('#workshop_data').data('url'));
        $('#messages_box').append(message);
      }
    });
  });
});

// Toggling favourite workshop option
$(function(){
  $('#workshop_details_modal').on('click', '.toggle-favourite-workshop', function(){
    var $this = $(this);

    $.ajax({
      type: "POST",
      url: $this.data('url'),
      data: $('#edit_workshop_form').serializeArray(),
      success: function(response) {
        if (response['status'] == 'success'){
          if (response['state'] == 'untoggled'){
            $('#favourite_workshop_toggle_button').html('<i class="bi bi-star"></i> Add to favourites');
            $this.data('favourite', false);
          } else if (response['state'] == 'toggled') {
            $('#favourite_workshop_toggle_button').html('<i class="bi bi-star-fill"></i> Delete from favourites');
            $this.data('favourite', true);
          }
        }
        refreshWorkshopsLists();
      }
    });
  });
});

// Deleting workshop
$(function(){
  $('#workshop_details_modal_content').on('click', '.delete-workshop', function(){
    if ($(this).data('confirmed') != true){
      $(this).popover('show')
        .html('Yes')
        .data('confirmed', true)
        .attr('data-bs-dismiss', 'modal')
    } else{
      var $this = $(this);

      $.ajax({
        type: "GET",
        url: $this.data('url'),
        success: function(response) {
          if (response['status'] == 'success'){
            var message = $(
              '<div id="workshop_message" class="alert alert-success" role="alert" style="display: block;">\
                Workshop deleted.\
                <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
              </div>'
            );
            refreshWorkshopsLists();
            $('.popover').remove();
            if ($('#workshop_details_modal').data('modal-redirect') == true){
              var newModal = new bootstrap.Modal($("#workshops_list_modal"));
              $('#workshops_list_messages_box').append(message);
              $('#workshop_details_modal').removeData('modal-redirect');
              newModal.show();
            } else {
              $('#messages_box').append(message);
            }
          }
        }
      });
    }
  });
});

// Toggle favourite car
$(function(){
  $('.car-toggle-favourite').on('click', function(event){
    event.preventDefault();
    var $this = $(this);
    var carId = $this.data('carId');
    
    $.ajax({
      type: "POST",
      data: $('#favourite_car_form_' + carId).serializeArray(),
      url: $this.data('url'),
      success: function(response) {
        if (response['status'] == 'failed'){
          let error_dismiss_button = '<button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>';
          $('#favourite_car_error_box').html(response['error'] + error_dismiss_button).prop('style', 'display: block;');
        } else {
          let current_favourite_car = $('.favourite-car');

          if ($this.hasClass('favourite-car')){
            $this.removeClass('favourite-car').html('<i class="bi bi-star"></i>');
          } else {
            current_favourite_car.removeClass('favourite-car').html('<i class="bi bi-star"></i>');
            $this.addClass('favourite-car').html('<i class="bi bi-star-fill"></i>');
          }  
        }
      }
    });
  });
});

// Handles new entry creation request
$(function() {  
  var modal = new bootstrap.Modal($("#new_entry_modal"));

    $(".save-new-entry").on("click", function(event) {
      event.preventDefault();

      // if (!validateEntryData('new_entry_submit_info', 'new_entry_form')){
        // return false;
      // }


      $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: $('#new_entry_form').serializeArray(),
        success: function(response) {
          handleAjaxResponse(response, modal, 'new_entry_submit_info', 'new_entry_form');
          var message = $(
            '<div id="workshop_message" class="alert alert-success" role="alert" style="display: block;">\
              Entry created!\
              <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>'
          );
          modal.hide();
          $('#entries_list').load($('#entries_list').data('url'));
          $('#messages_box').append(message);
        }
      });
    });
});

// Handles edit entry request
$(function() {  
  // var modal = new bootstrap.Modal($("#new_entry_modal"));
  $('#entry_details_modal_content').on('click', ".save-edit-entry", function(){
    var $this = $(this);

      // if (!validateEntryData('new_entry_submit_info', 'new_entry_form')){
        // return false;
      // }


    $.ajax({
      type: "POST",
      url: $(this).data('url'),
      data: $('#edit_entry_form').serializeArray(),
      success: function(response) {
        handleAjaxResponse(response, null, 'edit_entry_submit_info', 'edit_entry_form');
        var message = $(
          '<div id="workshop_message" class="alert alert-success" role="alert" style="display: block;">\
            Entry edited!\
            <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
          </div>'
        );
        // modal.hide();
        $('#entries_list').load($('#entries_list').data('url'));
        $('#entry_details_modal_content').load($this.data('refresh-url'));
        $('#messages_box').append(message);
      }
    });
  });
});

// Deleting entry
$(function(){
  $('#entry_details_modal_content').on('click', '.delete-entry', function(){
    if ($(this).data('confirmed') != true){
      $(this).popover('show')
        .html('Yes')
        .data('confirmed', true)
        .attr('data-bs-dismiss', 'modal')
    } else{
      var $this = $(this);

      $.ajax({
        type: "GET",
        url: $this.data('url'),
        success: function(response) {
          if (response['status'] == 'success'){
            var message = $(
              '<div id="entry_message" class="alert alert-success" role="alert" style="display: block;">\
                Entry deleted.\
                <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
              </div>'
            );
            $('#entries_list').load($('#entries_list').data('url'));
            $('.popover').remove();
            $('#messages_box').append(message);
          }
        }
      });
    }
  });
});

// Handles new reminder creation request
$(function() {  
  var modal = new bootstrap.Modal($("#new_reminder_modal"));

    $(".save-new-reminder").on("click", function(event) {
      event.preventDefault();

      // if (!validateReminderData('new_reminder_submit_info', 'new_reminder_form')){
        // return false;
      // }

      $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: $('#new_reminder_form').serializeArray(),
        success: function(response) {
          handleAjaxResponse(response, modal, 'new_reminder_submit_info', 'new_reminder_form');
          var message = $(
            '<div id="workshop_message" class="alert alert-success" role="alert" style="display: block;">\
              Reminder created!\
              <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>'
          );
          modal.hide();
          console.log($('#reminders_list').data('url'));
          $('#reminders_list').load($('#reminders_list').data('url'));
          $('#messages_box').append(message);
        }
      });
    });
});
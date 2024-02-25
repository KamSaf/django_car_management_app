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
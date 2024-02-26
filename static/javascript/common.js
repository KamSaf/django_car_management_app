// Clears currently displayed errors
function clearErrors(){
  $('.alert-danger').prop('style', 'display: none;');
  $('.is-invalid').removeClass('is-invalid');
}

$(function() {
    $(".clear-errors").on("click", function() {
      clearErrors();
      $('.alert-success').prop('style', 'display: none;');
    });
});
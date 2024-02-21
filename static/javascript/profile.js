$(function() {
    $(".delete-profile-button").on("click", function() {
      var modal = new bootstrap.Modal(document.getElementById("confirm_delete_modal"));
      modal.show();
    });

    $(".confirm-delete-profile-button").on("click", function() {
      var userId = $(this).data("userId");
      
    //   $.ajax({
    //     type: "POST",
    //     url: "",
    //     data: {
    //       postId: postId
    //     },
    //     success: function(response) {
    //       $("#post_" + postId).remove();
    //       modal.hide();
    //     }
    //   });
    });
});

$(function() {
    $(".edit-profile-button").on("click", function() {
      var modal = new bootstrap.Modal(document.getElementById("edit_profile_modal"));
      modal.show();
    });

//   $(".save-edit-profile-button").on("click", function(event) {
//     event.preventDefault();

//       $.ajax({
//         type: "POST",
//         url: "/edit_profile",
//         data: $('form').serializeArray(),
//         success: function(response) {
//           console.log(response);
//         }
//       });
//   });
});
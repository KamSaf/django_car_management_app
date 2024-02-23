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
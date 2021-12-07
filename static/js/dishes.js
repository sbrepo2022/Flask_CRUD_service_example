$(function() {
    $('[data-action="delete-dish"]').on('click', function() {
        $.ajax({
            url: `/dishes/${$(this).data('id')}`,
            method: 'delete',
            success: function(data) {
                window.location.replace('/dishes');
            }
        });
    });

    $('[data-action="edit-dish"]').on('click', function() {
        $('#dishCreateNew').prop('checked', false);
        $('#dishId').val($(this).data('id'));
        $('#dishTitle').val($(this).data('title'));
        $('#dishCost').val($(this).data('cost'));
    });

    $('[data-action="add-dish"]').on('click', function() {
        $('#dishCreateNew').prop('checked', true);
        $('#dishId').val('');
        $('#dishTitle').val('Блюдо');
        $('#dishCost').val(100);
    });

    $('#dishForm').on('submit', function(e) {
        let method = $('#dishCreateNew').is(':checked') ? 'post' : 'put';
        let url = '/dishes' + (method == 'put' ? '/' + $('#dishId').val() : '');

        $.ajax({
            url: url,
            method: method,
            dataType: 'json',
            data: JSON.stringify({
                'title': $('#dishTitle').val(),
                'cost': $('#dishCost').val()
            }),
            contentType: 'application/json; charset=utf-8',
            success: function(data){
                window.location.replace('/dishes');
            }
        });

        e.preventDefault();
    });
});
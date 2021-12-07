$(function() {
    $('[data-action="delete-position"]').on('click', function() {
        $.ajax({
            url: '/orders/basket',
            method: 'delete',
            dataType: 'json',
            data: JSON.stringify({
                'dish_id': $(this).data('id')
            }),
            contentType: 'application/json; charset=utf-8',
            success: function(data){
                window.location.replace('/orders');
            }
        });
    });

    $('[data-action="edit-position"]').on('click', function() {
        $('#positionCreateNew').val(false);
        $('#dishId').val($(this).data('id'));
        $('#dishAmount').val($(this).data('amount'));

        $('#dishTitle').html($(this).data('title'));

        $('#basketPositionModalLabel').html('Изменить позицию');
        $('#basketPositionModal').modal();
    });

    $('[data-action="add-position"]').on('click', function() {
        $('#positionCreateNew').val(true);
        $('#dishId').val($(this).data('id'));
        $('#dishAmount').val(1);

        $('#dishTitle').html($(this).data('title'));

        $('#basketPositionModalLabel').html('Добавить в корзину');
        $('#basketPositionModal').modal();
    });

    $('#basketPositionForm').on('submit', function(e) {
        let method = $('#positionCreateNew').val() == 'true' ? 'post' : 'put';
        let url = '/orders/basket';

        $.ajax({
            url: url,
            method: method,
            dataType: 'json',
            data: JSON.stringify({
                'dish_id': $('#dishId').val(),
                'amount': $('#dishAmount').val()
            }),
            contentType: 'application/json; charset=utf-8',
            success: function(data){
                window.location.replace('/orders');
            }
        });

        e.preventDefault();
    });

    $('[data-action="create-order"]').on('click', function() {
        let method = 'post';
        let url = '/orders/order';

        $.ajax({
            url: url,
            method: method,
            dataType: 'json',
            data: JSON.stringify({}),
            contentType: 'application/json; charset=utf-8',
            success: function(data) {
                window.location.replace('/orders');
            }
        });
    });

    $('[data-action="delete-order"]').on('click', function() {
        let method = 'delete';
        let url = '/orders/order';

        $.ajax({
            url: url,
            method: method,
            dataType: 'json',
            data: JSON.stringify({
                'order_id': $(this).data('id')
            }),
            contentType: 'application/json; charset=utf-8',
            success: function(data) {
                window.location.replace('/orders');
            }
        });
    });

    $('[data-action="details-order"]').on('click', function() {
        let method = 'get';
        let url = `/orders/order?order_id=${$(this).data('id')}`;

        let that = this;
        $.ajax({
            url: url,
            method: method,
            success: function(data) {
                result = data.order_dishes;
                html_insert = '';

                for (let i in result) {
                    html_insert += '<tr>';
                    for (let j in result[i]) {
                        html_insert += `<td>${result[i][j]}</td>`;
                    }
                    html_insert += '</tr>';
                }

                $('#orderDetailsModal tbody').html(html_insert);
                $('#orderId').html($(that).data('id'));
                $('#orderDate').html($(that).data('date'));
                $('#orderCost').html($(that).data('cost'));
                $('#customerId').html($(that).data('c-id'));
                $('#orderDetailsModal').modal();
            }
        });
    });
});
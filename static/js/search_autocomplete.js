$(document).ready(function() {
    $('#search-form').on('input', function() {
        let query = $(this).val();
        if (query.length < 1) {
            $('#search-suggestions').empty().hide();
            return;
        }
        $.get('/catalog/ajax_search_products/', {q: query}, function(data) {
            let html = '';
            if (data.categories.length) {
                html += '<div class="suggest-title">Categories</div><ul class="list-group">';
                html += data.categories.map(item =>
                    `<li class="list-group-item"><a href="/catalog?category=${item.id}">${item.name}</a></li>`
                ).join('');
                html += '</ul>';
            }
            if (data.products.length) {
                html += '<div class="suggest-title">Products</div><ul class="list-group">';
                html += data.products.map(item =>
                    `<li class="list-group-item"><a href="/catalog/${item.id}/">${item.name}</a></li>`
                ).join('');
                html += '</ul>';
            }
            $('#search-suggestions').html(html).show();
        });
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest('#search-suggestions, #search-form').length) {
            $('#search-suggestions').empty().hide();
        }
    });
});
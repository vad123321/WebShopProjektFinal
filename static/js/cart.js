$(document).ready(() => {
    // Check:
    console.log('cart.js -> Start');

    // Key Event:
    $('#gallery').on('click', '.add-to-cart-btn', (event) => {
        // 1
        console.log('add-btn -> Click');

        // 2
        let userId = $('#user-id').val();
        console.log('userId: ', userId);

        // 3
        if (userId == 'None') {
            alert('To use the cart you must be logged in.');
        } else {
            //4
            // let productId = $(event.target).prev().val();
            let productId = $(event.target).closest('.add-to-cart').find('.product-id').val();
            console.log('productId: ', productId);

            //5
            let productCard = $(event.target).closest('.product-card');
            let priceText = productCard.find('.item-price').text();
            let productPrice = parseFloat(priceText.replace('$', '').replace(',', '.'));
            console.log('productPrice: ', productPrice);
            // let productPrice = parseFloat($(event.target).parent().prev().find('h4').text());
            // console.log('productPrice: ', productPrice);
            // let productPrice = parseFloat($(event.target).closest('.add-to-cart').find('.product-price').val());
            // let productCard = $(event.target).closest('.product-card');
            // let productPrice = parseFloat(priceText.replace('$', '').replace(',', '.'));
            // let priceText = productCard.find('.item-price').text();
            // let productPrice = parseFloat(priceText.replace('$', '').replace(',', '.'));
            // console.log('productPrice: ', productPrice);

            // !!! AJAX - REQUEST TO SERVER TO SAVE THE PRODUCT IN THE DB (CART TABLE):
            $.ajax({
                url: '/orders/ajax_cart',
                data: `uid=${userId}&pid=${productId}&price=${productPrice}`,
                success: (result) => {
                    console.log('AJAX -> OK');
                    console.log(result.message);
                    console.log('Check data:');
                    // ->
                    console.log('uid', result.uid);
                    console.log('pid', result.pid);
                    console.log('price', result.price);
                    // ->
                    $('#count').text(result.count);
                    $('#_count').text(`Items in cart: ${result.count} шт`);
                    $('#_amount').text(`Cost: ${result.amount} $`);
                }
            });
        }
    });
});

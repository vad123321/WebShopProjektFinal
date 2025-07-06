$(document).ready(() => {
    // Check:
    console.log('cart.js -> Start');

    // Key Event:
    $('#gallery').on('click', '.add-to-cart-btn', (event) => {
        // 1
        console.log('add-btn -> Click');

        // 2
        let productId = $(event.target).prev().val();
        console.log('productId: ', productId);
    });
});
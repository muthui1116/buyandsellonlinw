$(document).ready(function(){
    // add to cart 
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

    
        $.ajax({
            type: 'GET',
            url: url,
           
            success: function(response){
               console.log(response)   
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = "/login/"
                    })
                }if(response.status == 'failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+item_id).html(response.qty);

                    // subtotal, tax and grand_total
                    applyCartAmaunts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                }
            }
        })
    })

    // place the cart item quatinty on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty) 
    })

    // decrease cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();

        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

    
        $.ajax({
            type: 'GET',
            url: url,
           
            success: function(response){
                //Sconsole.log(response) 
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = "/login/"
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+item_id).html(response.qty);

                    // subtotal, tax and grand_total
                    applyCartAmaunts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )

                    if(window.location.pathname == '/cart/'){
                        removeCardItem(response.qty, cart_id); 
                        checkEmptyCart();
                    }  
                }
            }
        })
    })

    // Delete cart item
    $('.delete_cart').on('click', function(e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

    
        $.ajax({
            type: 'GET',
            url: url,
           
            success: function(response){
                //Sconsole.log(response) 
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, 'success')

                        // subtotal, tax and grand_total
                        applyCartAmaunts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax'],
                            response.cart_amount['grand_total'],
                        )

                    removeCardItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
    })

    // Delete the cart element if the qty is 0
    function removeCardItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
            // Remove cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    // Check if the cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById('empty-cart').style.display = 'block';
        }
    }

    // Apply cart amounts
    function applyCartAmaunts(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }  
    }
});

let updateButtons = document.querySelectorAll('.product-btn');

let cartIcon = document.querySelector('#cart-length');
let cartItems = Object.keys(cart).length - 1;


if (cartItems < 0) {
    cartItems = 0;
}

cartIcon.innerHTML = cartItems;





for (let i=0;i<updateButtons.length; i++) {
    let button = updateButtons[i];
    button.addEventListener('click', updateCart);
}

function updateCart(){
    let productId = this.dataset.product;
    let action = this.dataset.action;

    console.log('button was clicked')
    processUpdate(productId, action);
    updateCartIcon();
}

function processUpdate(productId, action) {

    console.log('adding item ..')

    if (cart['orderId'] == undefined) {
        cart['orderId'] = 'none';
    }

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        }else {
            cart[productId]['quantity'] += 1;
        }

        console.log('item was added...')
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] < 0) {
            console.log('deleting item...');
            delete cart[productId];
            console.log('item was deleted')
        }

        console.log('item was removed...')
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
}

function updateCartIcon() {
    cartIcon = document.querySelector('#cart-length');
    cartItems = Object.keys(cart).length - 1;
    
    cartIcon.innerHTML = cartItems;
}



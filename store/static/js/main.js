// Nav

const hamNav = document.querySelector('#check');
const priNav = document.querySelector('.primary-navigation');

hamNav.addEventListener('change', changeNav);

function changeNav(){
    const visibility = priNav.getAttribute('data-visible');
    if (this.checked){
        if (visibility === 'false') {
            priNav.setAttribute('data-visible', true);
        }
    } else{
        if (visibility === 'true') {
            priNav.setAttribute('data-visible', false);
        }
    }
    }

// Update Cart

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
    console.log(cart)
    if (cart['orderId'] == undefined) {
        cart['orderId'] = 'none';
    }
    console.log(cart)

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




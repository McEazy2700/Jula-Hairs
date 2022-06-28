// Display the form or not
let formDiv = document.querySelector('.form')


if ((Object.keys(cart).length - 1) <=0) {
    formDiv.classList.add('hidden')
}


// Checkout

let checkoutBtn = document.querySelector('#checkout-btn');

let form = document.querySelector('#form');

form.addEventListener('submit', function(e){
    e.preventDefault();
    payWithPaystack()
})

function payWithPaystack() {
    let handler = PaystackPop.setup({
        key: payStackPubKey, // Replace with your public key
        email: form.email.value,
        amount: orderAmount * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit
        currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars
        ref: transaction_ref, // Replace with a reference you generated
        callback: function(response) {
            //this happens after the payment is completed successfully
            let reference = response.reference;
            alert('Payment complete! Reference: ' + reference);
            completeOrder()
          // Make an AJAX call to your server with the reference to verify the transaction
        },
        onClose: function() {
          alert('Transaction was not completed, window closed.');
        },
      });
      handler.openIframe();
}

function completeOrder() {
    console.log('button was clicked')


    let formData = {
        'first_name': form.first_name.value,
        'last_name': form.last_name.value,
        'email': form.email.value,
        'phone': form.phone.value,
        'name': form.address.value,
        'state': form.state.value,
        'city': form.city.value
    }

    console.log(formData)

    let orderId = cart['orderId']
    console.log(orderId)

    let csrfToken = form.csrfmiddlewaretoken.value;

    console.log(transaction_ref)

    url = `/process_order/${transaction_ref}/`

    fetch (url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': csrfToken,
        }, 
        body: JSON.stringify({'form_data': formData, 'orderId': orderId})
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log(data)
        if (data['status'] == 'success') {

            cart = {};
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

            alert('Transaction Complete');
            console.log('Success');
            console.log(cart);

            window.location.href = '/'
        }
    })
}
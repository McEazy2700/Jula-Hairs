// Display the form or not

if ((Object.keys(cart).length - 1) <=0) {
    formDiv.classList.add('hidden')
}


// Checkout

let checkoutBtn = document.querySelector('#checkout-btn');

let form = document.querySelector('#form');

form.addEventListener('submit', function(e){
    e.preventDefault()
    completeOrder()
})

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
    console.log(csrfToken)

    url = '/process_order/'

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
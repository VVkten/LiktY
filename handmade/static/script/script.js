const decreaseButtons = document.querySelectorAll('.decrease');
const increaseButtons = document.querySelectorAll('.increase');
const quantityInputs = document.querySelectorAll('.quantity-input');
const totalPriceDisplay = document.getElementById('totalPrice');
const buyButton = document.getElementById('buyButton');
const orderButton = document.getElementById('order-button');
const orderForm = document.getElementById('order-form');
const csrfToken = getCookie('csrftoken');
const addToCartUrl = "/add_to_cart/";
const removeFromCartUrl = "/remove_from_cart/";

function updateTotal() {
    let total = 0;

    quantityInputs.forEach(input => {
        const price = parseFloat(input.getAttribute('data-price'));
        const quantity = parseInt(input.value, 10) || 0;
        total += price * quantity;
    });

    if (totalPriceDisplay) {
        totalPriceDisplay.textContent = total.toFixed(2);
    } else {
        console.error('Element with ID "totalPrice" not found.');
    }
}

decreaseButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        const input = quantityInputs[index];
        if (input.value > 1) {
            input.value = parseInt(input.value, 10) - 1;
            updateTotal();
        }
    });
});

increaseButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        const input = quantityInputs[index];
        if (input.value < parseInt(input.max, 10)) {
            input.value = parseInt(input.value, 10) + 1;
            updateTotal();
        }
    });
});

updateTotal();

if (buyButton) {
    buyButton.addEventListener('click', function () {
        const selectedItems = Array.from(quantityInputs).map(input => ({
            productId: input.closest('.cart-item').getAttribute('data-product-id'),
            quantity: parseInt(input.value, 10)
        }));

        localStorage.setItem('selectedItems_cart', JSON.stringify(selectedItems));

        window.location.href = '/order/';
    });
}

if (orderForm) {
    orderForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const storedItems = localStorage.getItem('selectedItems_cart');
        const selectedItems_cart = storedItems ? JSON.parse(storedItems) : [];

        if (selectedItems_cart.length === 0) {
            alert("Виберіть хоча б один товар для замовлення.");
            return;
        }

        const address = orderForm.querySelector('input[name="address"]').value;
        const postalCode = orderForm.querySelector('input[name="postal_code"]').value;

        const orderData = {
            items: selectedItems_cart,
            shipping_address: address,
            city_postal_code: postalCode
        };

        fetch('/order_form/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                localStorage.removeItem('selectedItems_cart');
                window.location.href = `/success/`;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addToCart(productId) {
    fetch(addToCartUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.status === 'success') {
            alert(data.message);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function removeFromCart(productId) {
    fetch(removeFromCartUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            updateTotal();
            const cartItem = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
            if (cartItem) {
                cartItem.remove();
                updateTotal();
                location.reload();
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
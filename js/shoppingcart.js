// get the Add to Cart button element
const addToCartBtn = document.querySelector('.add-to-cart-btn');

// add a click event listener to the Add to Cart button
addToCartBtn.addEventListener('click', (event) => {
  event.preventDefault(); // prevent the default form submit behavior

  // get the item details from the DOM
  const name = document.querySelector('.item-name').textContent;
  const price = parseFloat(document.querySelector('.item-price').textContent);
  const quantity = parseInt(document.querySelector('.item-quantity').value);

  // create a data object to send in the request body
  const data = {
    name: name,
    price: price,
    quantity: quantity
  };

  // send a POST request to the /add-to-cart endpoint
  fetch('/add-to-cart', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.text())
  .then(data => {
    console.log(data); // log the response from the server
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
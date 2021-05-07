"use strict";

let updateBtns = document.getElementsByClassName("update-cart"); // Getting all buttons with "update-cart" class.

// For every update button add event listener.
for (let i = 0; i < updateBtns.length; i++) {
   updateBtns[i].addEventListener("click", function () {
      let productId = this.dataset.product; // Getting product id from data-product atrebute.
      let action = this.dataset.action; // Getting action from data-action atrebute.

      if (user === "AnonymousUser") addCookieItem(productId, action);
      // For guest user using addCookieItem().
      else updateUserOrder(productId, action); // For auth user using updateUserOrder().
   });
}

// Add product and product quantity to Cookie json.
function addCookieItem(productId, action) {
   // If data-action was "add".
   if (action == "add") {
      if (cart[productId] == undefined) cart[productId] = { quantity: 1 };
      // If there is no any products in the cart: Add +1.
      else cart[productId]["quantity"]++; // If there is at least one product in the cart: increment quantity.
   }
   // If data-action was "remove".
   if (action == "remove") {
      cart[productId]["quantity"]--; // Decrement quantity.

      if (cart[productId]["quantity"] <= 0) delete cart[productId]; // If quantity less or equall 0 delete product form Cookie.
   }
   document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"; // Add cookie based in productId, action and product quantity.
   location.reload();
}

// Craate Fetch promise with POST request to server with header parametrs and json in body.
function updateUserOrder(productId, action) {
   let url = "/update_item/"; // The beginig of request

   // Fetc(<begiging url>, request parameters)
   fetch(url, {
      // Method type
      method: "POST",
      // Format and security token params
      headers: {
         "Content-Type": "application/json",
         "X-CSRFToken": csrftoken,
      },
      // Json body
      body: JSON.stringify({
         productId: productId,
         action: action,
      }),
   })
      // Promise state handler: Returns JSON response
      .then((response) => response.json())
      // Promise state handler: Do page redirect
      .then((response) => {
         location.reload();
      });
}

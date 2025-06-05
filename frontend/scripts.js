// scripts.js

// Example: Add click event to the "Shop Now" buttons
document.addEventListener("DOMContentLoaded", () => {
  const shopButtons = document.querySelectorAll('.btn-shop, .shop-now');

  shopButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      alert('Shop Now button clicked!');
    });
  });
});

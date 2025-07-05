document.addEventListener('DOMContentLoaded', function() {
    // The Stripe handling is mostly done server-side in this implementation
    // The checkout button click is handled in customer.js

    // Check if we're coming back from Stripe with a success or cancel
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');

    if (sessionId && window.location.pathname === '/payment-success') {
        // Payment was successful
        console.log('Payment successful with session ID:', sessionId);
    }
});
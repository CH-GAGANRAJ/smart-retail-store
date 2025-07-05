document.addEventListener('DOMContentLoaded', function() {
    const scannerMessageElem = document.getElementById('scannerMessage');

    // Basic authentication check
    const userId = localStorage.getItem('user_id');
    const userRole = localStorage.getItem('user_role');

    if (!userId || userRole !== 'customer') {
        console.warn('User not authenticated as customer. Redirecting to login.');
        window.location.href = '/login'; // Redirect to login if not authenticated as customer
        return; // Stop further execution
    }

    document.getElementById('logoutButton').addEventListener('click', function() {
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_role');
        window.location.href = '/login';
    });

    const html5QrCode = new Html5Qrcode("reader");
    const qrCodeSuccessCallback = async (decodedText, decodedResult) => {
        // Stop scanning once a QR code is successfully decoded
        html5QrCode.stop().then(() => {
            scannerMessageElem.textContent = `QR Code Scanned: ${decodedText}`;
            scannerMessageElem.classList.remove('alert-info', 'alert-danger');
            scannerMessageElem.classList.add('alert-success'); // Indicate success
            // Pass the decodedText (which is the product URL) to fetch product details
            fetchProductDetails(decodedText);
        }).catch((err) => {
            console.error("Failed to stop scanning:", err);
            scannerMessageElem.textContent = "Error: Failed to stop scanner. " + err.message;
            scannerMessageElem.classList.remove('alert-info', 'alert-success');
            scannerMessageElem.classList.add('alert-danger');
        });
    };

    const config = { fps: 10, qrbox: { width: 250, height: 250 } };

    // Start scanning when the page loads
    html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback)
        .catch((err) => {
            console.error("Unable to start scanning:", err);
            scannerMessageElem.textContent = "Error: Unable to start camera. Please ensure camera access is granted and no other application is using the camera. Details: " + err.message;
            scannerMessageElem.classList.remove('alert-info', 'alert-success');
            scannerMessageElem.classList.add('alert-danger');
        });

    const productDetailsSection = document.getElementById('productDetailsSection');
    const productNameElem = document.getElementById('productName');
    const productPriceElem = document.getElementById('productPrice');
    const productImageElem = document.getElementById('productImage');
    const aiSummaryElem = document.getElementById('aiSummary');
    const usageTipsElem = document.getElementById('usageTips');
    const keyFeaturesElem = document.getElementById('keyFeatures');
    const addToCartButton = document.getElementById('addToCartButton');
    const viewProductUrlButton = document.getElementById('viewProductUrlButton');

    let currentProductId = null; // To store the product ID for adding to cart

    async function fetchProductDetails(productUrl) { // Renamed parameter to productUrl
        try {
            scannerMessageElem.textContent = 'Fetching product details...';
            scannerMessageElem.classList.remove('alert-success', 'alert-danger');
            scannerMessageElem.classList.add('alert-info');

            const response = await fetch(`/customer/product-by-url?product_url=${encodeURIComponent(productUrl)}`);
            const data = await response.json();

            if (response.ok) {
                currentProductId = data.product.id; // Store actual product ID for add to cart
                const product = data.product;
                const aiReview = data.ai_review;

                productNameElem.textContent = product.name;
                productPriceElem.textContent = `$${product.price.toFixed(2)}`;
                productImageElem.src = product.QR ? `/static/${product.QR}` : 'https://placehold.co/300x300/e0e0e0/ffffff?text=Product+Image';
                productImageElem.alt = product.name;

                aiSummaryElem.textContent = aiReview.Summary || 'No summary available.';

                usageTipsElem.innerHTML = '';
                if (aiReview['Usage Tips'] && Array.isArray(aiReview['Usage Tips'])) {
                    aiReview['Usage Tips'].forEach(tip => {
                        const li = document.createElement('li');
                        li.textContent = `- ${tip}`;
                        usageTipsElem.appendChild(li);
                    });
                } else {
                    usageTipsElem.innerHTML = '<li>No usage tips available.</li>';
                }

                keyFeaturesElem.innerHTML = '';
                if (aiReview.Features && Array.isArray(aiReview.Features)) {
                    aiReview.Features.forEach(feature => {
                        const li = document.createElement('li');
                        li.textContent = `- ${feature}`;
                        keyFeaturesElem.appendChild(li);
                    });
                } else {
                    keyFeaturesElem.innerHTML = '<li>No key features available.</li>';
                }

                viewProductUrlButton.onclick = () => window.open(product.product_url, '_blank');

                productDetailsSection.classList.remove('d-none');
                scannerMessageElem.textContent = 'Product details loaded successfully.';
                scannerMessageElem.classList.remove('alert-info', 'alert-danger');
                scannerMessageElem.classList.add('alert-success');

            } else {
                productDetailsSection.classList.add('d-none');
                scannerMessageElem.textContent = data.detail || 'Product not found.';
                scannerMessageElem.classList.remove('alert-info', 'alert-success');
                scannerMessageElem.classList.add('alert-danger');
            }
        } catch (error) {
            console.error('Error fetching product details:', error);
            productDetailsSection.classList.add('d-none');
            scannerMessageElem.textContent = 'An error occurred while fetching product details: ' + error.message;
            scannerMessageElem.classList.remove('alert-info', 'alert-success');
            scannerMessageElem.classList.add('alert-danger');
        }
    }

    addToCartButton.addEventListener('click', async function() {
        if (!currentProductId) {
            alert('No product selected to add to cart.'); // Replace with custom modal later
            return;
        }

        try {
            const response = await fetch('/customer/add-to-cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: parseInt(userId), product_id: parseInt(currentProductId), quantity: 1 })
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.message); // Replace with custom modal later
                // Optionally, update cart count in UI
            } else {
                alert(data.detail || 'Failed to add product to cart.'); // Replace with custom modal later
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert('An error occurred while adding to cart.'); // Replace with custom modal later
        }
    });
});

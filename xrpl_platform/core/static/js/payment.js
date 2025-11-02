document.addEventListener('DOMContentLoaded', () => {
    // Get all the elements we need to interact with
    const payButton = document.getElementById('pay-button');
    const qrContainer = document.getElementById('qr-container');
    const qrImage = document.getElementById('qr-image');
    const loadingMessage = document.getElementById('loading');
    const messageContainer = document.getElementById('message-container');

    let pollingInterval; // To store the interval timer

    // Helper function to get Django's CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add click event to the payment button
    payButton.addEventListener('click', createPaymentRequest);

    /**
     * Step 1: Call the backend to create a new payment payload.
     */
    async function createPaymentRequest() {
        // Reset the UI
        payButton.disabled = true;
        loadingMessage.classList.remove('hidden');
        qrContainer.classList.add('hidden');
        messageContainer.textContent = '';
        if (pollingInterval) clearInterval(pollingInterval);

        try {
            // This is the backend API endpoint you will need to create.
            // We use POST as we are creating a new payment request.
            const response = await fetch('/api/v1/payments/initiate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Required for Django POST
                },
                body: JSON.stringify({
                    // You can send payment details here if needed,
                    // e.g., amount: '1', currency: 'XRP'
                })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Check if we got the expected data from our backend
            if (data.qr_png && data.uuid) {
                // We got it! Show the QR code
                qrImage.src = data.qr_png;
                qrContainer.classList.remove('hidden');
                
                // Start checking for the payment status
                startPolling(data.uuid);
            } else {
                // Show an error if the backend didn't return what we need
                messageContainer.textContent = 'Error: Could not retrieve QR code.';
            }

        } catch (error) {
            console.error('Error creating payment request:', error);
            messageContainer.textContent = 'An error occurred. Please try again.';
        } finally {
            // Hide loading message and re-enable button
            loadingMessage.classList.add('hidden');
            payButton.disabled = false;
        }
    }

    /**
     * Step 2: Poll the backend to check the status of the payment.
     * @param {string} payloadUuid - The UUID of the payload we are checking.
     */
    function startPolling(payloadUuid) {
        pollingInterval = setInterval(async () => {
            try {
                // This is the second API endpoint you'll need to create.
                // It takes the UUID and checks its status.
                const response = await fetch(`/api/v1/payments/status/${payloadUuid}/`);
                const data = await response.json();

                // 'resolved' means the user has signed or rejected
                if (data.resolved) {
                    clearInterval(pollingInterval); // Stop checking
                    qrContainer.classList.add('hidden'); // Hide the QR code

                    if (data.signed) {
                        // Payment was successful
                        messageContainer.textContent = 'Success! Payment has been signed.';
                        messageContainer.style.color = 'green';
                    } else {
                        // Payment was rejected
                        messageContainer.textContent = 'Payment was rejected by the user.';
                        messageContainer.style.color = 'red';
                    }
                }
                // If not resolved, the loop will just continue
                
            } catch (error) {
                console.error('Error polling for status:', error);
                // If polling fails, stop to avoid flooding
                clearInterval(pollingInterval);
                messageContainer.textContent = 'Error checking payment status.';
            }
        }, 2000); // Check every 2 seconds
    }

    // Small helper to add/remove 'hidden' class
    // You can replace this with your own CSS logic
    const style = document.createElement('style');
    style.innerHTML = `.hidden { display: none; }`;
    document.head.appendChild(style);
});


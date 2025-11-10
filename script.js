document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const outputBox = document.getElementById('outputBox');

    let vehicleModels = [];
    let allVehicleModels = [];

    // Load and display all models on page load
    fetch('data/vehicle_listings.json')
        .then(res => res.json())
        .then(data => {
            vehicleModels = data.slice();
            allVehicleModels = data.slice();
            renderModelList();
        });

    function renderModelList() {
        outputBox.innerHTML = '';
        vehicleModels.forEach((model) => {
            const modelDiv = document.createElement('div');
            modelDiv.classList.add('model-listing');

            const link = document.createElement('a');
            link.href = model.url;
            link.textContent = model.model_name;
            link.target = '_blank';
            link.classList.add('model-link');

            modelDiv.appendChild(link);
            outputBox.appendChild(modelDiv);
        });
    }

    submitBtn.addEventListener('click', handleSubmit);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    });

    resetBtn.addEventListener('click', () => {
        vehicleModels = allVehicleModels.slice();
        renderModelList();
    });

 async function handleSubmit() {
        const query = userInput.value.trim();
        if (!query) return;

        userInput.value = '';

        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.textContent = query;

        // This function will now return `null` if there's an error
        const aiResponseText = await sendToPython(query);

        // *** ADD THIS CHECK ***
        // If the server failed, aiResponseText will be null.
        // Stop the function from running and crashing on .split().
        if (!aiResponseText) {
            console.error("Failed to get a valid response from the server.");
            // You could also show a message to the user here
            return; 
        }

        var newModels = [];
        // This line is now safe
        for (const modelName of aiResponseText.split(',').map(name => name.trim())) {
            const matchedModel = vehicleModels.find(m => m.model_name.toLowerCase() === modelName.toLowerCase());
            if (matchedModel) {
                newModels.push(matchedModel);
            }
        }
        vehicleModels = newModels;
        renderModelList();
    }

    async function sendToPython(textToSend) {
        try { // Add a try...catch block for network errors
            const response = await fetch("http://127.0.0.1:5000/process", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ text: textToSend }),
            });

            // *** ADD THIS CHECK ***
            // Check if the response status is OK (e.g., 200)
            if (!response.ok) {
                // Log the server error to the console for debugging
                console.error("Server error:", response.status, response.statusText);
                return null; // Return null to signal an error
            }

            const data = await response.json();
            
            // Also check if the 'processed' key exists
            if (data && data.processed) {
                 return data.processed;
            } else {
                console.error("Invalid response from server:", data);
                return null; // Return null if data is not in the expected format
            }

        } catch (error) {
            // This catches network failures or if response.json() fails
            console.error("Fetch error:", error);
            return null; // Return null to signal an error
        }
    }
});
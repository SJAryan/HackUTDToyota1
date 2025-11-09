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

        const aiResponseText = await sendToPython(query);

        var newModels = [];
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
        const response = await fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: textToSend }),
        });

        const data = await response.json();
        return data.processed;
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const submitBtn = document.getElementById('submitBtn');
    const outputBox = document.getElementById('outputBox');

    submitBtn.addEventListener('click', handleSubmit);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    });

    // FIX 1: Make handleSubmit async
    async function handleSubmit() {
        const query = userInput.value.trim();
        if (!query) return;

        // Clear the input
        userInput.value = '';

        // Add user query to output box
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.textContent = query;
        outputBox.appendChild(userMessage);

        // FIX 2: Await the response and pass the 'query' string
        const aiResponseText = await sendToPython(query);
        
        // FIX 3: Add the AI response to the output box
        const aiMessage = document.createElement('div');
        aiMessage.classList.add('message', 'ai-message');
        aiMessage.textContent = aiResponseText;
        outputBox.appendChild(aiMessage);
    }

    async function sendToPython(textToSend) {
        // FIX 4: Remove the hardcoded text
        // textToSend = "hello from javascript"; 

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
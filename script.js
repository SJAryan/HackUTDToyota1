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

    function handleSubmit() {
        const query = userInput.value.trim();
        if (!query) return;

        // Clear the input
        userInput.value = '';

        // Add user query to output box
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.textContent = query;
        outputBox.appendChild(userMessage);

        // Simulate AI response (this should be replaced with actual API call)
        setTimeout(() => {
            const aiMessage = document.createElement('div');
            aiMessage.classList.add('message', 'ai-message');
            aiMessage.textContent = `I'm processing your query about: ${query}`;
            outputBox.appendChild(aiMessage);
            outputBox.scrollTop = outputBox.scrollHeight;
        }, 500);
    }
});
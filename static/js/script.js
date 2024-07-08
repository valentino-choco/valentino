// alert('Hello')
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const suggestionsContainer = document.getElementById('suggestions');

    let messageHistory = [];
    let currentIndex = -1;
    let firstMessageSent = false;

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const userMessage = userInput.value.trim();
        if (userMessage !== '') {
            addMessage('user', userMessage);
            messageHistory.push(userMessage);
            currentIndex = messageHistory.length; // Reset index
            userInput.value = '';
            sendMessageToChatbot(userMessage);
        }
    });

    userInput.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowUp') {
            if (currentIndex > 0) {
                currentIndex--;
                userInput.value = messageHistory[currentIndex];
            }
            event.preventDefault();
        } else if (event.key === 'ArrowDown') {
            if (currentIndex < messageHistory.length - 1) {
                currentIndex++;
                userInput.value = messageHistory[currentIndex];
            } else {
                currentIndex = messageHistory.length;
                userInput.value = '';
            }
            event.preventDefault();
        }
    });

    function addMessage(sender, message) {
        if (!firstMessageSent && sender === 'user') {
            firstMessageSent = true;
            suggestionsContainer.style.display = 'none';
        }

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        if (sender === 'user') {
            messageDiv.classList.add('user-message');
        }
        messageDiv.textContent = message;
        chatContainer.appendChild(messageDiv);
        if (sender === 'bot' && message.toLowerCase().includes('gateau basque')) {
            // Create image element for gateau basque
            const imageContainer = document.createElement('div');
            imageContainer.classList.add('image-container');

            const img = document.createElement('img');
            img.src = './static/gateau_basque_ex.jpg'; // Replace with actual image path
            img.alt = 'Gateau Basque';

            imageContainer.appendChild(img);
            messageDiv.appendChild(imageContainer);
        }

        // Scroll to the bottom of the chat container
        scrollChatToBottom();
    }

    function sendMessageToChatbot(message) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('bot', data.response);
        });
    }

    function scrollChatToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to use suggestion
    window.useSuggestion = function(suggestion) {
        userInput.value = suggestion;
        chatForm.dispatchEvent(new Event('submit'));
    }

    // Function to toggle the chatbot visibility
    window.toggleChatbot = function() {
        const chatbotContainer = document.getElementById('chatbot-container');
        chatbotContainer.style.display = chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '' ? 'flex' : 'none';
    }
});





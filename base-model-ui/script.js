class ChatBot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.apiUrl = 'http://localhost:8000/ask';
        this.testUrl = 'http://localhost:8000/';
        this.init();
    }

    async testConnection() {
        const urls = [
            'http://localhost:8000/',
            'http://127.0.0.1:8000/',
            'http://0.0.0.0:8000/'
        ];
        
        for (const url of urls) {
            try {
                console.log('Testing connection to:', url);
                const response = await fetch(url);
                console.log('Connection test status:', response.status);
                if (response.ok) {
                    const data = await response.json();
                    console.log('Connection test response:', data);
                    // Update the API URL to use the working one
                    this.apiUrl = url + 'ask';
                    console.log('Updated API URL to:', this.apiUrl);
                    return true;
                }
            } catch (error) {
                console.error(`Connection test failed for ${url}:`, error);
                continue;
            }
        }
        return false;
    }

    init() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });

        // Focus input on load
        this.messageInput.focus();
        
        // Test connection on startup
        this.testConnection().then(isConnected => {
            if (!isConnected) {
                this.addMessage('⚠️ Cannot connect to backend server. Please make sure the API is running on http://localhost:8000', 'bot');
            } else {
                console.log('Backend connection successful');
            }
        });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input and reset height
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // Disable send button and show typing indicator
        this.setSendButtonState(false);
        this.showTypingIndicator();

        try {
            console.log('Sending request to:', this.apiUrl);
            console.log('Request body:', JSON.stringify({ question: message }));
            
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message })
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Response data:', data);
            const botResponse = data.answer || 'Sorry, I could not process your request.';
            
            // Add bot response to chat
            this.addMessage(botResponse, 'bot');
        } catch (error) {
            console.error('Error:', error);
            let errorMessage = 'Sorry, I encountered an error. Please try again.';
            
            if (error.message.includes('Failed to fetch')) {
                errorMessage = 'Cannot connect to the server. Please make sure the backend is running on http://localhost:8000';
            } else if (error.message.includes('CORS')) {
                errorMessage = 'CORS error. Please check server configuration.';
            } else {
                errorMessage = `Error: ${error.message}`;
            }
            
            this.addMessage(errorMessage, 'bot');
        } finally {
            // Hide typing indicator and enable send button
            this.hideTypingIndicator();
            this.setSendButtonState(true);
            this.messageInput.focus();
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.textContent = text;
        messageContent.appendChild(messageText);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
        
        // Add animation
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            messageDiv.style.transform = 'translateY(20px)';
            messageDiv.style.transition = 'all 0.3s ease';
            
            setTimeout(() => {
                messageDiv.style.opacity = '1';
                messageDiv.style.transform = 'translateY(0)';
            }, 50);
        }, 0);
    }

    showTypingIndicator() {
        this.typingIndicator.classList.add('active');
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.classList.remove('active');
    }

    setSendButtonState(enabled) {
        this.sendButton.disabled = !enabled;
        if (enabled) {
            this.sendButton.style.opacity = '1';
        } else {
            this.sendButton.style.opacity = '0.6';
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

// Handle connection errors gracefully
window.addEventListener('online', () => {
    console.log('Connection restored');
});

window.addEventListener('offline', () => {
    console.log('Connection lost');
    alert('You appear to be offline. Please check your internet connection.');
});

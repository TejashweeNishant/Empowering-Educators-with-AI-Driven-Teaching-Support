document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-message');
    const startCoachingBtn = document.getElementById('startCoooking');
    const resourcesGrid = document.getElementById('resources-grid');

    // Scroll to chat section when Start Coaching is clicked
    if (startCoachingBtn) {
        startCoachingBtn.addEventListener('click', () => {
            document.getElementById('chat').scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Handle sending message when Send button is clicked
    sendButton.addEventListener('click', sendMessage);

    // Handle sending message when Enter key is pressed
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && userInput.value.trim() !== '') {
            sendMessage();
        }
    });

    // Function to send a message
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        // Add user message to chat
        addMessage(message, 'user');
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Send message to backend and get response
            const response = await fetch('https://empowering-educators-with-ai-driven-9h0h.onrender.com/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add AI response to chat
            addMessage(data.insight, 'ai');
            
            // Display resources
            if (data.recommendations && data.recommendations.length > 0) {
                displayResources(data.recommendations);
                
                // Scroll to resources section
                setTimeout(() => {
                    document.getElementById('resources').scrollIntoView({ behavior: 'smooth' });
                }, 500);
            }
            
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again later.', 'ai');
        }
    }

    // Function to add a message to the chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.innerHTML = `<p>${text}</p>`;
        
        // Add message to chat
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom of chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Function to display resources
    function displayResources(resources) {
        // Clear previous resources
        resourcesGrid.innerHTML = '';
        
        // Add each resource as a card
        resources.forEach(resource => {
            const resourceCard = document.createElement('div');
            resourceCard.className = 'resource-card';
            
            const typeClass = resource.type.toLowerCase().includes('workshop') ? 'workshop' : 
                             resource.type.toLowerCase().includes('tool') ? 'tool' : 'strategy';
            
            resourceCard.innerHTML = `
                <div class="resource-content">
                    <span class="resource-type ${typeClass}">${resource.type}</span>
                    <h3>${resource.title}</h3>
                    <p>${resource.description || 'Learn more about this resource and how it can enhance your teaching.'}</p>
                    <a href="${resource.link}" target="_blank" class="resource-link">
                        Learn More
                        <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            `;
            
            resourcesGrid.appendChild(resourceCard);
        });
    }

    // Sample resources (fallback in case API is not available)
    const sampleResources = [
        {
            title: "Workshop: Digital Pedagogy for Modern Classrooms",
            type: "Workshop",
            description: "Learn how to effectively integrate technology into your teaching practice.",
            link: "#"
        },
        {
            title: "Tool: Nearpod",
            type: "EdTech Tool",
            description: "Interactive lessons, videos, and activities to engage students in any setting.",
            link: "https://nearpod.com"
        },
        {
            title: "Strategy: Think-Pair-Share",
            type: "Teaching Strategy",
            description: "A collaborative learning strategy to encourage student participation.",
            link: "#"
        }
    ];

    // Display sample resources on page load
    displayResources(sampleResources);
});

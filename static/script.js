const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

input.focus();

input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {

    const message = input.value.trim();

    if (!message) {
        return;
    }

    // Add user message
    chatBox.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    // Typing indicator
    const typingId = "typing-indicator";

    chatBox.innerHTML += `
        <div class="bot-message" id="${typingId}">
            Nova is typing...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Remove typing indicator
        document.getElementById(typingId)?.remove();

        // Add bot response
        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.response}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        document.getElementById(typingId)?.remove();

        chatBox.innerHTML += `
            <div class="bot-message">
                Sorry, something went wrong. Please try again.
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

        console.error(error);
    }
}

function quickMessage(message) {

    document.getElementById("message-input").value = message;

    sendMessage();
}
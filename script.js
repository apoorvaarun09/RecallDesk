
const customerInput = document.getElementById("customerId");
const messageInput = document.getElementById("messageInput");
const chatMessages = document.getElementById("chatMessages");
const memoryStatus = document.getElementById("memoryStatus");
const sendButton = document.getElementById("sendButton");
const statusElement = document.getElementById("status");

function addMessage(message, sender) {
    const messageElement = document.createElement("div");

    messageElement.classList.add("message", sender);
    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {

    const customerId = customerInput.value.trim();
    const message = messageInput.value.trim();

    if (!customerId) {
        alert("Please enter a Customer ID.");
        return;
    }

    if (!message) {
        alert("Please enter your message.");
        return;
    }

    addMessage(message, "user");

    messageInput.value = "";
    sendButton.disabled = true;

    statusElement.textContent = "Thinking...";
    memoryStatus.textContent =
        "Searching previous customer memories...";

    try {

        const response = await fetch("/api/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                customer_id: customerId,
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok || data.status !== "success") {
            throw new Error(
                data.message || "Unable to process your message."
            );
        }

        addMessage(data.reply, "assistant");
        
// Display memories retrieved from Hindsight
const memoryList = document.getElementById("memoryList");

memoryList.innerHTML = "";

if (data.memories && data.memories.length > 0) {

    data.memories.forEach((memory, index) => {

        const memoryItem = document.createElement("div");

        memoryItem.classList.add("memory-item");

        const memoryTitle = document.createElement("strong");
        memoryTitle.textContent = `Memory ${index + 1}`;

        const memoryText = document.createElement("p");
        memoryText.textContent = memory;

        memoryItem.appendChild(memoryTitle);
        memoryItem.appendChild(memoryText);

        memoryList.appendChild(memoryItem);

    });

} else {

    memoryList.innerHTML =
        '<p class="empty-memory">No previous memories found.</p>';

}


        if (data.memory_used) {
            memoryStatus.textContent =
                "Previous customer memories were retrieved and used.";
        } else {
            memoryStatus.textContent =
                "No previous memories found. New interaction saved.";
        }

        statusElement.textContent = "Online";

    } catch (error) {

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "assistant"
        );

        memoryStatus.textContent = error.message;
        statusElement.textContent = "Error";

        console.error("Chat error:", error);

    } finally {

        sendButton.disabled = false;
        messageInput.focus();

    }
}

// Send message when Enter is pressed
messageInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});

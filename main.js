const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    userInput.value = "";

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

        if (data.reply) {

            addMessage(data.reply, "bot");

        } else {

            addMessage(data.error || "Something went wrong.", "bot");

        }

    } catch (error) {

        addMessage("Server connection failed.", "bot");

    }
}

function addMessage(text, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");
    messageDiv.classList.add(sender);

    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}

userInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});

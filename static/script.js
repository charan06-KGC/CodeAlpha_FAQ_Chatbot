const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");


// ==========================================
// ADD MESSAGE
// ==========================================

function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    if (sender === "user") {
        messageDiv.classList.add("user-message");
    } else {
        messageDiv.classList.add("bot-message");
    }


    const wrapper = document.createElement("div");

    const content = document.createElement("div");

    content.classList.add("message-content");

    content.textContent = message;


    const time = document.createElement("div");

    time.classList.add("message-time");

    const now = new Date();

    time.textContent = now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });


    wrapper.appendChild(content);
    wrapper.appendChild(time);

    messageDiv.appendChild(wrapper);

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// ==========================================
// TYPING ANIMATION
// ==========================================

function showTyping() {

    const typingDiv = document.createElement("div");

    typingDiv.classList.add(
        "message",
        "bot-message"
    );

    typingDiv.id = "typing";


    typingDiv.innerHTML = `
        <div class="message-content">

            <div class="typing">
                <span></span>
                <span></span>
                <span></span>
            </div>

        </div>
    `;


    chatBox.appendChild(typingDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// ==========================================
// REMOVE TYPING
// ==========================================

function removeTyping() {

    const typing =
        document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


// ==========================================
// SEND MESSAGE
// ==========================================

async function sendMessage() {

    const question = input.value.trim();

    if (!question) {
        return;
    }


    const welcome =
        document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    sendButton.disabled = true;


    addMessage(
        question,
        "user"
    );


    input.value = "";


    showTyping();


    try {

        const response = await fetch(
            "/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data = await response.json();


        setTimeout(() => {

            removeTyping();

            addMessage(
                data.answer,
                "bot"
            );

            sendButton.disabled = false;

            input.focus();

        }, 500);


    } catch (error) {

        removeTyping();

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

        sendButton.disabled = false;
    }
}


// ==========================================
// QUICK SUGGESTION
// ==========================================

function askSuggestion(question) {

    input.value = question;

    sendMessage();
}


// ==========================================
// EXAMPLE QUESTION
// ==========================================

function askExample(question) {

    closeExamples();

    input.value = question;

    sendMessage();
}


// ==========================================
// CLEAR CHAT
// ==========================================

function clearChat() {

    chatBox.innerHTML = `

        <div class="welcome">

            <div class="welcome-avatar">
                🤖
            </div>

            <h2>How can I help you?</h2>

            <p>
                Ask me anything about orders, payments,
                delivery, returns or your account.
            </p>

            <div class="suggestions">

                <button
                    onclick="askSuggestion('How can I reset my password?')">
                    Reset my password
                </button>

                <button
                    onclick="askSuggestion('How can I track my order?')">
                    Track my order
                </button>

                <button
                    onclick="askSuggestion('How long does delivery take?')">
                    Delivery time
                </button>

                <button
                    onclick="askSuggestion('How can I return a product?')">
                    Return a product
                </button>

            </div>

        </div>
    `;

    input.focus();
}


// ==========================================
// OPEN EXAMPLES
// ==========================================

function showExamples() {

    const modal =
        document.getElementById("examples-modal");

    if (!modal) {
        console.error("Examples modal not found.");
        return;
    }

    modal.classList.add("show");
}


// ==========================================
// CLOSE EXAMPLES
// ==========================================

function closeExamples() {

    const modal =
        document.getElementById("examples-modal");

    if (!modal) {
        return;
    }

    modal.classList.remove("show");
}


// ==========================================
// CLOSE WITH ESCAPE KEY
// ==========================================

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Escape") {
            closeExamples();
        }

    }
);


// ==========================================
// CLOSE WHEN CLICKING OUTSIDE MODAL
// ==========================================

document.addEventListener(
    "click",
    function(event) {

        const modal =
            document.getElementById("examples-modal");

        if (
            modal &&
            event.target === modal
        ) {
            closeExamples();
        }

    }
);


// ==========================================
// ENTER KEY
// ==========================================

input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }

    }
);
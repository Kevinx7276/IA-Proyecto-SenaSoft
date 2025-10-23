const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function appendMessage(role, text, delay = 0) {
  const msg = document.createElement("div");
  msg.classList.add("message", role);
  msg.style.opacity = "0";
  msg.textContent = text;
  chatBox.appendChild(msg);

  setTimeout(() => {
    msg.style.transition = "opacity 0.3s ease-in";
    msg.style.opacity = "1";
    chatBox.scrollTop = chatBox.scrollHeight;
  }, delay);
}

function showTyping() {
  const typing = document.createElement("div");
  typing.classList.add("message", "bot");
  typing.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
  return typing;
}

function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage("user", text);
  userInput.value = "";

  const typingBubble = showTyping();

  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  })
    .then((res) => res.json())
    .then((data) => {
      typingBubble.remove();
      const reply = data.reply.trim() || "(sin respuesta)";
      appendMessage("bot", reply);
    })
    .catch(() => {
      typingBubble.remove();
      appendMessage("bot", "(Error al conectar con el servidor)");
    });
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

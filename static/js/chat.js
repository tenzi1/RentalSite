console.log('inside of chat js')


chatSocket = new WebSocket(
    "ws://"
    + document.location.host
    + "/ws/chat/"
)

chatSocket.onopen = function (e) {
    console.log("Chat Socket successfully connected.")
}

chatSocket.onclose = function (e) {
    console.log("Chat socket closed unexpectedly.")
}

chatSocket.onmessage = async function (e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const senderId = data.senderId;
    alertMessage()
    sender_data = await getUserDetail(senderId);
    renderChatContainer(senderId, sender_data);
    renderReceivedMessage(message, senderId)
    renderSender(message, senderId, sender_data)
}

// for buffering chat user info
let chatUsers = {}

// function to get user detail and buffer it.
async function getUserDetail(user_id) {
    if (user_id in chatUsers) {
        return chatUsers[user_id];
    } else {
        user_detail = await fetchUserDetail(user_id);
        chatUsers[user_id] = user_detail;
        return user_detail
    }
}

// function to fetch user detail.
async function fetchUserDetail(user_id) {
    return fetch(`/api/v1/chat_user/${user_id}`, {
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data) {
                console.log('No data received');
                return {};
            }
            return data;
        })
        .catch(error => {
            console.error("Error fetching chat user detail: ", error);
            return {};
        });
}

function alertMessage() {
    badge = document.querySelector('.message-container .badge')
    badge.classList.remove('visually-hidden')
}


function renderSender(message, senderId, userDetails) {


    chatItem = document.getElementById(`chat-${senderId}`)
    if (!chatItem) {

        img = document.createElement('img')
        img.src = userDetails.profile_img

        p1 = document.createElement('p')
        p1.classList.add('chat-name')
        p1.textContent = userDetails.username

        p2 = document.createElement('p')
        p2.classList.add('chat-message')
        p2.id = `p_${senderId}`;
        p2.textContent = message.slice(0, 15) + '...';

        div = document.createElement('div')
        div.classList.add('chat-item')
        div.id = `chat-${senderId}`
        div.setAttribute("data-user-id", senderId);

        div.appendChild(img)
        div.appendChild(p1)
        div.appendChild(p2)

        div2 = document.querySelector('.chat-list')
        div2.appendChild(div)

    } else {
        p2 = document.getElementById(`p_${senderId}`)
        p2.textContent = message.slice(0, 15) + '...';


    }

    document.querySelectorAll('.chat-item').forEach(
        function (chat) {
            chat.addEventListener('click', async function (e) {
                const user_id = chat.getAttribute('data-user-id');
                mainContainer = document.getElementById(`main-chat-${user_id}`)
                mainContainer.classList.remove('visually-hidden')

                chatContainer = document.getElementById(`chat-content-${user_id}`)

                let currentPage = 1;
                let allChatsFetched = false;

                try {
                    // Function to fetch chats with error handling
                    const fetchAndRenderChats = async () => {

                        if (chatContainer.hasChildNodes()) {
                            return;
                        } else {
                            console.log("The container does not have any child elements.");
                            const chats = await fetchChats(user_id, currentPage);
                            if (!chats) {
                                console.log('No chats found for page:', currentPage);
                                allChatsFetched = true;
                                return;
                            }
                            renderChats(chats);

                            // Previous scroll position to detect scroll direction
                            let prevScrollTop = chatContainer.scrollTop;

                            // Scroll event listener to fetch older messages
                            chatContainer.addEventListener('scroll', async () => {
                                if (!allChatsFetched && chatContainer.scrollTop === 0 && chatContainer.scrollTop < prevScrollTop) {
                                    currentPage++;
                                    try {
                                        const olderChats = await fetchChats(user_id, currentPage);
                                        if (!olderChats || olderChats.length === 0) {
                                            allChatsFetched = true;
                                            return;
                                        }
                                        renderChats(olderChats, true);
                                    } catch (error) {
                                        console.error('Error fetching older chats:', error);
                                    }
                                }
                                // Update previous scroll position
                                prevScrollTop = chatContainer.scrollTop;
                            });
                        }
                    };

                    // Initial fetch and render
                    await fetchAndRenderChats();

                } catch (error) {
                    console.error('Error while fetching initial chats:', error);
                }


            })
        }
    )

}

function renderChats(chats, prepend = false) {
    chats.reverse().forEach((chat) => {
        if (chat.sent) {
            renderSentMessage(chat.message, chat.user_id, prepend);
        } else {
            renderReceivedMessage(chat.message, chat.user_id, prepend);
        }
    });
}


// function to send message on websocket
async function sendChat(message, receiverId) {
    if (message != '' && receiverId) {
        const payload = {
            'message': message,
            'receiverId': receiverId
        };
        chatSocket.send(JSON.stringify(payload));
        renderSentMessage(message, receiverId)
        receiver_data = await getUserDetail(receiverId)
        renderSender(message, receiverId, receiver_data)
    }
}



// creates Layout for rendering chat message.
function renderChatContainer(chatId, chatDetail) {
    mainContainer = document.getElementById(`main-chat-${chatId}`)

    if (!mainContainer) {
        mainContainer = document.createElement('div')
        mainContainer.classList.add('chat-container')
        mainContainer.id = `main-chat-${chatId}`
        mainContainer.setAttribute('chat_id', chatId);

        // chat header
        profileImg = document.createElement('img');
        profileImg.classList.add('profile-pic');
        profileImg.src = chatDetail.profile_img;

        profileName = document.createElement('span');
        profileName.classList.add('name');
        profileName.textContent = chatDetail.username;

        closeIcon = document.createElement('i');
        closeIcon.classList.add('fa', 'fa-times', 'close-icon');
        closeIcon.id = `close-chat-${chatId}`;

        divHeader = document.createElement('div');
        divHeader.classList.add('header-info');

        divHeader.appendChild(profileName);
        divHeader.appendChild(closeIcon);

        divChatHeader = document.createElement('div');
        divChatHeader.classList.add('chat-header');
        divChatHeader.appendChild(profileImg);
        divChatHeader.appendChild(divHeader);

        // chat content --
        divChatContent = document.createElement('div');
        divChatContent.classList.add('chat-content');
        divChatContent.id = `chat-content-${chatId}`;

        // chat input
        input = document.createElement('input');
        input.id = `input-${chatId}`;
        input.type = 'text';
        input.placeholder = 'Aa';

        btn = document.createElement('button');
        btn.classList.add('send-btn');
        btn.id = `send-btn-${chatId}`
        btn.textContent = 'Send';

        divChatInput = document.createElement('div');
        divChatInput.classList.add('chat-input');

        divChatInput.appendChild(input);
        divChatInput.appendChild(btn);

        mainContainer.appendChild(divChatHeader);
        mainContainer.appendChild(divChatContent);
        mainContainer.appendChild(divChatInput);

        mainContainer.classList.add('visually-hidden')

        document.querySelector('.message-container').appendChild(mainContainer)

    }
    // initially hide the layout message
    mainContainer.classList.add('visually-hidden')

    sendbtn = document.getElementById(`send-btn-${chatId}`)
    sendbtn.addEventListener('click', function (e) {
        textInput = document.getElementById(`input-${chatId}`);
        message = textInput.value;
        receiverId = chatId;
        sendChat(message, receiverId);
        textInput.value = "";
    })

    closeIcon = document.getElementById(`close-chat-${chatId}`)
    closeIcon.onclick = function (e) {
        document.getElementById(`main-chat-${chatId}`).classList.add('visually-hidden')
    }
}


// function to render sent messages.
function renderSentMessage(message, receiverId, prepend = false) {
    divChatContent = document.getElementById(`chat-content-${receiverId}`);

    p = document.createElement('p');
    p.textContent = message;

    divMessage = document.createElement('div');
    divMessage.classList.add('message-content');

    divMessage.appendChild(p);

    divMessageContainer = document.createElement('div');
    divMessageContainer.classList.add('message', 'left');
    divMessageContainer.appendChild(divMessage);

    if (prepend) {
        divChatContent.insertBefore(divMessageContainer, divChatContent.firstChild);
    } else {
        divChatContent.appendChild(divMessageContainer);
    }

}

// function to render received messages.
function renderReceivedMessage(message, senderId, prepend = false) {
    divChatContent = document.getElementById(`chat-content-${senderId}`);

    p = document.createElement('p');
    p.textContent = message

    divMessage = document.createElement('div');
    divMessage.classList.add('message-content');

    divMessage.appendChild(p);

    divMessageContainer = document.createElement('div');
    divMessageContainer.classList.add('message', 'right');
    divMessageContainer.appendChild(divMessage);

    if (prepend) {
        divChatContent.insertBefore(divMessageContainer, divChatContent.firstChild);
    } else {
        divChatContent.appendChild(divMessageContainer);
    }

}

// Function to fetch chats
function fetchChats(user_id, page = 1) {
    return fetch(`/api/v1/chats/?user_id=${user_id}&page=${page}`, {
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.json())
        .then(data => {
            if (!data) {
                console.log("No data received");
                return [];
            }
            return data.results;
        })
        .catch(error => {
            console.error("Error fetching chats:", error);
            return [];
        })
}

function fetchLatestChats() {
    return fetch("/api/v1/latest_chats/", {
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.json())
        .then(data => {
            if (!data) {
                console.log("No data received");
                return [];
            }
            return data.results;
        })
        .catch(error => {
            console.error("Error fetching chats:", error);
            return [];
        })
}


document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.start-chat').forEach(
        function (btn) {
            btn.addEventListener('click', function (e) {

                const user_id = btn.getAttribute("data-user-id");

                if (user_id in chatUsers) {
                    user_data = chatUsers[user_id];
                    renderChatContainer(user_id, user_data);
                    document.getElementById(`main-chat-${user_id}`).classList.remove('visually-hidden');

                    document.querySelectorAll('.chat-container').forEach(container => {
                        if (container.id != `main-chat-${user_id}`) {
                            container.classList.add('visually-hidden')
                        }
                    })


                } else {
                    fetchUserDetail(user_id).then(user_data => {
                        chatUsers[user_id] = user_data;
                        renderChatContainer(user_id, user_data);
                        document.getElementById(`main-chat-${user_id}`).classList.remove('visually-hidden');

                    })
                }
            })
        }
    );

    // Chat 
    document.querySelector('.message-icon').onclick = function (e) {
        const messageContainer = document.querySelector('.messages-popup');
        messageContainer.classList.toggle('visually-hidden');  // Toggle visibility

        // Fetch and render chats if the container is not hidden
        if (!messageContainer.classList.contains('visually-hidden')) {
            fetchLatestChats()
                .then(chats => {
                    if (chats.length == 0) {
                        document.querySelector('.no-chat').classList.remove('visually-hidden')

                    } else {
                        document.querySelector('.no-chat').classList.add('visually-hidden')
                    }

                    chats.forEach(async function (chat) {
                        user_data = await getUserDetail(chat.user_id);
                        renderChatContainer(chat.user_id, user_data)
                        renderSender(chat.message, chat.user_id, user_data);
                    });
                })
                .catch(error => {
                    console.error('Error fetching chats:', error);
                });
        }
    };

});



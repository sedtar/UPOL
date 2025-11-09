import { useEffect, useState, useRef } from "react";

import { io } from "socket.io-client";
const socket = io("http://localhost:5000");


const Chat = ({ Logout, username }) => {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([
        { sender: "System", text: "Welcome to the chat!" },
    ]);
    const [selectedUser, setSelectedUser] = useState("Chat");
    const [contacts, setContacts] = useState([]); // an array of usernames that we have stored in React state.
    const [searchTerm, setSearchTerm] = useState("");
    const socketRef = useRef();

    // Initialize socket once
    useEffect(() => {
        socketRef.current = io("http://localhost:5000");
        socketRef.current.emit("join", username);

        // Receive messages
        socketRef.current.on("receiveMessage", (data) => {
            setMessages((prev) => [...prev, { sender: data.sender, text: data.text }]);
        });

        return () => {
            socketRef.current.disconnect();
        };
    }, [username]);



    useEffect(() => { // useEffect is spacial React hook, which says "do something, when the component loads or when username is changed"

        const fetchUsers = async () => { //this function communicated with server
            try {
                const res = await fetch(`http://localhost:5000/users?username=${username}`); //send the http request and wait
                const data = await res.json(); // need to convert it to a normal JavaScript object
                if (data.success) { //checks if the users were successfully retrieved from the server
                    const userList = data.users.map(u => u.username); // The .map() function goes through the entire array and extracts only the name from each object.
                    setContacts(userList);// saves the new contact field to React state,
                }
            } catch (err) {
                console.error("Failed to fetch users:", err);
            }
        };
        fetchUsers();
    }, [username])

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const res = await fetch(`http://localhost:5000/users?username=${username}&search=${searchTerm}`);
                const data = await res.json();
                if (data.success) {
                    const userList = [...data.users.map(u => u.username)];
                    setContacts(userList);
                }
            } catch (err) {
                console.error("Failed to fetch users:", err);
            }
        };
        fetchUsers();
    }, [username, searchTerm]);


    //load messages when clicking on a user
    useEffect(() => {
        const fetchMessages = async () => {
            if (selectedUser === "Chat") return; // don't choose the default room

            try {
                const res = await fetch(
                    `http://localhost:5000/messages?user1=${username}&user2=${selectedUser}`
                );
                const data = await res.json();

                if (data.success) {
                    setMessages(data.messages.map(m => ({
                        sender: m.sender,
                        text: m.message
                    })));
                }
            } catch (err) {
                console.error("Failed to fetch messages:", err);
            }
        };

        fetchMessages();
    }, [selectedUser, username]); // it starts every time you click on another user¨



    const handleSend = async (e) => {
        e.preventDefault();
        if (!message.trim() || selectedUser === "Chat") return; // checks if the message is empty or contains only spaces, if yes, returns

        const newMsg = { sender: username, receiver: selectedUser, text: message }; // new object of message

        setMessages([...messages, newMsg]); //(...messages)unpacks old messages (copy of existing field), //newMsg -- adds to end a new message
        setMessage(""); // The input field is cleared — the user can now type more text

        /**await fetch("http://localhost:5000/messages", { // here the message is being sent to the server
             method: "POST",
             headers: { "Content-Type": "application/json" },
             body: JSON.stringify(newMsg), //converts our newMsg object into a JSON string so that the server can process it.
         });**/

        socket.emit("sendMessage", newMsg); // sends a message via WebSocket
    };

    //filteredContacts will be a new array containing only users whose name contains the search text, regardless of case.
    const filteredContacts = contacts.filter((user) => //
        user.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="container">
            <div className="card card--main">
                {/* Levý panel se seznamem kontaktů */}
                <aside className="sidebar">
                    <h3>Chats</h3>
                    <input
                        className="card--main__search"
                        type="text"
                        placeholder="Search..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}

                    />
                    <ul>
                        {filteredContacts.map((user) => (
                            <li
                                key={user}
                                className={selectedUser === user ? "active" : ""}// loop through each array item and return a new array of JSX elements.
                                onClick={() => setSelectedUser(user)}
                            >
                                {user}
                            </li>
                        ))}
                    </ul>
                    <button className="logout" onClick={Logout}>
                        Logout
                    </button>
                </aside>

                {/* Hlavní okno chatu */}
                <main className="chat">
                    <div className="chat-header">
                        <h2>{selectedUser}</h2>
                    </div>

                    <div className="chat-messages">
                        {messages.map((msg, i) => (
                            <div
                                key={i}
                                className={`message ${msg.sender === username ? "sent" : "received"
                                    }`}
                            >
                                <strong>{msg.sender}:</strong> {msg.text}
                            </div>
                        ))}
                    </div>

                    <form className="chat-input" onSubmit={handleSend}>
                        <input
                            type="text"
                            placeholder="Type your message..."
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        />
                        <button type="submit">Send</button>
                    </form>
                </main>
                <aside className="user-panel">
                    <h3>User info</h3>
                    <p><strong>Logged in as:</strong></p>
                    <p className="username">{username}</p>
                    <button className="logout" onClick={Logout}>Logout</button>

                </aside>
            </div>
        </div >
    );
};

export default Chat;

const onlineUsers = {}; // { username: socket.id }

const setupSocket = (io, pool) => {
    io.on("connection", (socket) => {
        console.log("User connected:", socket.id);

        socket.on("join", (username) => {
            socket.username = username;
            onlineUsers[username] = socket.id;
            console.log(`${username} joined chat`);
        });

        socket.on("sendMessage", async ({ sender, receiver, text }) => {
            try {
                const senderRes = await pool.query("SELECT id FROM users WHERE username = $1", [sender]);
                const receiverRes = await pool.query("SELECT id FROM users WHERE username = $1", [receiver]);
                if (!senderRes.rows[0] || !receiverRes.rows[0]) return;

                await pool.query(
                    "INSERT INTO messages (sender_id, receiver_id, message) VALUES ($1, $2, $3)",
                    [senderRes.rows[0].id, receiverRes.rows[0].id, text]
                );

                if (onlineUsers[receiver]) io.to(onlineUsers[receiver]).emit("receiveMessage", { sender, text });
                socket.emit("receiveMessage", { sender, text });
            } catch (err) {
                console.error("Error sending message:", err);
            }
        });

        socket.on("disconnect", () => {
            console.log("User disconnected:", socket.username);
            delete onlineUsers[socket.username];
        });
    });
};

module.exports = setupSocket;
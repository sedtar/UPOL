const express = require("express");
const cors = require("cors");
const http = require("http");
const { Server } = require("socket.io");
const pool = require("./db");

const authRoutes = require("./routes/auth");
const usersRoutes = require("./routes/users");
const messagesRoutes = require("./routes/messages");
const setupSocket = require("./sockets");
const initDb = require("./initDb");

const app = express();
const server = http.createServer(app);

const io = new Server(server, {
    cors: { origin: "http://localhost:5173", methods: ["GET", "POST"] },
});

app.use(cors());
app.use(express.json());

// Routes
app.use("/", authRoutes);
app.use("/users", usersRoutes);
app.use("/messages", messagesRoutes);

// Socket.IO
setupSocket(io, pool);

initDb();

// Start server
const PORT = 5000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));

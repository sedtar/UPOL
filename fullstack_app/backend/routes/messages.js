const express = require("express");
const router = express.Router();
const pool = require("../db");

// Get messages between two users
router.get("/", async (req, res) => {
    const { user1, user2 } = req.query;
    try {
        const user1Res = await pool.query("SELECT id FROM users WHERE username = $1", [user1]);
        const user2Res = await pool.query("SELECT id FROM users WHERE username = $1", [user2]);
        if (!user1Res.rows[0] || !user2Res.rows[0]) return res.status(400).json({ success: false, message: "User not found" });

        const user1Id = user1Res.rows[0].id;
        const user2Id = user2Res.rows[0].id;

        const result = await pool.query(
            `SELECT m.id, u.username AS sender, m.message, m.created_at
       FROM messages m
       JOIN users u ON m.sender_id = u.id
       WHERE (m.sender_id = $1 AND m.receiver_id = $2)
          OR (m.sender_id = $2 AND m.receiver_id = $1)
       ORDER BY m.created_at ASC`,
            [user1Id, user2Id]
        );

        res.json({ success: true, messages: result.rows });
    } catch (err) {
        console.error("Error loading messages:", err);
        res.status(500).json({ success: false, message: "Database error" });
    }
});

// Send message (optional if using socket.io)
router.post("/", async (req, res) => {
    const { sender, receiver, text } = req.body;
    try {
        const senderRes = await pool.query("SELECT id FROM users WHERE username = $1", [sender]);
        const receiverRes = await pool.query("SELECT id FROM users WHERE username = $1", [receiver]);
        if (!senderRes.rows[0] || !receiverRes.rows[0]) return res.status(400).json({ success: false, message: "Sender or receiver not found" });

        await pool.query(
            "INSERT INTO messages (sender_id, receiver_id, message) VALUES ($1, $2, $3)",
            [senderRes.rows[0].id, receiverRes.rows[0].id, text]
        );
        res.json({ success: true, message: "Message sent successfully" });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: "Database error" });
    }
});

module.exports = router;
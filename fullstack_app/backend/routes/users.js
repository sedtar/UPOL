const express = require("express");
const router = express.Router();
const pool = require("../db");

router.get("/", async (req, res) => {
    const username = req.query.username;
    const search = req.query.search || "";
    try {
        const result = await pool.query(
            "SELECT username FROM users WHERE username != $1 AND username ILIKE $2 AND is_active = true ORDER BY username ASC",
            [username, `%${search}%`]
        );
        res.json({ success: true, users: result.rows });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: "Database error" });
    }
});

module.exports = router;
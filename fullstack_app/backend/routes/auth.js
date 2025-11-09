const express = require("express");
const router = express.Router();
const bcrypt = require("bcrypt");
const pool = require("../db");

const SALT_ROUNDS = 10;

router.post("/login", async (req, res) => {
    const { username, password } = req.body;
    try {
        const result = await pool.query("SELECT * FROM users WHERE username = $1", [username]);
        if (result.rows.length === 0) return res.json({ success: false, message: "Invalid username or password." });

        const user = result.rows[0];
        const isMatch = await bcrypt.compare(password, user.password);
        if (isMatch) res.json({ success: true, message: "Login successful!" });
        else res.json({ success: false, message: "Invalid username or password" });
    } catch (err) {
        console.error(err);
        res.json({ success: false, message: "Server error" });
    }
});

router.post("/register", async (req, res) => {
    const { username, email, password } = req.body;
    try {
        const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);
        const result = await pool.query(
            `INSERT INTO users (username, email, password)
       VALUES ($1, $2, $3)
       RETURNING id, username, email`,
            [username, email, hashedPassword]
        );
        res.json({ success: true, user: result.rows[0] });
    } catch (err) {
        console.error(err);
        if (err.code === "23505") res.json({ success: false, message: "Username or email already exists" });
        else res.json({ success: false, message: "Server error" });
    }
});

module.exports = router;
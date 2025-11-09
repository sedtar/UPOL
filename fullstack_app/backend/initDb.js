const pool = require("./db");

const initDb = async () => {
    try {
        await pool.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
        is_active BOOLEAN DEFAULT true
      );

      CREATE TABLE IF NOT EXISTS chats (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        is_group BOOLEAN DEFAULT false,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
      );

      CREATE TABLE IF NOT EXISTS chat_users (
        chat_id INT REFERENCES chats(id) ON DELETE CASCADE,
        user_id INT REFERENCES users(id) ON DELETE CASCADE,
        PRIMARY KEY (chat_id, user_id)
      );

      CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        sender_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        receiver_id INT REFERENCES users(id),
        chat_id INT REFERENCES chats(id),
        message TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
      );

      CREATE INDEX IF NOT EXISTS idx_sender_receiver ON messages(sender_id, receiver_id);
      CREATE INDEX IF NOT EXISTS idx_receiver_sender ON messages(receiver_id, sender_id);
    `);

        console.log("Database tables are ready.");
    } catch (err) {
        console.error("Error creating tables:", err);
    }
};

module.exports = initDb;
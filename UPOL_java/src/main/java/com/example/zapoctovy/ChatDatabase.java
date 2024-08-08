package com.example.zapoctovy;

import java.sql.*;


public class ChatDatabase implements AutoCloseable {

    private static final String TABLE_NAME = "CHATS"; // Název tabulky pro ukládání chatů
    private final PreparedStatement getByUsersStmt; // Připravený dotaz pro získání chatu mezi dvěma uživateli
    private final PreparedStatement insertMessageStmt; // Připravený dotaz pro vložení nové zprávy do chatu

    // Konstruktor třídy ChatDatabase
    public ChatDatabase(Connection con) throws UserDBException {
        try {
            // Připojení k databázi
            // Připravený dotaz pro získání chatu mezi dvěma uživateli
            getByUsersStmt = con.prepareStatement("SELECT * FROM " + TABLE_NAME + " WHERE (user1 = ? AND user2 = ?) or (user1 = ? AND user2 = ?)");
            // Připravený dotaz pro vložení nové zprávy do chatu
            insertMessageStmt = con.prepareStatement("INSERT INTO " + TABLE_NAME + " (user1, user2, message) VALUES (?, ?, ?)");
        } catch (SQLException e) {
            throw new UserDBException("Unable to initialize prepared statements.", e);
        }
    }

    // Metoda pro získání chatových zpráv mezi dvěma uživateli
    public ResultSet getChatMessages(String user1, String user2) throws UserDBException {
        try {
            getByUsersStmt.setString(1, user1);
            getByUsersStmt.setString(2, user2);
            getByUsersStmt.setString(3, user2);
            getByUsersStmt.setString(4, user1);
            return getByUsersStmt.executeQuery(); // Vrátí výsledek dotazu
        } catch (SQLException e) {
            throw new UserDBException("Unable to fetch chat messages", e);
        }
    }

    // Metoda pro přidání nové zprávy do chatu
    public void addMessage(String user1, String user2, String message) throws UserDBException {
        try {
            insertMessageStmt.setString(1, user1);
            insertMessageStmt.setString(2, user2);
            insertMessageStmt.setString(3, message);
            insertMessageStmt.executeUpdate(); // Spustí vložení záznamu do databáze
        } catch (SQLException e) {
            throw new UserDBException("Unable to add a message to the chat", e);
        }
    }

    // Metoda pro uzavření přípravených dotazů
    @Override
    public void close() {
        try {
            getByUsersStmt.close();
            insertMessageStmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
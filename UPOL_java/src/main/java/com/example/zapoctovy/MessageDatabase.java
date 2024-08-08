package com.example.zapoctovy;

import java.sql.*;


public class MessageDatabase implements AutoCloseable {

    private static final String TABLE_NAME = "MESSAGES"; // Table name
    private PreparedStatement getByIdStmt;
    private PreparedStatement insertStmt;
    private PreparedStatement deleteByIdStmt;
    private Connection con;

    public MessageDatabase(Connection con) throws UserDBException {
        try {
            this.con = con;
            getByIdStmt = con.prepareStatement("SELECT * FROM " + TABLE_NAME + " WHERE id = ?");
            insertStmt = con.prepareStatement("INSERT INTO " + TABLE_NAME + " (content, date_created) VALUES (?, ?)");
            deleteByIdStmt = con.prepareStatement("DELETE FROM " + TABLE_NAME + " WHERE id = ?");
        } catch (SQLException e) {
            throw new UserDBException("Unable to initialize prepared statements.", e);
        }
    }

    // Metoda pro získání zprávy podle ID
    public Message getById(int id) throws UserDBException {
        Message message = null;
        try {
            getByIdStmt.setInt(1, id);
            try (ResultSet results = getByIdStmt.executeQuery()) {
                if (results.next()) {
                    message = new Message(results.getInt("id"), results.getString("content"), results.getDate("date_created"));
                }
            }
        } catch (SQLException e) {
            throw new UserDBException("Unable to find a message by ID", e);
        }
        return message;
    }

    // Metoda pro vytvoření nové zprávy
    public Message create(String content, Date date) throws UserDBException {
        try {
            insertStmt.setString(1, content);
            insertStmt.setDate(2, date);
            insertStmt.executeUpdate();

            ResultSet generatedKeys = insertStmt.getGeneratedKeys();
            int id = -1;
            if (generatedKeys.next()) {
                id = generatedKeys.getInt(1);
            }
            return new Message(id, content, date);
        } catch (SQLException e) {
            throw new UserDBException("Unable to create a new message", e);
        }
    }

    // Metoda pro odstranění zprávy podle ID
    public void removeById(int id) throws UserDBException {
        try {
            deleteByIdStmt.setInt(1, id);
            deleteByIdStmt.executeUpdate();
        } catch (SQLException e) {
            throw new UserDBException("Unable to delete a message by ID", e);
        }
    }

    @Override
    public void close() {
        try {
            getByIdStmt.close();
            insertStmt.close();
            deleteByIdStmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
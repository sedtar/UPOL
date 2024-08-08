package com.example.zapoctovy;
import javafx.application.Platform;
import javafx.collections.ObservableList;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

import java.sql.*;

/**
 * Controller class for managing the chat functionality.
 */
public class ChatController {
    private static final String TABLE_NAME = "chats"; // Table name
    private static final String DB_NAME = "demodb"; // Database name
    public Label chatLabel;
    public User friendUser;
    public TextField messageField;
    public ListView chatArea;
    String connectionURL = "jdbc:derby:" + DB_NAME + ";create=true"; // URL for database connection
    private User actualUser;

    /**
     * Initializes the chat functionality.
     */
    public void initialize() {
        updateChat();
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            initializeTable(con);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }

        Thread updateThread = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(50); //
                    Platform.runLater(this::updateChat); // Update chat from JavaFX thread
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        updateThread.setDaemon(true); // Set the thread as daemon (terminates with the main thread)
        updateThread.start();

       

    }

    /**
     * Initializes the database table if not already existing.
     *
     * @param con Connection to the database
     * @throws SQLException If an SQL error occurs
     */
    private void initializeTable(Connection con) throws SQLException {
        try (Statement stmt = con.createStatement()) {
            DatabaseMetaData metaData = con.getMetaData();
            ResultSet tables = metaData.getTables(null, null, TABLE_NAME.toUpperCase(), null); // Default schema name is "APP"
            if (tables.next()) {

                System.out.println("Table '" + TABLE_NAME + "' already exists");
            }else {
                // Create a new table with the specified columns
                String createTableQuery = "CREATE TABLE " + TABLE_NAME + " (id INT GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1), user1 VARCHAR(30), user2 VARCHAR(30), message VARCHAR(255), sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)";
                stmt.executeUpdate(createTableQuery);
                System.out.println("Table '" + TABLE_NAME + "' created successfully.");
            }


        } catch (SQLException e) {
            throw new RuntimeException("Error initializing table: " + e.getMessage(), e);
        }
    }

    /**
     * Sets the other user with whom the current user is chatting.
     *
     * @param selectedFriend The username of the selected friend
     */
    public void setOtherUser(String selectedFriend) {
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (UserDatabase users = new UserDatabase(con)) {
                friendUser = users.getByUsername(selectedFriend);
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        chatLabel.setText("Chat with " + selectedFriend);
        updateChat();
    }

    /**
     * Sets the currently logged-in user.
     *
     * @param user The logged-in user
     */
    public void setLoggedInUser(User user) {
        this.actualUser = user;
        updateChat();
    }

    /**
     * Sends a message from the current user to the friend user.
     */
    public void sendMessage() {
        if (actualUser == null) {
            return;
        }
        String message = actualUser.getUsername() + ": " + messageField.getText();
        // Check if the message is not empty
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (ChatDatabase chatDatabase = new ChatDatabase(con)) {
                // Add message to the database

                chatDatabase.addMessage(actualUser.getUsername(), friendUser.getUsername(), message);
                // Clear message field and update chat display
                messageField.clear();
                updateChat();
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }
        updateChat();
    }

    /**
     * Updates the chat display with messages between the current user and the friend user.
     */
    private void updateChat() {
        // Get chat messages from the database
        if (actualUser == null) {
            return;
        }
        if (friendUser == null) {
            return;
        }
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (ChatDatabase chatDatabase = new ChatDatabase(con)) {
                ResultSet resultSet = chatDatabase.getChatMessages(actualUser.getUsername(), friendUser.getUsername());
                ObservableList<String> items = chatArea.getItems();
                items.clear(); // Clear current messages in ListView
                // Add new messages to ListView
                while (resultSet.next()) {
                    String message = resultSet.getString("message");
                    items.add(message);
                }
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }
    }
}
package com.example.zapoctovy;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;
import javafx.stage.Stage;
import java.io.IOException;
import java.sql.*;
import java.util.List;

/**
 * Controller class for the main functionality of the application.
 */
public class MainController {
    public ListView<String> fListView;
    public Button refreshButton;
    private List<User> allUsers;
    private Parent root;

    @FXML
    private ListView<String> friendListView;

    private User actualUser; // aktualne prihlaseny user
    private String selectedFriend;
    @FXML
    private TextField searchField;

    @FXML
    private Button logoutButton;
    ;
    String connectionURL = "jdbc:derby:" + DB_NAME + ";create=true"; // URL pro připojení k databázi

    private static final String DB_NAME = "demodb"; // Název databáze
    private static final String TABLE_NAME = "friends"; // Table name



    /**
     * Initializes the controller after its root element has been completely processed.
     */
    public void initialize(){
        try(Connection con = DriverManager.getConnection(connectionURL)) {

            initializeTable(con);

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }

        // Zobrazení všech uživatelů při spuštění aplikace
        displayAllUsers();

        Thread updateThread = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(50); //
                    Platform.runLater(this::displayAllUsers); // Update chat from JavaFX thread
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

    }

    /**
     * Handles the search functionality to find a user.
     */
    @FXML
    public void searchUser(){
        displayAllFriends();
        try (Connection con = DriverManager.getConnection(connectionURL)) {

            String username = searchField.getText();
            try (UserDatabase users = new UserDatabase(con)) {

                User user = users.getByUsername(username);

                friendListView.getItems().clear(); // Vyčistí seznam
                if (user == null) {
                    friendListView.getItems().clear();
                    friendListView.getItems().add("User not found");

                }
                else if(fListView.getItems().contains(user.getUsername())) {
                    friendListView.getItems().add("Already your friend");


                }  else {
                    // Pokud uživatel neexistuje, vypište chybovou zprávu

                    friendListView.getItems().add(user.getUsername());
                }
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }
    }

    /**
     * Handles the action when a friend is clicked.
     * @param mouseEvent The mouse event triggering the action.
     */
    public void friendsClick(MouseEvent mouseEvent){
        selectedFriend = fListView.getSelectionModel().getSelectedItem();
        if (selectedFriend != null) {
            // Vytvoření nového dialogu
            Dialog<ButtonType> dialog = new Dialog<>();
            dialog.setTitle("User Action");
            dialog.setHeaderText("What do you want to do with the user?");
            dialog.setContentText("You have selected the user: " + selectedFriend);

            // Přidání tlačítek pro zobrazení chatu a odebrání přítele
            ButtonType chatButton = new ButtonType("Show Chat");
            ButtonType removeButton = new ButtonType("Remove Friend");
            ButtonType cancelButton = new ButtonType("Cancel", ButtonBar.ButtonData.CANCEL_CLOSE);

            dialog.getDialogPane().getButtonTypes().addAll(chatButton, removeButton, cancelButton);

            // Zpracování odpovědi uživatele
            dialog.setResultConverter(dialogButton -> {
                if (dialogButton == chatButton) {
                    // Zavolání metody pro zobrazení chatu
                    loadChat();
                    System.out.println("Show chat with user: " + selectedFriend);
                } else if (dialogButton == removeButton) {
                    // Zavolání metody pro odebrání přítele
                    deleteFriend(selectedFriend);
                }
                return null;
            });

            // Zobrazení dialogu
            dialog.showAndWait();
        }
    }

    /**
     * Loads the chat window for communication with the selected friend.
     */
    private void loadChat() {
        Stage chatStage = new Stage();
        chatStage.setTitle("Chat");
        chatStage.setResizable(false);

        // Load the FXML file for the registration form
        FXMLLoader loader = new FXMLLoader(getClass().getResource("chat.fxml"));

        try {
            Parent root = loader.load();
            ChatController chatController = loader.getController(); // Získání odkazu na kontroler po načtení obsahu FXML souboru

            // Pass the logged-in user to the MainController
            chatController.setLoggedInUser(actualUser);
            chatController.setOtherUser(selectedFriend);

            // Set the scene with the loaded FXML root
            Scene scene = new Scene(root);
            chatStage.setScene(scene);

            // Show the registration form window
            chatStage.show();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Handles the deletion of a friend.
     * @param username The username of the friend to be deleted.
     */
    public void deleteFriend(String username){

        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (FriendDatabase friends = new FriendDatabase(con)) {

                friends.deleteUser(username);

            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        displayAllFriends();
        displayAllUsers();
    }

    /**
     * Handles the action when a mouse click is detected.
     */
    public void handleMouseClick() {
        String selectedFriend = friendListView.getSelectionModel().getSelectedItem();

        // You can display a dialog window here
        if (selectedFriend != null) {
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("Add Friend");
            alert.setHeaderText("Do you really want to add this friend?");
            alert.setContentText("You selected: " + selectedFriend);

            // Adding buttons
            ButtonType addButton = new ButtonType("Add");
            ButtonType cancelButton = new ButtonType("Cancel");

            alert.getButtonTypes().setAll(addButton, cancelButton);

            // Handling user response
            alert.showAndWait().ifPresent(buttonType -> {
                if (buttonType == addButton) {
                    // Add friend code goes here
                    String[] strings = selectedFriend.split(", ");
                    try (Connection con = DriverManager.getConnection(connectionURL)) {
                        try (UserDatabase users = new UserDatabase(con)) {
                            User user = users.getByUsername(strings[0]);
                            if (user != null) {
                                addFriend(actualUser, user);
                            } else {
                                System.out.println("User not found");
                            }
                        } catch (UserDBException ex) {
                            throw new RuntimeException(ex);
                        }
                    } catch (SQLException ex) {
                        throw new RuntimeException(ex);
                    }
                }
                displayAllFriends();
            });
        }
    }

    /**
     * Displays all users in the application.
     */
    private void displayAllUsers() {
        if(actualUser == null)
        {
            return;
        }
        displayAllFriends();
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (UserDatabase users = new UserDatabase(con)) {
                // Získání všech uživatelů
                allUsers = users.getAllUsers();

                friendListView.getItems().clear(); // Vyčistí seznam přátel před přidáním nových uživatelů

                for (User user : allUsers) {

                    if(!fListView.getItems().contains(user.getUsername()) && !user.getUsername().equals(actualUser.getUsername()))
                    {
                        System.out.println(user.getUsername() + " - " + actualUser.getUsername());
                        friendListView.getItems().add(user.getUsername());
                    }
                }
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }
    }

    /**
     * Displays all friends of the current user.
     */
    public void displayAllFriends(){
        if(actualUser == null)
        {
            return;
        }
        fListView.getItems().clear(); // Vymazat všechny položky v ListView před aktualizací
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (FriendDatabase friends = new FriendDatabase(con)) {
                ResultSet resultSet = friends.getFriendsForUser(actualUser.getUsername());

                if (resultSet.next()) { // Pokud uživatel má přátele
                    do{
                        String friendName = resultSet.getString("hisFriend");
                        friendName = friendName.equals(actualUser.getUsername()) ? resultSet.getString("actualLoggedUser") : friendName;
                        fListView.getItems().add(friendName);
                    } while (resultSet.next());
                } else {
                    fListView.getItems().add("No friends yet.");
                }
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }
    }

    /**
     * Adds a friend for the current user.
     * @param actual The logged-in user.
     * @param added The user to be added as a friend.
     */
    public void addFriend(User actual, User added) {
        String connectionURL = "jdbc:derby:" + DB_NAME + ";create=true"; // Database connection URL

        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (FriendDatabase friends = new FriendDatabase(con)) {
                friends.addFriend(actual.getUsername(), added.getUsername());
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }
        displayAllUsers();
    }

    /**
     * Sets the currently logged-in user.
     * @param user The user who is currently logged in.
     */
    public void setLoggedInUser(User user) {
        this.actualUser = user;
        displayAllUsers();
    }

    /**
     * Initializes the database table.
     * @param con The database connection.
     * @throws SQLException if a database access error occurs.
     */
    private static void initializeTable(Connection con) throws SQLException {
        try (Statement stmt = con.createStatement()) {
            // Check if the table exists
            DatabaseMetaData metaData = con.getMetaData();
            ResultSet tables = metaData.getTables(null, null, TABLE_NAME.toUpperCase(), null); // Default schema name is "APP"
            if (tables.next()) { // If the table exists, drop it

                System.out.println("Table '" + TABLE_NAME + "' already exists.");
            }else {
                // Create a new table with the specified columns
                String createTableQuery = "CREATE TABLE " + TABLE_NAME + " (actualLoggedUser varchar(30), hisFriend varchar(30))";
                stmt.executeUpdate(createTableQuery);
                System.out.println("Table '" + TABLE_NAME + "' created successfully.");
            }

        } catch (SQLException e) {
            throw new RuntimeException("Error initializing table: " + e.getMessage(), e);
        }
    }

    /**
     * Logs out the current user.
     */
    public void logout() {
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            try (UserDatabase userDB = new UserDatabase(con)) {
                userDB.logout(actualUser.getUsername()); // Volání metody logout pro aktuálně přihlášeného uživatele
            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }

        // Zavření aktuálního okna
        Stage stage = (Stage) logoutButton.getScene().getWindow();
        stage.close();
    }

    public void refreshPage(ActionEvent actionEvent) {
        displayAllFriends();
        displayAllUsers();
    }

}
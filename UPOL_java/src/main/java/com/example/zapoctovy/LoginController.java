package com.example.zapoctovy;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import java.io.IOException;
import java.sql.*;

/**
 * Controller class for managing the login functionality.
 */
public class LoginController {
    private static final String DB_NAME = "demodb"; // Database name
    private static final String TABLE_NAME = "users"; // Table name

    @FXML
    private TextField usernameField;

    @FXML
    private PasswordField passwordField;

    @FXML
    private Button createAccountButton;

    @FXML
    private Label statusLabel;

    private Parent root;
    public User loggedUser;

    String connectionURL = "jdbc:derby:" + DB_NAME + ";create=true"; // Database connection URL

    private UserDatabase userDB;

    /**
     * Initializes the login controller.
     */
    @FXML
    public void initialize() {
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            initializeTable(con);
            userDB = new UserDatabase(con); // Initialize UserDatabase
        } catch (SQLException | UserDBException e) {
            throw new RuntimeException(e);
        }

        createAccountButton.setOnAction(event -> {
            Stage registrationStage = new Stage();
            registrationStage.setTitle("User Registration");

            // Load the FXML file for the registration form
            FXMLLoader loader = new FXMLLoader(getClass().getResource("registration.fxml"));
            registrationStage.setResizable(false);

            try {
                root = loader.load();
            } catch (IOException e) {
                e.printStackTrace();
                return;
            }

            // Set the scene with the loaded FXML root
            Scene scene = new Scene(root);
            registrationStage.setScene(scene);

            // Show the registration form window
            registrationStage.show();
        });
    }

    /**
     * Redirects to the main messenger window after successful login.
     */
    private void toTheMain() {
        Stage mainStage = new Stage();
        mainStage.setTitle("Messenger");
        mainStage.setResizable(false);

        // Load the FXML file for the main messenger window
        FXMLLoader loader = new FXMLLoader(getClass().getResource("main1.fxml"));
        Parent root;
        try {
            root = loader.load();
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        // Get the controller instance from the loader
        MainController mainController = loader.getController();

        // Pass the logged-in user to the MainController
        mainController.setLoggedInUser(loggedUser);

        // Set the scene with the loaded FXML root
        Scene scene = new Scene(root);
        mainStage.setScene(scene);

        // Show the main messenger window
        mainStage.show();
    }

    /**
     * Initializes the users table if not already existing.
     *
     * @param con Connection to the database
     * @throws SQLException    If an SQL error occurs
     * @throws UserDBException If there is an error initializing the table
     */
    private static void initializeTable(Connection con) throws SQLException, UserDBException {


        try (Statement stmt = con.createStatement()) {



            DatabaseMetaData metaData = con.getMetaData();
            ResultSet tables = metaData.getTables(null, null, TABLE_NAME.toUpperCase(), null); // Default schema name is "APP"
            if (tables.next()) { // If the table exists, drop it

                System.out.println("Table '" + TABLE_NAME + "' already exists.");
            }else{
            // Create a new table with the specified columns
            String createTableQuery = "CREATE TABLE " + TABLE_NAME + " (name varchar(60), surname varchar(50), username varchar(30), password varchar(60), dateofbirth date, is_logged_in boolean)";
            stmt.executeUpdate(createTableQuery);
            System.out.println("Table '" + TABLE_NAME + "' created successfully with the new column 'is_logged_in'.");
            }
        } catch (SQLException e) {
            throw new UserDBException("Error initializing table: " + e.getMessage(), e);
        }
    }

    /**
     * Handles the login process.
     */
    public void login() {
        String username = usernameField.getText();
        char[] password = passwordField.getText().toCharArray();
        try (Connection con = DriverManager.getConnection(connectionURL)) {
            userDB = new UserDatabase(con); // Initialize UserDatabase

            try {
                User loggedInUser = userDB.getByUsername(username); // Retrieve user from database
                if (loggedInUser != null) { // If user exists
                    String storedPassword = loggedInUser.getPassword();
                    if (storedPassword.equals(new String(password))) { // Check if passwords match
                        // Set the loggedIn status of the user to true
                        userDB.login(username);
                        statusLabel.setText("Login successful");
                        loggedUser = loggedInUser;

                        toTheMain();
                    } else {
                        statusLabel.setText("Invalid password");
                    }
                } else {
                    statusLabel.setText("User not found");
                }
            } catch (UserDBException e) {
                throw new RuntimeException(e);
            }
        } catch (SQLException | UserDBException e) {
            throw new RuntimeException(e);
        }
    }
}
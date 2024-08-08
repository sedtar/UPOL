package com.example.zapoctovy;
import java.sql.*;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;

import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;


public class RegistrationController {
    private static final String DB_NAME = "demodb"; // Název databáze
    private static final String TABLE_NAME = "users"; // Table name
    /***Register***/
    @FXML
    private TextField nameFieldR;

    @FXML
    private TextField surnameFieldR;

    @FXML
    private TextField usernameFieldR;

    @FXML
    private PasswordField passwordFieldR;

    @FXML
    private TextField dobFieldR;

    @FXML
    private Button registerButton;

    @FXML
    private Label statusLabelR;

    @FXML
    private void newUser(){
        String name = nameFieldR.getText();
        String surname = surnameFieldR.getText();
        String username = usernameFieldR.getText();
        String password = passwordFieldR.getText();
        String dobText = dobFieldR.getText();
        String connectionURL = "jdbc:derby:" + DB_NAME + ";create=true"; // URL pro připojení k databázi
        try (Connection con = DriverManager.getConnection(connectionURL)) {


            try (UserDatabase users = new UserDatabase(con)) {

                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
                LocalDate dob = LocalDate.parse(dobText, formatter);
                Date dateOfBirth = Date.valueOf(dob);
                // Check if the user already exists
                if (users.getByUsername(username) != null) {
                    statusLabelR.setText("User with username " + username + " already exists.");
                    //throw new IllegalArgumentException("User with username " + username + " already exists.");

                }else{
                    // Insert the user into the database
                    users.create(name, surname, username, password, dateOfBirth);
                    System.out.println(users.getByUsername("admin")); //
                    statusLabelR.setText("User registered successfully");
                }

            } catch (UserDBException ex) {
                throw new RuntimeException(ex);
            }
        } catch (SQLException ex) {
            throw new RuntimeException(ex);
        }

    }
}

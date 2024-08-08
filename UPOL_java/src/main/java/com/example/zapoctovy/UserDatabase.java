package com.example.zapoctovy;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;


public class UserDatabase implements AutoCloseable {
    private static final String TABLE_NAME = "users"; // Table name
    private final PreparedStatement getByUsernameStmt;

    private final PreparedStatement insertStmt;
    private final PreparedStatement deleteStmt;
    private final Connection con;

    private final PreparedStatement loginStmt;
    private final PreparedStatement logoutStmt;
    public UserDatabase(Connection con) throws UserDBException {
        try {
            this.con = con;
            getByUsernameStmt = con.prepareStatement("SELECT * FROM users WHERE (username = ?)");
            insertStmt = con.prepareStatement("INSERT INTO users (name, surname, username, password, dateofbirth, is_logged_in) VALUES (?, ?, ?, ?, ?, ?)");
            deleteStmt = con.prepareStatement("DELETE FROM users WHERE (username = ?)");
            // Připravené dotazy pro přihlášení a odhlášení
            loginStmt = con.prepareStatement("UPDATE users SET is_logged_in = TRUE WHERE username = ?");
            logoutStmt = con.prepareStatement("UPDATE users SET is_logged_in = FALSE WHERE username = ?");

        } catch (SQLException e) {
            throw new UserDBException("Unable to initialize prepared statements.", e);
        }
    }

    public List<User> getAllUsers() throws UserDBException {
        List<User> users = new ArrayList<>();
        String query = "SELECT * FROM " + TABLE_NAME;

        try (PreparedStatement statement = con.prepareStatement(query);
             ResultSet resultSet = statement.executeQuery()) {

            while (resultSet.next()) {
                String name = resultSet.getString("name");
                String surname = resultSet.getString("surname");
                String username = resultSet.getString("username");
                String password = resultSet.getString("password");
                Date dateOfBirth = resultSet.getDate("dateofbirth");
                Boolean is_logged_in = resultSet.getBoolean("is_logged_in");
                // Získání dalších informací o uživateli podle potřeby

                User user = new User(name, surname, username, password, dateOfBirth, is_logged_in);
                // Vytvoření instance uživatele a přidání do seznamu
                users.add(user);
            }
        } catch (SQLException e) {
            throw new UserDBException("Error retrieving users from the database.", e);
        }

        return users;
    }



    // Metoda pro získání uživatelů podle uživatelského jména
        public User getByUsername(String username) throws UserDBException {

            User user = null;
            try {

                // Nastavení hodnoty uživatelského jména do připraveného dotazu
                getByUsernameStmt.setString(1, username);
                try (ResultSet results = getByUsernameStmt.executeQuery()) {
                    if (results.next())
                        user = new User(results.getString("name"), results.getString("surname"), results.getString("username"),results.getString("password"), results.getDate("dateofbirth"), results.getBoolean(("is_logged_in")));
                }
            } catch (SQLException e) {
                throw new UserDBException("Unable to find a user", e);
            }

            return user;
        }
    // Metoda pro přihlášení uživatele
    public void login(String username) throws UserDBException {
        try {
            loginStmt.setString(1, username);
            loginStmt.executeUpdate();
        } catch (SQLException e) {
            throw new UserDBException("Unable to login user", e);
        }
    }
    // Metoda pro odhlášení uživatele
    public void logout(String username) throws UserDBException {
        try {
            logoutStmt.setString(1, username);
            logoutStmt.executeUpdate();
        } catch (SQLException e) {
            throw new UserDBException("Unable to logout user", e);
        }
    }


    public User create(String username, String password, String name, String surname, Date date) throws UserDBException {
        try {

            insertStmt.setString(1, username);
            insertStmt.setString(2, password);
            insertStmt.setString(3, name);
            insertStmt.setString(4, surname);
            insertStmt.setDate(5, date);
            insertStmt.setBoolean(6, false);

            insertStmt.executeUpdate();

            return new User(username, password, name, surname, date, false);
        } catch (SQLException e) {
            throw new UserDBException("Unable to create new user", e);
        }
    }


    @Override
    public void close() {
        try {
            getByUsernameStmt.close();
            insertStmt.close();
            deleteStmt.close();
            loginStmt.close();
            logoutStmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }


}

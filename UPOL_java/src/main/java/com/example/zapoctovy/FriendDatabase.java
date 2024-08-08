package com.example.zapoctovy;

import java.sql.*;

/**
 * Provides methods to interact with the FRIENDS table in the database.
 */
public class FriendDatabase implements AutoCloseable {

    private static final String TABLE_NAME = "FRIENDS";
    private final PreparedStatement getByUserStmt;
    private final PreparedStatement insertStmt;
    private final PreparedStatement deleteByUserStmt;
    private final PreparedStatement deleteUserStmt;

    /**
     * Constructs a FriendDatabase object with the given database connection.
     *
     * @param con The database connection
     * @throws UserDBException If there is an error initializing the prepared statements
     */
    public FriendDatabase(Connection con) throws UserDBException {
        try {
            getByUserStmt = con.prepareStatement("SELECT * FROM " + TABLE_NAME + " WHERE actualLoggedUser = ? OR hisFriend = ?");

            insertStmt = con.prepareStatement("INSERT INTO " + TABLE_NAME + " (actualLoggedUser, hisFriend) VALUES (?, ?)");
            deleteByUserStmt = con.prepareStatement("DELETE FROM " + TABLE_NAME + " WHERE actualLoggedUser = ?");
            deleteUserStmt = con.prepareStatement("DELETE FROM " + TABLE_NAME + " WHERE hisFriend = ?");
        } catch (SQLException e) {
            throw new UserDBException("Unable to initialize prepared statements.", e);
        }
    }

    /**
     * Retrieves friends associated with the given username.
     *
     * @param username The username to fetch friends for
     * @return A ResultSet containing the friends
     * @throws UserDBException If there is an error fetching friends
     */
    public ResultSet getFriendsForUser(String username) throws UserDBException {
        try {
            getByUserStmt.setString(1, username);
            getByUserStmt.setString(2, username);
            return getByUserStmt.executeQuery();
        } catch (SQLException e) {
            throw new UserDBException("Unable to fetch friends for user", e);
        }
    }

    /**
     * Adds a friend relationship between two users.
     *
     * @param actualLoggedUser The username of the user initiating the friendship
     * @param hisFriend        The username of the friend to be added
     * @throws UserDBException If there is an error adding the friend
     */
    public void addFriend(String actualLoggedUser, String hisFriend) throws UserDBException {
        try {
            insertStmt.setString(1, actualLoggedUser);
            insertStmt.setString(2, hisFriend);
            insertStmt.executeUpdate();
        } catch (SQLException e) {
            throw new UserDBException("Unable to add a friend", e);
        }
    }

    /**
     * Deletes a user from the FRIENDS table.
     *
     * @param userToDelete The username of the user to delete
     * @throws UserDBException If there is an error deleting the user
     */
    public void deleteUser(String userToDelete) throws UserDBException {
        try {
            deleteUserStmt.setString(1, userToDelete);
            deleteUserStmt.executeUpdate();
        } catch (SQLException e) {
            throw new UserDBException("Unable to delete user", e);
        }
    }

    /**
     * Closes the prepared statements associated with this FriendDatabase object.
     */
    @Override
    public void close() {
        try {
            getByUserStmt.close();
            insertStmt.close();
            deleteByUserStmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
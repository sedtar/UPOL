package com.example.zapoctovy;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class User {


    private  String userName;

    private  String Password;
    private Boolean is_logged_in;
    private  String Name;
    private  String Surname;
    private  Date dateOfBirth;
    private boolean loggedIn;
    private boolean isAdmin;
    //private List<Chat> chats;
    private List<User> friends;

    private List<Chat> chats;



    public User(String Name, String Surname, String userName, String Password, Date dateOfBirth, Boolean is_logged_in) {
        this.Name = Name;
        this.Surname = Surname;
        this.userName = userName;
        this.Password = Password;
        this.dateOfBirth = dateOfBirth;
        this.is_logged_in = is_logged_in;

    }
    @Override
    public String toString() {


        return "User{" +
                "name=" + Name +
                ", surname='" + Surname + '\'' +
                ", userName='" + userName + '\'' +
                ", password='" + Password + '\'' +
                ", Date of Birth=" + dateOfBirth.toString() +
                '}';
    }


    public boolean getLoggedIn(){
        return is_logged_in;
    }
    public String getUsername(){
        return userName;
    }



    public String getPassword() {
        return Password;
    }
}

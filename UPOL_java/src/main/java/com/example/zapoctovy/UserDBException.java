package com.example.zapoctovy;

public class UserDBException extends Exception {

    private static final long serialVersionUID = 5249388341630044966L;
    public UserDBException(String msg, Exception e) {
        super(msg, e);
    }

}

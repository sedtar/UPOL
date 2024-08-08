module com.example.zapoctovy {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.sql;


    opens com.example.zapoctovy to javafx.fxml;
    exports com.example.zapoctovy;
}
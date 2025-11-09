// src/App.jsx
import React, { useState } from "react";
import { useEffect } from "react";
import "./css/style.css";
import Register from "./components/Register";
import Chat from "./components/Chat";
import Login from "./components/Login";
import NewChat from "./components/NewChat";

function App() {

    const [isLogged, setIsLogged] = useState(false);
    const [username, setUsername] = useState("");
    const [currentPage, setCurrentPage] = useState("login");


    useEffect(() => {
        const savedUser = localStorage.getItem("username");
        if (savedUser) {
            setUsername(savedUser);
            setIsLogged(true);

            setCurrentPage("main");
        }
    }, []);


    const handleLoginSuccess = (username) => {
        setUsername(username);
        setIsLogged(true);
    };

    const handleLogout = () => {
        localStorage.removeItem("username");
        setIsLogged(false);
        setUsername("");
        setCurrentPage("login"); // přepnutí zpět na login
    };


    return (
        <div className="container">
            {currentPage === "login" && !isLogged && (
                <Login
                    onLoginSuccess={(username) => {
                        handleLoginSuccess(username);
                        setCurrentPage("main");
                    }}
                    onShowRegister={() => setCurrentPage("register")}
                />
            )}

            {currentPage === "register" && !isLogged && (
                <Register onBackToLogin={() => setCurrentPage("login")} />
            )}

            {currentPage === "main" && isLogged && (
                <Chat
                    Logout={() => {
                        handleLogout();
                        setCurrentPage("login");
                    }}
                    onNewChat={() => setCurrentPage("newChat")}
                    username={username}
                />
            )}

            {currentPage === "newChat" && isLogged && (
                <NewChat onBackToMain={() => setCurrentPage("main")} />
            )}
        </div>
    );
}

export default App;

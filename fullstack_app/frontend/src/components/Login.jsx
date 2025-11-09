// src/components/Login.jsx
import React, { useState } from "react";

const Login = ({ onLoginSuccess, onShowRegister }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            if (data.success) {
                setMessage("Login successful!");
                localStorage.setItem("username", username);
                onLoginSuccess(username); // předá username a změní stav v App.jsx
            } else {
                setMessage("Invalid username or password");
            }
        } catch (error) {
            console.error(error);
            setMessage("Server error");
        }
    };

    return (
        <div className="card card--form">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <label>Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                    />
                </div>
                <div className="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                    />
                </div>
                <button type="submit">Log in</button>
                <button type="button" onClick={onShowRegister}>
                    Create an account
                </button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Login;

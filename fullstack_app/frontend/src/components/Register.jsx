
import { useState } from "react"; // useState -- react hook that allows you to save and change stae (e.g. the content of inputs or messages). Each call to useState returns a pair :[value, function_to_change]

const Register = ({ onBackToLogin }) => { //Register is a functional component, i.el. a part of an application thath can be reused
    //({ onBackToLogin }) means that component receives props (input parameters from the parent) and immediately desctructurizes them to extract only one item -onBacktoLogin function



    //here we use the react hook useState, which allows us to store variables that change during the life of a component
    const [username, setUsername] = useState(""); //content of the "username" text field
    const [email, setEmail] = useState("");//content of the "email" text field
    const [password, setPassword] = useState("");//content of the "password" text field

    const [message, setMessage] = useState("");

    const handleRegister = async (e) => { // it is  an asynchronous function(async), it will be called when the form is submitted (e.g. after clicking the register button)
        e.preventDefault(); //e stands for event object -- its an automatic argument that the browser give whenever an event happens (a click, form submit (onSubmit), ), do not perform the default form hehavior (reload the page)

        if (!username || !password) { // if the user has not filled in a username or password
            setMessage("Please enter username and password");
            return; //return terminates the functon -- fetch() is not run anymore
        }

        try { //communication with server (backnend)
            const response = await fetch("http://localhost:5000/register", { //sends a http request to server
                method: "POST", // method POST, because we send a data
                headers: { "Content-Type": "application/json" },  // says that the body is JSON
                body: JSON.stringify({ username, email, password }), //convets the object {usrname, password} to JSON
            });

            const data = await response.json(); // waits for a response from the server, but does not block the entire program.
            setMessage(data.success ? "User registered successfully!" : data.message); //if success true, then user is registered
        } catch (error) {
            console.error(error);
            setMessage("Server error");
        }
    };

    return ( //function of component Register returns JSX, which is an HTML-like notation that React translates into actual HTML in the browser.
        <div className="card card--form"> {/*The form's wrapper container.*/}
            <h2>Register</h2>
            <form onSubmit={handleRegister}>
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
                    <label>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
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
                <button type="submit">Register</button>
                <button onClick={onBackToLogin}> Already have an account? Login</button> {/*Calls onBackToLogin(), React will render back the login form (according to the ternary operator)*/}

            </form>


            {message && <p>{message}</p>}
        </div>
    );
};

export default Register;

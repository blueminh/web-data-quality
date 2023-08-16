import "./Login.css";
import '../../styleguide.css'
import React, {useState, useContext, useEffect} from "react";
// import {bake_cookie} from "sfcookies";
import {Button} from "react-bootstrap";
// import {LoginContext} from "../../App";
import AuthContext from "../../contexts/AuthProvider";
import { useNavigate } from "react-router-dom";
import authService from "../../services/authService";

function LoginPage() {
    const [getEmail, setEmail] = useState("null");
    const [getPassword, setPassword] = useState("null");
    const [getLoginErrorActive, setLoginErrorActive] = useState(false);
    // eslint-disable-next-line
    const [message, setMessage] = useState("")
    const {auth, setAuth} = useContext(AuthContext)
    const navigate = useNavigate()

    /**
     * Handler to update the e-mail field.
     * @param event - the current user event.
     */
    const updateEmail = (event) => { setEmail(event.target.value); }

    /**
     * Handler to update the password field.
     * @param event - the current user event.
     */
    const updatePassword = (event) => { setPassword(event.target.value); }

    /**
     * Handler submit the login data.
     * @param event - the current user event containing
     * the login form info.
     */
    const onSubmitHandle = (event) => {
        event.preventDefault();

        // Throw an error if etiher of the fields is empty.
        // if (getEmail === "null" || getPassword === "null") {
        //     setLoginErrorActive(true);
        //     return false;
        // }

        const data = {
            email: getEmail,
            password: getPassword
        }

        authService.submitLogin(data)
            .then(response => {
                console.log("response", response)
                console.log("Received auth token! ", response.data);
                setLoginErrorActive(false);
                setAuth({
                    isLoggedIn: true,
                    username: response.data.user.username,
                    email: response.data.user.email,
                    roles: response.data.user.roles
                });
                console.log(response.data.user.roles)
                navigate("/calculation")
            }) // If login failed, throw an error to the user.
            .catch(e => {
                // const validationError = new ValidationError("Login Failed: ", e)
                // const errorMessage = validationError.readErrorObjectLogin();
                setMessage("Wrong email or password");
                setLoginErrorActive(true);
                console.log(e)
            });
    }

    return (
        <div className="poppins-bold-white-49px Back">
            <header className="LoginHeader">
                Log In
            </header>
            <div className="LoginBackground poppins-normal-white-20px">
                <form>
                    <hr className="Separator"/>

                    <div className="form-group LoginLabelBox">
                        <label htmlFor="emailLoginForm" className="LoginLabel">Username</label>
                        <input type="email" className="form-control InputField" id="emailLoginForm"
                               onChange={updateEmail}
                               placeholder="Username..." required/>
                    </div>
                    <div className="form-group LoginLabelBox">
                        <label htmlFor="passwordLoginForm" className="LoginLabel">Password</label>
                        <input type="password" className="form-control InputField" id="passwordLoginForm"
                               onChange={updatePassword}
                               placeholder="Password..." required/>
                    </div>
                    <hr className="Separator"/>
                </form>
                <div className="LoginContainer">
                    {(getLoginErrorActive && 
                            <div className="LoginLabelBoxError poppins-normal-ghost-16px" style={{ color: "red"}}>
                                <p>Login failed. {message}</p>
                            </div>
                        ) || (!getLoginErrorActive && 
                            <div className="LoginLabelBoxSuccess poppins-normal-ghost-16px" style={{ color: "green"}}>
                                <p>{message}</p>
                            </div>
                        )
                    }
                    <Button className="btn primary-button poppins-medium-white-22px btn-lg" onClick={onSubmitHandle}>
                        Log In
                    </Button>
                </div>
        </div>
    </div>
    );
}

export default LoginPage;
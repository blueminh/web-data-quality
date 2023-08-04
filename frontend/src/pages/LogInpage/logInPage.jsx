import "./Login.css";
import '../../styleguide.css'
import React, {useState} from "react";
// import {bake_cookie} from "sfcookies";
// import AuthService from "../../services/auth.service";
import {Button} from "react-bootstrap";
// import {LoginContext} from "../../App";
// import ValidationError from "../../error/ValidationError";

function LoginPage() {
    // const [, setLoggedIn]= useContext(LoginContext);
    const [getEmail, setEmail] = useState("null");
    const [getPassword, setPassword] = useState("null");
    const [getLoginErrorActive, setLoginErrorActive] = useState(false);
    // eslint-disable-next-line
    const [message, setMessage] = useState("")

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
        if (getEmail === "null" || getPassword === "null") {
            setLoginErrorActive(true);
            return false;
        }
        // Code to send request to backend here
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
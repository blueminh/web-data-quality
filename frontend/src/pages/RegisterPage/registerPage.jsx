import "./Register.css";
import '../../styleguide.css'
import React, {useState} from "react";
// import {bake_cookie} from "sfcookies";
import {Button} from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import authService from "../../services/authService";
import useLocalStorageAuth from "../../hooks/useLocalStorageAuth";

function RegisterPage() {
    const [getUsername, setUsername] = useState("null");
    const [getEmail, setEmail] = useState("null");
    const [getPassword, setPassword] = useState("null");
    const [getRegisterErrorActive, setRegisterErrorActive] = useState(false);
    // eslint-disable-next-line
    const [message, setMessage] = useState("")
    const {setAuth} = useLocalStorageAuth()
    const navigate = useNavigate()

    /**
     * Handler to update the e-mail field.
     * @param event - the current user event.
     */
    const updateUsername = (event) => { setUsername(event.target.value); }

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
        
        authService.submitRegsiter(getUsername, getEmail, getPassword)
            .then(response => {
                setRegisterErrorActive(false);
                setAuth({
                    isLoggedIn: true,
                    username: response.data.user.username,
                    email: response.data.user.email,
                    roles: response.data.user.roles
                });
                navigate("/calculation")
            }) // If login failed, throw an error to the user.
            .catch(e => {
                // const validationError = new ValidationError("Login Failed: ", e)
                // const errorMessage = validationError.readErrorObjectLogin();
                setMessage("");
                const returnedMessage = e?.response?.data?.msg;
                if(returnedMessage) {
                    setMessage(returnedMessage);
                }
                setRegisterErrorActive(true);
                console.log(e)
            });

        // authService.submitLogin(data)
        //     .then(response => {
        //         setLoginErrorActive(false);
        //         setAuth({
        //             isLoggedIn: true,
        //             username: response.data.user.username,
        //             email: response.data.user.email,
        //             roles: response.data.user.roles
        //         });
        //         navigate("/calculation")
        //     }) // If login failed, throw an error to the user.
        //     .catch(e => {
        //         // const validationError = new ValidationError("Login Failed: ", e)
        //         // const errorMessage = validationError.readErrorObjectLogin();
        //         setMessage("Wrong email or password");
        //         setLoginErrorActive(true);
        //         console.log(e)
        //     });
    }

    return (
        <div className="poppins-bold-white-49px Back">
            <header className="LoginHeader">
                Đăng ký
            </header>
            <div className="LoginBackground poppins-normal-white-20px">
                <form>
                    <hr className="Separator"/>

                    <div className="form-group LoginLabelBox">
                        <label htmlFor="emailLoginForm" className="LoginLabel">Tên tài khoản</label>
                        <input type="email" className="form-control InputField" id="usernameLoginForm"
                               onChange={updateUsername}
                               placeholder="Username..." required/>
                    </div>
                    <div className="form-group LoginLabelBox">
                        <label htmlFor="emailLoginForm" className="LoginLabel">Email</label>
                        <input type="email" className="form-control InputField" id="emailLoginForm"
                               onChange={updateEmail}
                               placeholder="Email..." required/>
                    </div>
                    <div className="form-group LoginLabelBox">
                        <label htmlFor="passwordLoginForm" className="LoginLabel">Mật khẩu</label>
                        <input type="password" className="form-control InputField" id="passwordLoginForm"
                               onChange={updatePassword}
                               placeholder="Password..." required/>
                    </div>
                    <hr className="Separator"/>
                </form>
                <div className="LoginContainer">
                    {(getRegisterErrorActive && 
                            <div className="LoginLabelBoxError poppins-normal-ghost-16px" style={{ color: "red"}}>
                                <p>Đăng ký không thành công: {message}</p>
                            </div>
                        ) || (!getRegisterErrorActive && 
                            <div className="LoginLabelBoxSuccess poppins-normal-ghost-16px" style={{ color: "green"}}>
                                <p>{message}</p>
                            </div>
                        )
                    }
                    <Button className="btn primary-button poppins-medium-white-22px btn-lg" onClick={onSubmitHandle}>
                        Đăng ký
                    </Button>
                </div>
        </div>
    </div>
    );
}

export default RegisterPage;
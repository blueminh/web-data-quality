import {Container, Nav, Navbar,  Button} from "react-bootstrap";
import "./navbar.css"
import { useContext } from "react";
import AuthContext from "../../contexts/AuthProvider";
import { useNavigate } from "react-router-dom";
import authService from "../../services/authService";



export default function NavigationBar() {
    const {auth, setAuth} = useContext(AuthContext)
    const navigate = useNavigate()
    const handleLogout = () => {
        authService.submitLogout()
            .then(response => {
                setAuth({
                    isLoggedIn: false,
                });
                navigate("/calculation")
            }) // If login failed, throw an error to the user.
            .catch(e => {
                console.log(e)
            });
    };

    return (
        <>
        <Navbar collapseOnSelect expand="lg" className="header-footer" sticky="top">
            <Container>
                <Navbar.Brand href="/">
                    <img
                        className="d-inline-block align-top kpmg-logo"
                        src="/img/logo3.png"
                        alt="KPMG logo"
                    />
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="/calculation">Calculation Tool</Nav.Link>
                        <Nav.Link href="/validation">Validation Tool</Nav.Link>
                    </Nav>
                    <Nav>
                    {auth.isLoggedIn ? 
                        <div>
                            <Button
                                className="primary-button btn-primary shadow-none btn-outline-dark button-navbar-padding"
                                onClick={handleLogout}
                            >
                                Đăng xuất
                            </Button>
                        </div>
                    : (<div>
                            <Button
                                className="primary-button btn-primary shadow-none btn-outline-dark button-navbar-padding"
                                href="/register"
                            >
                                Tạo tài khoản
                            </Button>
                            <Button
                                className="primary-button btn-primary shadow-none btn-outline-dark button-navbar-padding"
                                href="/login"
                            >
                                Đăng nhập
                            </Button>
                        </div>
                        ) 
                    }
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
        </>
    )
}
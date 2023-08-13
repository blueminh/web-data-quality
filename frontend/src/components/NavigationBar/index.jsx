import {Container, Nav, Navbar,  Button} from "react-bootstrap";
import "./navbar.css"
import { useContext, useEffect} from "react";

export default function NavigationBar() {
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
                    {true ? 
                        <div>
                            <Button
                                className="primary-button btn-primary shadow-none btn-outline-dark button-navbar-padding"
                            >
                                Log out
                            </Button>
                        </div>
                    : (<div>
                            <Button
                                className="primary-button btn-primary shadow-none btn-outline-dark button-navbar-padding"
                                href="/register"
                            >
                                Register
                            </Button>
                            <Button
                                className="primary-button btn-primary shadow-none btn-outline-dark button-navbar-padding"
                                href="/login"
                            >
                                Log In
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
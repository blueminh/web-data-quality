import {Container, Nav, Navbar} from "react-bootstrap";
import "./navbar.css"

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
                        <Nav.Link href="/home">Dashboard</Nav.Link>
                        <Nav.Link href="/lcr">LCR</Nav.Link>
                        <Nav.Link href="/nsfr">NSFR</Nav.Link>
                        <Nav.Link href="/input">Input Data</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
        </>
    )
}
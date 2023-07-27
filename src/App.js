import React from "react";
import {useState, createContext } from "react";
import {Routes, Route} from "react-router-dom";
import Nagivationbar from './components/NavigationBar'
import CalculationHomePage from "./pages/CalculationHomePage/homePage";
import LoginPage from "./pages/LogInpage/logInPage"
import './App.css'
import './Global.css'
import './styleguide.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import ValidationPage from "./pages/ValidationBoardPage";

export const LoginContext = createContext({
    state: {
        loggedIn: true
    },
    setState: () => {}
});


const App = () => {
    const [loggedIn, setLoggedIn] = useState(true);
    return (
        <LoginContext.Provider value={[loggedIn, setLoggedIn]}>
            <div>
                <Nagivationbar />
                <Routes>
                    <Route path='/' element={<CalculationHomePage />}></Route>
                    <Route path='/calculation' element={<CalculationHomePage />}></Route>
                    <Route path='/login' element={<LoginPage />}></Route>
                    <Route path='/validation' element={<ValidationPage/>}></Route>
                </Routes>
            </div>
        </LoginContext.Provider>
    )
}

export default App
import React from "react";
import {Routes, Route} from "react-router-dom";
import Nagivationbar from './components/NavigationBar'
import CalculationHomePage from "./pages/CalculationHomePage/homePage";
import ValidationHomePage from "./pages/ValidationHomePage/homePage";
import LoginPage from "./pages/LogInpage/logInPage"
import './App.css'
import './Global.css'
import './styleguide.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import RequireAuth from "./components/RequireAuth";
import AuthContext from "./contexts/AuthProvider";
import { useContext, useEffect } from 'react';


const App = () => {

    const {auth, setAuth} = useContext(AuthContext)
    useEffect(() => {
        console.log("auth updated to: ", auth);
    }, [auth])

    return (
        <div>
            <Nagivationbar />
            <Routes>
                <Route path='/' element={<CalculationHomePage />}></Route>
                <Route element={<RequireAuth />}>
                    <Route path='/calculation' element={<CalculationHomePage />} />
                </Route>
                <Route path='/login' element={<LoginPage />}></Route>
                <Route path='/validation' element={<ValidationHomePage />}></Route>
            </Routes>
        </div>
    )
}

export default App
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

const App = () => {
    return (
        <div>
            <Nagivationbar />
            <Routes>
                <Route path='/login' element={<LoginPage />}></Route>

                {/* <Route element={<RequireAuth />}> */}
                    <Route path='/' element={<CalculationHomePage />} />
                {/* </Route> */}

                <Route element={<RequireAuth />}>
                    <Route path='/calculation' element={<CalculationHomePage />} />
                </Route>

                {/* <Route element={<RequireAuth />}> */}
                <Route path='/validation' element={<ValidationHomePage />}></Route>
                {/* </Route> */}
            </Routes>
        </div>
    )
}

export default App
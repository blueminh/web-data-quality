import React from "react";
import {Routes, Route} from "react-router-dom";
import Nagivationbar from './components/NavigationBar'
import CalculationHomePage from "./pages/CalculationHomePage/homePage";
import ValidationHomePage from "./pages/ValidationHomePage/homePage";
import LoginPage from "./pages/LogInpage/logInPage"
import RegisterPage from "./pages/RegisterPage/registerPage";
import './App.css'
import './Global.css'
import './styleguide.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import RequireAuth from "./components/RequireAuth";
import Unauthorized from "./pages/Unauthorized/Unauthorized"

const App = () => {
    return (
        <div>
            <Nagivationbar />
            <Routes>
                <Route path='/login' element={<LoginPage />}></Route>
                <Route path='/register' element={<RegisterPage />}></Route>
                <Route path="/unauthorized" element={<Unauthorized />} />

                <Route element={<RequireAuth allowedRoles={["admin", "viewer"]}/>}>
                    <Route path='/' element={<CalculationHomePage />} />
                </Route>

                <Route element={<RequireAuth allowedRoles={["admin", "viewer"]}/>}>
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
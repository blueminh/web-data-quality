import React from "react";
import {Routes, Route} from "react-router-dom";
import Homepage  from './pages/HomePage/homePage';
import Nagivationbar from './components/NavigationBar'
import './App.css'
import './Global.css'
import './styleguide.css'
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
    return (
        <div>
            <Nagivationbar />
            <Routes>
            <Route path='/' element={<Homepage />}></Route>
            <Route path='/home' element={<Homepage />}></Route>
            </Routes>
        </div>
    )
}

export default App
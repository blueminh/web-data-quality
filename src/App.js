import React from "react";
import {Routes, Route} from "react-router-dom";
import Homepage  from './pages/HomePage';


const App = () => {
    return (
        <div>
            <Routes>
            <Route path='/' element={<Homepage />}></Route>
            </Routes>
        </div>
    )
}

export default App
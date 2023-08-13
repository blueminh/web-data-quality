import { Navigate, Outlet } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../contexts/AuthProvider";

const RequireAuth = () => {
    const {auth} = useContext(AuthContext)
    return (
        auth 
            ? <Outlet />
            : <Navigate to="/login" />
    );
}

export default RequireAuth;
import { Navigate, Outlet } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../contexts/AuthProvider";

const RequireAuth = ({allowedRoles = []}) => {
    const {auth} = useContext(AuthContext)

    if (!auth.isLoggedIn) {
        // Redirect to the login page if the user is not logged in
        return <Navigate to="/login" />;
    }

    if (auth.roles.some(role => allowedRoles.includes(role))) {
        // User has at least one of the allowed roles, allow access
        return <Outlet />;
    }

    return <Navigate to="/unauthorized" replace />;
}

export default RequireAuth;
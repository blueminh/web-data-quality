import axios from "axios";

class AuthService {

    /**
     * Submits user login data to the back end authentication server.
     * @param data the details of the user - a JSON structure containing
     *             a "username" and a "password" field.
     * @returns {Promise<axios.AxiosResponse<any>>} A response from the auth
     * back end server containing the token, if the provided login details
     * are valid.
     */
    submitLogin(data) {
        return axios.create({
            baseURL: "http://ec2-13-49-67-93.eu-north-1.compute.amazonaws.com:8085/",
            headers: {
                "Content-type": "application/json"
            },
        }).post("/api/users/login", data)
    }
}

const authService = new AuthService();

export default authService;
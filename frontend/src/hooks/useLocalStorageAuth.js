const useLocalStorageAuth = () => {
    const getAuth = () => {
      const storedAuthData = localStorage.getItem('authData');
      return storedAuthData ? JSON.parse(storedAuthData) : null;
    };
  
    const setAuth = (newAuthData) => {
      localStorage.setItem('authData', JSON.stringify(newAuthData));
    };
  
    return {
      getAuth,
      setAuth
    };
  };
  
  export default useLocalStorageAuth;
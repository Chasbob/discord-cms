import React, { useState, useEffect } from "react";

import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import { useLogin, Notification } from "react-admin";
import { ThemeProvider } from "@material-ui/styles";

const LoginForm = ({ theme }) => {
  const [loading, setLoading] = useState(false);
  const login = useLogin();

  useEffect(() => {
    const { searchParams } = new URL(window.location.href);
    const token = searchParams.get("token");
    if (token) {
      setLoading(true);
      login({ token });
    }
  }, []);

  const handleLogin = () => {
    setLoading(true);
    login(); // Do not provide token, just trigger the redirection
  };

  return (
    <ThemeProvider theme={theme}>
      <div>
        <CardActions>
          <Button
            variant="raised"
            type="submit"
            color="primary"
            onClick={handleLogin}
            disabled={loading}
          >
            {loading && <CircularProgress size={18} thickness={2} />}
            Login With Discord
          </Button>
        </CardActions>
      </div>
      <Notification />
    </ThemeProvider>
  );
};

export default LoginForm;

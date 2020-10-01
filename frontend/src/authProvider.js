const API_BASE = process.env.REACT_APP_API_BASE;
const cleanup = () => {
  // Remove the ?code&state from the URL
  window.history.replaceState(
    {},
    window.document.title,
    window.location.origin
  );
};
const authProvider = {
  login: ({ token }) => {
    if (token) {
      console.log("authProvider", token);
      localStorage.setItem("token", token);
      fetch(`${API_BASE}/me`, {
        headers: { Authorization: `Bearer ${token}` },
      }).then((response) => {
        if (!response.ok) {
          cleanup();
          return Promise.reject();
        }
      });
      cleanup();
      return Promise.resolve();
    }
    window.location.assign(`${API_BASE}/login`);
    return Promise.resolve();
  },
  logout: () => {
    localStorage.removeItem("token");
    return Promise.resolve();
  },
  checkAuth: () =>
    localStorage.getItem("token") ? Promise.resolve() : Promise.reject(),

  checkError: (error) => {
    const status = error.status;
    if (status === 401) {
      return Promise.reject();
    }
    return Promise.resolve();
  },
  getPermissions: (params) => Promise.resolve(),
};

export default authProvider;

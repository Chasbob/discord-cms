import { Admin, Resource, fetchUtils } from "react-admin";
import simpleRestProvider from "ra-data-simple-rest";
import React from "react";
import authProvider from "./authProvider";
import LoginForm from "./components/LoginForm";
import { MessageList, MessageEdit } from "./resources/Messages";
import { GuildList } from "./resources/Guilds";

const httpClient = (url, options = {}) => {
  if (!options.headers) {
    options.headers = new Headers({ Accept: "application/json" });
  }
  const token = localStorage.getItem("token");
  options.headers.set("Authorization", `Bearer ${token}`);
  return fetchUtils.fetchJson(url, options);
};
const API_BASE = process.env.REACT_APP_API_BASE;

const dataProvider = simpleRestProvider(`${API_BASE}`, httpClient);

const App = () => {
  return (
    <Admin
      loginPage={LoginForm}
      dataProvider={dataProvider}
      authProvider={authProvider}
    >
      <Resource name="messages" list={MessageList} edit={MessageEdit} />
      <Resource name="guilds" list={GuildList} />
    </Admin>
  );
};
export default App;

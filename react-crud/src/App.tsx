import React from "react";
import "./App.css";
import Nav from "./components/Nav";
import Menu from "./components/Menu";
import Products from "./admin/Products";
import Main from "./main/Main";
import { BrowserRouter, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Route path={"/"} exact component={Main} />
        <Route path={"/admin/products"} component={Products} />
      </BrowserRouter>
    </div>
  );
}

export default App;

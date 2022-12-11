import React, { Component } from "react";
import HomePage from "./HomePage";
import ContactPage from "./ContactPage";
import OrderPage from "./OrderPage";
import {BrowserRouter as Router, Switch, Link, Redirect, Route } from "react-router-dom"
import Appbar from "./appbar";

export default class RouterPage extends Component {
    constructor(props) {
      super(props);
    }
  
    render() {
      return (
        <div> 
            <div> 
                <Appbar />
            </div>
            <div> 
                <Router>
                    <Switch>
                        <Route exact path="/" component={HomePage} />
                        <Route path="/contact" component={ContactPage} />
                        <Route path="/order" component={OrderPage} />
                    </Switch>
                </Router>
            </div>
        </div>
      );
    }
  }

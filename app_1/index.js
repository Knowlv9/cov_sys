import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route } from "react-router-dom";
// import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

import Header from './Components/Header';
import Main from './Components/Main';
import Dashboard from './Components/Dashboard';
import Reception from './Components/Reception';
import Result from './Components/Result';
import Search from './Components/Search';
import Setting from './Components/Setting';

ReactDOM.render(
  <React.StrictMode>
	  <BrowserRouter>
		  <Route path="/Header" component={Header} exact />
		  <Route path="/" component={Main} exact />
		  <Route path="/Dashboard" Component={Dashboard} exact />
		  <Route path="/Reception" Component={Reception} exact />
		  <Route path="/Result" Component={Result} exact />
		  <Route path="/Search" Component={Search} exact />
		  <Route path="/Setting" Component={Setting} exact />
	  </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

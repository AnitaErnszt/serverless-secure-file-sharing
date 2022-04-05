import React from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar navbar-light bg-light p-3">
      <div className="container-fluid">
        <ul className="navbar-nav mr-auto d-flex flex-row">
          <li className="nav-item">
            <NavLink
              className="nav-link"
              // onClick={() => window.location.reload()}
              // exact={true}
              to="/"
            >
              Home
            </NavLink>
          </li>
          <li className="nav-item ms-4">
            <NavLink
              className="nav-link"
              // onClick={() => window.location.reload()}
              // exact={true}
              to="/download"
            >
              Download
            </NavLink>
          </li>
          <li className="nav-item ms-4">
            <NavLink
              className="nav-link"
              // onClick={() => window.location.reload()}
              // exact={true}
              to="/delete"
            >
              Delete
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;

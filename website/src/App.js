import React, { Fragment } from "react";
import FileDrop from "./FileDrop";
import Navbar from "./Navbar";
import { Route, Routes } from "react-router-dom";
import DownloadFile from "./DownloadFile";
import DeleteFile from "./DeleteFile";

const App = () => (
  <Fragment>
    <Navbar />
    <div className="container">
      <Routes>
        <Route exact path="/" element={<FileDrop />} />
        <Route exact path="/download" element={<DownloadFile />} />
        <Route exact path="/delete" element={<DeleteFile />} />
      </Routes>
    </div>
  </Fragment>
);

export default App;

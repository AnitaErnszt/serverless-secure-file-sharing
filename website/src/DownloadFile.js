import React, { Fragment, useState, useEffect } from "react";
import { Button, Input, Notification } from "react-rainbow-components";
import api, { extractAPIErrorString } from "./api/index";
import axios from "axios";

const DownloadFile = () => {
  const [publicKey, setPublicKey] = useState("");
  const [accessCode, setAccessCode] = useState("");
  const [isLoading, setLoading] = useState(false);
  const [state, setState] = useState(false);

  useEffect(() => {
    if (state) {
      setTimeout(() => {
        setState(null);
      }, 4000);
    }
  }, [state]);

  const handleDownload = () => {
    if (!publicKey) {
      // TODO: add some error message
      return null;
    }

    setLoading(true);
    api
      .get(
        `/files/${publicKey}`,
        accessCode ? { params: { access_code: accessCode } } : null
      )
      .then(
        ({ data }) => {
          axios({
            url: data.data.download_url,
            method: "GET",
            responseType: "blob",
          }).then((res) => {
            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", data.data.file_name);
            document.body.appendChild(link);
            link.click();
            setState({ type: "success" });
            setAccessCode(null);
            setPublicKey(null);
            setLoading(false);
          });
        },
        (err) => {
          setState({ type: "error", message: extractAPIErrorString(err) });
          setLoading(false);
        }
      );
  };

  return (
    <Fragment>
      <h3 className="mt-5 mb-4 text-center">
        Enter your file details below. Files can only be accessed once.
      </h3>
      {state && (
        <Notification
          className="rainbow-error"
          title={
            state.type === "error"
              ? "Error"
              : "Successfully downloaded the file"
          }
          description={state.message ? state.message : null}
          icon={state.type}
          onRequestClose={() => setState(null)}
        />
      )}
      <div className="col-8 offset-2 mt-5">
        <Input
          label="Public key"
          placeholder="public key"
          type="text"
          name="public_key"
          className="react-rainbow rainbow-p-around_medium"
          required
          value={publicKey}
          onChange={(e) => setPublicKey(e.target.value)}
        />
        <Input
          label="Access code"
          placeholder="**********"
          type="password"
          name="access_code"
          className="react-rainbow rainbow-p-around_medium mt-3"
          value={accessCode}
          onChange={(e) => setAccessCode(e.target.value)}
        />
        <Button
          variant="brand"
          className="rainbow-m-around_medium mt-5"
          label="Download file"
          disabled={!publicKey}
          isLoading={isLoading}
          onClick={handleDownload}
        />
      </div>
    </Fragment>
  );
};

export default DownloadFile;

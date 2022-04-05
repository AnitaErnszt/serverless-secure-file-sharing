import React, { Fragment, useState, useEffect } from "react";
import { Button, Input, Notification } from "react-rainbow-components";
import api, { extractAPIErrorString } from "./api/index";

const DeleteFile = () => {
  const [publicKey, setPublicKey] = useState(" ");
  const [deleteCode, setDeleteCode] = useState("");
  const [state, setState] = useState(false);
  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    if (state) {
      setTimeout(() => {
        setState(null);
      }, 4000);
    }
  }, [state]);

  const handleDelete = () => {
    if (!publicKey || !deleteCode) {
      // TODO: add some error message
      return null;
    }

    setLoading(true);
    api
      .delete(`/files/${publicKey}`, { delete_code: deleteCode })
      .then(
        () => {
          setState({ type: "success" });
        },
        (err) => {
          setState({ type: "error", message: extractAPIErrorString(err) });
        }
      )
      .finally(() => setLoading(false));
  };

  //   TODO: maybe support getting these values from the URL...

  return (
    <Fragment>
      {state && (
        <Notification
          className="rainbow-error"
          title={
            state.type === "error" ? "Error" : "Successfully deleted the file"
          }
          description={state.message ? state.message : ""}
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
          label="Delete code"
          placeholder="**********"
          type="password"
          name="delete_code"
          className="react-rainbow rainbow-p-around_medium mt-3"
          value={deleteCode}
          onChange={(e) => setDeleteCode(e.target.value)}
        />
        <Button
          variant="destructive"
          className="rainbow-m-around_medium mt-5"
          label="Destroy file"
          disabled={!publicKey}
          isLoading={isLoading}
          onClick={handleDelete}
        />
      </div>
    </Fragment>
  );
};

export default DeleteFile;

import React, { Fragment, useState } from "react";
import {
  FileSelector,
  Button,
  Input,
  HelpText,
  ButtonIcon,
} from "react-rainbow-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopy } from "@fortawesome/free-solid-svg-icons";
import api, { extractAPIErrorString } from "./api/index";
import axios from "axios";

const containerStyles = {
  maxWidth: 300,
  margin: "auto",
};

const FileDrop = () => {
  const [files, setFiles] = useState([]);
  const [isLoading, setLoading] = useState(false);
  const [successData, setSuccessData] = useState(null);
  const [accessCode, setAccessCode] = useState(null);

  const handleUpload = () => {
    setLoading(true);
    const contentType = files[0].type;
    const fileName = files[0].name;
    const uploadFile = files[0];
    const accessCodeConfig = accessCode ? { access_code: accessCode } : {};

    api
      .post("/files/generate-presigned-url", {
        content_type: contentType,
        file_name: fileName,
        ...accessCodeConfig,
      })
      .then(
        ({ data }) => {
          axios
            .put(data.data.upload_url, uploadFile, {
              headers: {
                "Content-Type": contentType,
              },
            })
            .then(
              () => {
                setSuccessData(data.data);
              },
              (err) => {
                console.error("Error: ", err);
              }
            )
            .finally(() => setLoading(false));
        },
        (err) => {
          console.log(extractAPIErrorString(err));
          setLoading(false);
        }
      );
  };

  if (successData) {
    return (
      <div className="p-5 my-5 bg-light bg-gradient rounded shadow">
        <h3 className="mb-4">Successfully uploaded the file</h3>
        <div className="d-flex mb-2 align-items-center">
          <p className="my-auto">Public key: {successData.public_key}</p>
          <ButtonIcon
            variant="border-filled"
            size="small"
            tooltip="Copy"
            icon={<FontAwesomeIcon icon={faCopy} />}
            className="ms-3"
            onClick={() => {
              navigator.clipboard.writeText(successData.public_key);
            }}
          />
          <HelpText
            variant="question"
            title="Public key"
            className="ms-3"
            text={
              <p>To help protect your file, the file name is not exposed.</p>
            }
          />
        </div>
        <div className="d-flex mb-2 align-items-center">
          <p className="my-auto">Delete code: {successData.delete_code}</p>
          <ButtonIcon
            variant="border-filled"
            size="small"
            tooltip="Copy"
            icon={<FontAwesomeIcon icon={faCopy} />}
            className="ms-3"
            onClick={() => {
              navigator.clipboard.writeText(successData.delete_code);
            }}
          />
          <HelpText
            variant="question"
            title="Delete code"
            className="ms-3"
            text={
              <p>
                If you thimk you made a mistake and you wish to immediately
                destroy the file you can do it using the delete code.
              </p>
            }
          />
        </div>
        {setSuccessData.protected && <p>The file is passsword protected</p>}
      </div>
    );
  }

  return (
    <div className="text-center p-5">
      <h3 className="mb-4">Select the file you wish to share</h3>
      <FileSelector
        className="rainbow-m-vertical_x-large rainbow-p-horizontal_medium rainbow-m_auto"
        style={containerStyles}
        // label="File selector"
        placeholder="Drag & Drop or Click to Browse"
        bottomHelpText="Select only one file"
        variant="multiline"
        onChange={(v) => setFiles(v)}
        value={files.length > 0 ? files : null}
      />
      {files.length > 0 && (
        <Fragment>
          <Input
            label="To limit access to the file enter an (optional) access code"
            placeholder="Access code"
            type="password"
            labelAlignment="left"
            className="react-rainbow rainbow-p-around_medium my-4 col-8 offset-2"
            value={accessCode}
            onChange={(e) => setAccessCode(e.target.value)}
          />
          <Button
            variant="brand"
            className="rainbow-m-around_medium mt-5"
            label="Upload file"
            // disabled={files.length > 0 ? false : true}
            isLoading={isLoading}
            onClick={handleUpload}
          />
        </Fragment>
      )}
    </div>
  );
};

export default FileDrop;

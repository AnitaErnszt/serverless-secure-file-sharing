import axios from "axios";
import _ from "lodash";
import config from "./constants";

export const api = axios.create({
  baseURL: config.baseURL,
  timeout: 30000,
});

const extractAPIError = (cb) => (error) => {
  // console.log(error);
  // console.log(error.response);
  // console.log(error.response.data);
  // Application-code error

  // 401 Error
  if (error.response && error.response.status === 401) {
    return cb("Unauthorized");
  }

  if (error && _.get(error, "response.data.error")) {
    return cb(error.response.data.error);
  }

  const { response, request } = error;

  // 500 Error
  if (response && response.status === 500) {
    return cb("Something went wrong. Please try again");
  }

  // Connectivity Error
  if (
    !response &&
    request &&
    request.status === 0 &&
    request._hasError === true
  ) {
    return cb("Check your internet connection.");
  }

  // None of the above - give axios' error
  return cb(error.message);
};

const extractFirstFieldError = (fields) => {
  const fieldIDs = Object.keys(fields);
  for (let fieldIdx = 0; fieldIdx < fieldIDs.length; fieldIdx++) {
    const field = fields[fieldIDs[fieldIdx]];
    if (field && field.length > 0) {
      return field[0];
    }
  }
  return null;
};

export const extractAPIErrorString = (err) => {
  return extractAPIError((errObj) => {
    if (_.isString(errObj)) {
      return errObj;
    }
    if (errObj.code) {
      switch (errObj.code) {
        case "invalid_input":
          return extractFirstFieldError(errObj.fields) || errObj.message;
        default:
          return errObj.message;
      }
    }
    return errObj.message || "Something went wrong. Please try again";
  })(err);
};

export const extractAPIErrorCode = (err) => {
  if (!err.response || !err.response.data) {
    return null;
  }

  return _.get(err, "response.data.error.code");
};

export default api;

/**
 * ExpressJS server for frontend.
 *
 * This server's purpose is mostly to statically serve the frontend files.
 * However it also handles post requests for an embedded launch and configures
 * the frontend to already include a session token.
 */

import express from "express";
global.fetch = require('node-fetch');
require('abortcontroller-polyfill/dist/polyfill-patch-fetch');

import config from "./config/expressConfig";

import embeddedAuthenticationMiddleware from "./src/express/embeddedAuthenticationMiddleware";

const app = express();

app.use(express.urlencoded({
    extended: true
}));

app.use(express.json());

app.post(
    '/survey/:questionnaireId/lti',
    embeddedAuthenticationMiddleware(config.frontendPath)
);

app.use(express.static("dist"));

app.listen(80, () => console.log("Server is listening on port 80."));
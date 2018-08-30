/**
 * ExpressJS server for frontend.
 *
 * This server's purpose is mostly to statically serve the frontend files.
 * However it also handles post requests for an embedded launch and sets authen-
 * tication cookies.
 */

import express from "express";
import bodyParser from "body-parser";

import embeddedAuthenticationMiddleware from "./src/express/embeddedAuthenticationMiddleware";

const app = express();

app.use(bodyParser.json());

app.use(embeddedAuthenticationMiddleware);

app.use(express.static("dist"));

app.listen(80, () => console.log("Server is listening on port 80."));
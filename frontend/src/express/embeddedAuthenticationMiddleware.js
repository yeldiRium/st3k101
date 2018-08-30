import R from "ramda";

/**
 * @param req Express request.
 * @param res Express response.
 * @param next Callback for next middleware.
 */
const embeddedAuthenticationMiddleware = function (req, res, next) {
  if (req.method === "POST") {
    // No key given, no access granted.
    if (R.not(R.has("key", req.body))) {
      return next();
    }

    const key = req.body.key;


  }
  next();
};

export default embeddedAuthenticationMiddleware;
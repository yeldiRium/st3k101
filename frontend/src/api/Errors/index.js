class ApiError extends Error {
  constructor(s) {
    super(s);
    this.status = -1;
    this.name = "ApiError";
  }
}

/**
 * Client side validation error. Does not correlate with a status code, since it
 * is used before interaction with the Api ensues.
 */
class ValidationError extends ApiError {
  constructor(s, payload) {
    super(s);
    this.name = "ValidationError";
    this.payload = payload;
  }
}

class BadRequestError extends ApiError {
  constructor(s, payload) {
    super(s);
    this.name = "BadRequestError";
    this.status = 400;
    this.payload = payload;
  }
}

class AuthorizationError extends ApiError {
  constructor(s, payload) {
    super(s);
    this.name = "AuthorizationError";
    this.status = 401;
    this.payload = payload;
  }
}

class ForbiddenError extends ApiError {
  constructor(s) {
    super(s);
    this.status = 403;
    this.name = "ForbiddenError";
  }
}

class NotFoundError extends ApiError {
  constructor(s) {
    super(s);
    this.status = 404;
    this.name = "NotFoundError";
  }
}

class ConflictError extends ApiError {
  constructor(s, payload) {
    super(s);
    this.status = 409;
    this.name = "ConflictError";
    this.payload = payload;
  }
}

class InternalServerError extends ApiError {
  constructor(s) {
    super(s);
    this.status = 500;
    this.name = "InternalServerError";
  }
}

/**
 * Default
 */
class UnknownError extends ApiError {
  constructor(s, payload) {
    super(s);
    this.name = "UnknownError";
    this.payload = payload;
  }
}

export {
  NotFoundError,
  AuthorizationError,
  ForbiddenError,
  BadRequestError,
  ConflictError,
  InternalServerError,
  UnknownError,
  ValidationError
};

class ApiError extends Error {
    constructor(s) {
        super(s);
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

/**
 * 400
 */
class BadRequestError extends ApiError {
    constructor(s, payload) {
        super(s);
        this.name = "BadRequestError";
        this.payload = payload;
    }
}

/**
 * 401
 */
class AuthorizationError extends ApiError {
    constructor(s, payload) {
        super(s);
        this.name = "AuthorizationError";
        this.payload = payload;
    }
}

/**
 * 403
 */
class ForbiddenError extends ApiError {
    constructor(s) {
        super(s);
        this.name = "ForbiddenError";
    }
}

/**
 * 404
 */
class NotFoundError extends ApiError {
    constructor(s) {
        super(s);
        this.name = "NotFoundError";
    }
}

/**
 * 409
 */
class ConflictError extends ApiError {
    constructor(s, payload) {
        super(s);
        this.name = "ConflictError";
        this.payload = payload;
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
    UnknownError
};

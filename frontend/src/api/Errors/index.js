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
 * 403
 */
class AuthenticationError extends ApiError {
    constructor(s) {
        super(s);
        this.name = "AuthenticationError";
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
    AuthenticationError,
    BadRequestError,
    ConflictError,
    UnknownError
};

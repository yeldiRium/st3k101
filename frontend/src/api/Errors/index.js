class ApiError extends Error {
    constructor(s) {
        super(s);
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
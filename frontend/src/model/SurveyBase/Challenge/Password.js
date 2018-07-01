import Challenge from "./Challenge";

class Password extends Challenge {
    /**
     * @param {Boolean} isEnabled See Challenge.
     * @param {String} password
     */
    constructor(isEnabled, password) {
        super(isEnabled);

        this.password = password;
    }

    get name() {
        return "Password";
    }

    /**
     * Returns a new Password Challenge with the new password.
     *
     * @param {String} password
     * @returns {Password}
     */
    setPassword(password) {
        return new Password(this.isEnabled, password);
    }

    /**
     * @param {String} data A password.
     * @return {Boolean} true, if the password is the same as the contained one.
     */
    innerValidate(data) {
        return data === this.password;
    }

    /**
     * Clones the object.
     *
     * @returns {Password}
     */
    clone() {
        return new Password(
            this.isEnabled,
            this.password
        );
    }
}

export default Password;

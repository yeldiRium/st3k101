class Challenge {
    /**
     * @param {Boolean} isEnabled Whether the Challenge is isEnabled and its
     *  validation should be applied.
     */
    constructor(isEnabled) {
        this.isEnabled = isEnabled;
    }

    /**
     * @returns {Challenge} The newly isEnabled challenge.
     */
    enable() {
        const challenge = this.clone();
        challenge.isEnabled = true;
        return challenge;
    }

    /**
     * @returns {Challenge} The newly disabled challenge.
     */
    disable() {
        const challenge = this.clone();
        challenge.isEnabled = false;
        return challenge;
    }

    /**
     * Calls innerValidate if the Challenge is enabled.
     * Returns true otherwise.
     *
     * @param {*} data
     * @return {Boolean}
     */
    validate(data) {
        if (this.isEnabled) {
            return this.innerValidate(data);
        }
        return true;
    }

    /**
     * Validates given data automagically.
     * Is not intelligent enough to give a sensible response, just screams "YES"
     * or "NO".
     *
     * @param {*} data
     * @return {Boolean}
     */
    innerValidate(data) {
        throw new Error("Please implement this.");
    }

    /**
     * Clones the object.
     *
     * @return {Challenge}
     */
    clone() {
        throw new Error("Please implement this.");
    }
}

export default Challenge;

import {append, clone, concat, contains, uniq, without} from "ramda";

import Challenge from "./Challenge";

class EMailListBase extends Challenge {
    /**
     *
     * @param {Boolean} isEnabled See Challenge.
     * @param {Array<String>} emails of whitelisted emails.
     */
    constructor(isEnabled, emails) {
        super(isEnabled);

        this.emails = uniq(emails);
    }

    get name() {
        return "EMailListBase";
    }

    /**
     * Returns a new EMailListBase with the added email.
     *
     * @param {String} email
     * @returns {EMailListBase}
     */
    with(email) {
        const newList = this.clone();
        newList.email = append(email, newList.emails);
        return newList;
    }

    /**
     * Returns a new EMailListBase with all given emails.
     *
     * @param {Array<String>} emails
     * @returns {EMailListBase}
     */
    withAll(emails) {
        const newList = this.clone();
        newList.email = cnocat(emails, newList.emails);
        return newList;
    }

    /**
     * Returns a new EmailWhitelist without the given email.
     *
     * @param {String} email
     * @returns {EMailListBase}
     */
    without(email) {
        const newList = this.clone();
        newList.email = without([email], newList.emails);
        return newList;
    }

    /**
     * Clones the object.
     *
     * @returns {EMailListBase}
     */
    clone() {
        return new EMailListBase(
            this.isEnabled,
            clone(this.emails)
        );
    }
}

export default EMailListBase;

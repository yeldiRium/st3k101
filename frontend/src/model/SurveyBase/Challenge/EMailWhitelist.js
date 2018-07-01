import {append, clone, concat, contains, uniq, without} from "ramda";

import Challenge from "./Challenge";

class EMailWhitelist extends Challenge {
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
        return "EMailWhitelist Challenge";
    }

    /**
     * Returns a new EMailWhitelist with the added email.
     *
     * @param {String} email
     * @returns {EMailWhitelist}
     */
    with(email) {
        return new EMailWhitelist(
            this.isEnabled,
            append(email, this.emails)
        );
    }

    /**
     * Returns a new EMailWhitelist with all given emails.
     *
     * @param {Array<String>} emails
     * @returns {EMailWhitelist}
     */
    withAll(emails) {
        return new EMailWhitelist(
            this.isEnabled,
            concat(emails, this.emails)
        );
    }

    /**
     * Returns a new EmailWhitelist without the given email.
     *
     * @param {String} email
     * @returns {EMailWhitelist}
     */
    without(email) {
        return new EMailWhitelist(
            this.isEnabled,
            without([email], this.emails)
        );
    }

    /**
     * @param {String} data Hopefully an E-Mail.
     * @return {Boolean} true, if the email is contained in the whitelist.
     */
    innerValidate(data) {
        return contains(data, this.emails);
    }

    /**
     * Clones the object.
     *
     * @returns {EMailWhitelist}
     */
    clone() {
        return new EMailWhitelist(
            this.isEnabled,
            clone(this.emails)
        );
    }
}

export default EMailWhitelist;

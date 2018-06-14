import Party from "./Party";

class DataClient extends Party {
    /**
     *
     * @param {String} href See Resource.
     * @param {String} email
     * @param {Language} language
     */
    constructor(href,
                email,
                language) {
        super(href);
        this._email = email;
        this._language = language;
    }

    // TODO: refactor email out into own model and/or validate

    /**
     * @param {String} email
     */
    set email(email) {
        this._email = email;
    }

    /**
     * @returns {String}
     */
    get email() {
        return this._email;
    }

    // TODO: refactor language out into own model and/or validate

    /**
     * @param {Language} language
     */
    set language(language) {
        this._language = language;
    }

    /**
     * @returns {Language}
     */
    get language() {
        return this._language;
    }
}

export default DataClient;

export {
    DataClient
};
import Party from "./Party";

class DataClient extends Party {
    constructor(href,
                email,
                language) {
        super(href);
        this._email = email;
        this._language = language;
    }

    // TODO: refactor email out into own model and/or validate

    /**
     * @param {string} email
     */
    set email(email) {
        this._email = email;
    }

    /**
     * @returns {string}
     */
    get email() {
        return this._email;
    }

    // TODO: refactor language out into own model and/or validate

    /**
     * @param {string} language
     */
    set language(language) {
        this._language = language;
    }

    /**
     * @returns {string}
     */
    get language() {
        return this._language;
    }
}

export default DataClient;

export {
    DataClient
};
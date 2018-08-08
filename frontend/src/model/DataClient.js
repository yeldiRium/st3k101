import Party from "./Party";

class DataClient extends Party {
    /**
     *
     * @param {String} href See Resource.
     * @param {String} id See Resource.
     * @param {String} email
     * @param {Language} language
     * @param {Array<Roles>} roles
     */
    constructor(href,
                id,
                email,
                language,
                roles
    ) {
        super(href, id);
        this._email = email;
        this._language = language;
        this._roles = roles;
    }

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

    /**
     *
     * @returns {Array<Roles>}
     */
    get roles() {
        return this._roles;
    }

    /**
     * @param {Array<Roles>} roles
     */
    set roles(roles) {
        this._roles = roles;
    }

    /**
     * @returns {DataClient}
     */
    clone() {
        return new DataClient(
            this._href,
            this._id,
            this._email,
            this._language,
            this._roles
        );
    }
}

export default DataClient;

export {
    DataClient
};

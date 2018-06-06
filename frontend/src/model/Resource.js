/**
 * An object that has a representation in the API and can be constructed by
 * fetching the given href.
 */
class Resource {
    /**
     *
     * @param {string} href
     */
    constructor(href) {
        this._href = href;
    }

    /**
     *
     * @param {string} href
     */
    set href(href) {
        this._href = href;
    }

    /**
     *
     * @returns {string}
     */
    get href() {
        return this._href;
    }
}

export default Resource;
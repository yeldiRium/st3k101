/**
 * An object that has a representation in the API and can be constructed by
 * fetching the given href.
 */
class Resource {
    /**
     *
     * @param {String} href
     */
    constructor(href) {
        this._href = href;
    }

    /**
     *
     * @param {String} href
     */
    set href(href) {
        this._href = href;
    }

    /**
     *
     * @returns {String}
     */
    get href() {
        return this._href;
    }
}

export default Resource;
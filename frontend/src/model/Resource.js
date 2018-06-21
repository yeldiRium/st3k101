/**
 * An object that has a representation in the API and can be constructed by
 * fetching the given href.
 */
class Resource {
    /**
     *
     * @param {string} href
     */
    constructor(href, id) {
        this._href = href;
        this._id = id;
    }

    /**
     *
     * @returns {string}
     */
    get href() {
        return this._href;
    }

    /**
     *
     * @returns {String}
     */
    get id() {
        return this._id;
    }

    /**
     * @param {Resource} otherResource
     * @return {boolean} If the Resources are equal.
     */
    identifiesWith(otherResource) {
        return this.href === otherResource.href;
    }
}

/**
 * @param {Resource} aResource
 * @param {Resource} bResource
 * @returns {boolean} True, if a identifies with b.
 */
function identifiesWith(aResource, bResource) {
    return aResource.identifiesWith(bResource);
}

export default Resource;

export {
    Resource,
    identifiesWith
};

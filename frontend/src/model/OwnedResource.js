import Resource from "./Resource";
import Party from "./Party";

/**
 * A Resource that can be owned by someone.
 */
class OwnedResource extends Resource {
    /**
     *
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Party} owner
     */
    constructor(href,
                id,
                owner) {
        super(href, id);
        this._owner = owner;
    }

    /**
     * @returns {Party}
     */
    get owner() {
        return this._owner;
    }

    /**
     * @param {Party} party
     * @return {boolean} True, if the OwnedResource is owned by the given Party.
     */
    isOwnedBy(party) {
        return party.identifiesWith(this._owner);
    }
}

/**
 *
 * @param {OwnedResource} resource
 * @param {Party} party
 * @return {boolean} True, if the resource is owned by the party.
 */
function isResourceOwnedBy(resource, party) {
    return resource.isOwnedBy(party);
}

export default OwnedResource;

export {
    OwnedResource,
    isResourceOwnedBy
};
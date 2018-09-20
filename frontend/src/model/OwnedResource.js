import Resource from "./Resource";
import Party from "./Party";
import { any } from "ramda";

/**
 * A Resource that can be owned by someone.
 */
class OwnedResource extends Resource {
  /**
   *
   * @param {string} href See Resource.
   * @param {String} id See Resource.
   * @param {Array<Party>} owners
   */
  constructor(href, id, owners) {
    super(href, id);
    this._owners = owners;
  }

  /**
   * @returns {Array<Party>}
   */
  get owners() {
    return this._owners;
  }

  /**
   * @param {Party} party
   * @return {boolean} True, if the OwnedResource is owned by the given Party.
   */
  isOwnedBy(party) {
    return any(owner => party.identifiesWith(owner), this.owners);
  }

  /**
   * @returns {OwnedResource}
   */
  clone() {
    return new OwnedResource(this._href, this._id, [...this._owners]);
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

export { OwnedResource, isResourceOwnedBy };

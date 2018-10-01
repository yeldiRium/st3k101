import { append, clone, concat, contains, uniq, without } from "ramda";

import EMailListBase from "./EMailListBase";

class EMailBlacklist extends EMailListBase {
  get name() {
    return "EMailBlacklist";
  }

  /**
   * @param {String} data Hopefully an E-Mail.
   * @return {Boolean} true, if the email is contained in the whitelist.
   */
  innerValidate(data) {
    return !contains(data, this.emails);
  }

  /**
   * Clones the object.
   *
   * @returns {EMailBlacklist}
   */
  clone() {
    return new EMailBlacklist(this.isEnabled, clone(this.emails));
  }
}

export default EMailBlacklist;

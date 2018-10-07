import { clone, contains } from "ramda";

import EMailListBase from "./EMailListBase";

class EMailWhitelist extends EMailListBase {
  get name() {
    return "EMailWhitelist";
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
    return new EMailWhitelist(this.isEnabled, clone(this.emails));
  }
}

export default EMailWhitelist;

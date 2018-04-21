import Future from "fluture";

import ResultHandling from "../Utility/ResultHandling";
import PathHandling from "../Utility/PathHandling";

export default {
    /**
     * @returns a Future.
     * @resolves with a locale list of the form [[short, long], [short, long]..]
     * sorted by the long form ascending.
     * @reject with either a TypeError, if a connection problem occured, or with
     * the server's response detailling the error, if the status code is not
     * 200.
     * @cancel aborts the HTTP request.
     */
    "all": function () {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(PathHandling.buildApiPathTo("/api/locales"), {
                "mode": "cors"
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    }
}

import Future from "fluture";

import ResultHandling from "../Utility/ResultHandling";
import PathHandling from "../Utility/PathHandling";

export default {
    /**
     * @returns a Future.
     * @resolves with a list of all available QACs.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
    "list": function () {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(PathHandling.buildApiPath("/api/qac_module"), {
                "method": "GET",
                "mode": "cors",
                signal
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

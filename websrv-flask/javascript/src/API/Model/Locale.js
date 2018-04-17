import Future from "fluture";

import ResultHandling from "../Utility/ResultHandling";

export default {
    "all": function () {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch("/api/locales", {
                "mode": "cors"
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    }
}

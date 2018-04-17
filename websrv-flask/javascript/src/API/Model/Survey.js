import Future from "fluture";

import ResultHandling from "../Utility/ResultHandling";
import PathHandling from "../Utility/PathHandling";

export default {
    "all": function (locale = "") {
        let path = PathHandling.pathMaybeWithLocale(
            "/api/survey", locale
        );

        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(
                path,
                {
                    "method": "GET",
                    "mode": "cors",
                    "credentials": "include",
                    signal
                }
            )
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJsonPlusLocale)
            .chainRej(ResultHandling.extractJson);
    },
    "create": function (name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(
                "/api/survey",
                {
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "mode": "cors",
                    "credentials": "include",
                    "body": JSON.stringify({
                        "name": name
                    }),
                    signal
                }
            )
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    "update": function (uuid, name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(
                `/api/survey/${uuid}`,
                {
                    "method": "PUT",
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "mode": "cors",
                    "credentials": "include",
                    "body": JSON.stringify({
                        "name": name
                    }),
                    signal
                }
            )
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    "delete": function (uuid) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;
            fetch(
                `/api/survey/${uuid}`,
                {
                    "method": "DELETE",
                    "mode": "cors",
                    "credentials": "include",
                    signal
                }
            )
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    }
}

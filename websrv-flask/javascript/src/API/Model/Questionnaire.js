import Future from "fluture";
import ResultHandling from "../Utility/ResultHandling";
import PathHandling from "../Utility/PathHandling";

export default {
    "create": function ({survey_uuid, name, description, template = null}) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch("/api/questionnaire", {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "survey_uuid": survey_uuid,
                    "questionnaire": {
                        "name": name,
                        "description": description,
                        "template": template
                    }
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "get": function (questionnaire_uuid, locale = "") {
        const path = PathHandling.pathMaybeWithLocale(
            `/api/questionnaire/${questionnaire_uuid}`, locale
        );
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(path, {
                "method": "GET",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .map(data => {
                console.log(data);
                return data;
            })
            .chain(ResultHandling.checkStatus(200))
            .map(data => {
                console.log(data);
                return data;
            });
    },
    "update": function (questionnaire_uuid, {name = null, description = null}) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}`, {
                "method": "PUT",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "name": name,
                    "description": description
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "publish": function (questionnaire_uuid) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}/publish`, {
                "method": "PATCH",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "unpublish": function (questionnaire_uuid) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}/unpublish`, {
                "method": "PATCH",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "delete": function (questionnaire_uuid, survey_uuid) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}`, {
                "method": "DELETE",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify({
                    "survey_uuid": survey_uuid
                }),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "listTemplates": function () {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch("/api/questionnaire/templates", {
                "method": "GET",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "listQACs": function (questionnaire_uuid) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}/qac`, {
                "method": "GET",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "getQACConfig": function (questionnaire_uuid, qac_name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`, {
                "method": "GET",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "enableQAC": function (questionnaire_uuid, qac_name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`, {
                "method": "POST",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "configureQAC": function (questionnaire_uuid, qac_name, data) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`, {
                "method": "PUT",
                "headers": {
                    "Content-Type": "application/json"
                },
                "mode": "cors",
                "credentials": "include",
                "body": JSON.stringify(data),
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
    "disableQAC": function (questionnaire_uuid, qac_name) {
        return Future((reject, resolve) => {
            const controller = new AbortController();
            const signal = controller.signal;

            fetch(`/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`, {
                "method": "DELETE",
                "mode": "cors",
                "credentials": "include",
                signal
            })
                .then(resolve)
                .catch(reject);

            return controller.abort;
        })
            .chain(ResultHandling.checkStatus(200));
    },
}

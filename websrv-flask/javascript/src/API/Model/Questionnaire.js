import Future from "fluture";
import ResultHandling from "../Utility/ResultHandling";
import PathHandling from "../Utility/PathHandling";

export default {
    /**
     * Creates a new Questionnaire with the given name and description on the
     * given Survey.
     *
     * If a template is given, name and description are ignored and the template
     * is used instead.
     *
     * @param survey_uuid
     * @param name
     * @param description
     * @param template
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Reads the complete structure of the given Questionnaire, optionally using
     * the given locale.
     *
     * @param questionnaire_uuid
     * @param locale
     * @returns a Future.
     * @resolves with the Questionnaire's content.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJsonPlusLocale)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Updates the given Questionnaire. Overwrites name or description, whatever
     * is given.
     *
     * @param questionnaire_uuid
     * @param name
     * @param description
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Marks the Questionnaire as published and makes it accessible for
     * subjects.
     *
     * @param questionnaire_uuid
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Marks the Questionnaire as published and makes it inaccessible.
     *
     * @param questionnaire_uuid
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Deletes the Questionnaire with uuid = questionnaire_uuid on the given
     * Survey.
     *
     * @param questionnaire_uuid
     * @param survey_uuid
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Lists the templates that are available to the current user.
     *
     * @returns a Future.
     * @resolves with a list of templates.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Lists the enabled QACs on the given Questionnaire.
     *
     * @param questionnaire_uuid
     * @returns a Future.
     * @resolves with the list of QACs on the given Questionnaire.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * @param questionnaire_uuid
     * @param qac_name
     * @returns a Future.
     * @resolves with the configuration for the QAC on the give Questionnaire.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Enables the qac_name on the given Questionnaire.
     *
     * @param questionnaire_uuid
     * @param qac_name
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Configures the QAC with qac_name on the given Questionnaire.
     *
     * The data object is dependent on the QAC in question and varies.
     *
     * @param questionnaire_uuid
     * @param qac_name
     * @param data
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
    /**
     * Disables qac_name on the given Questionnaire.
     *
     * @param questionnaire_uuid
     * @param qac_name
     * @returns a Future.
     * @resolves with the server's confirmation response.
     * @rejects with either a TypeError, if a connection problem occured, or
     * with the server's response detailling the error, if the status code is
     * not 200.
     * @cancel aborts the HTTP request.
     */
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
            .chain(ResultHandling.checkStatus(200))
            .chain(ResultHandling.extractJson)
            .chainRej(ResultHandling.extractJson);
    },
}

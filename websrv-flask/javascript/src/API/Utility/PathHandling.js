export default {
    "pathMaybeWithLocale": function (path, locale = "") {
        return path + (
            (locale === "")
                ? ""
                : "?locale_cookie=0&locale=" + locale
        );
    },
    "openQuestionnaire": function (questionnaire_uuid) {
        const win = window.open(
            `/survey/${questionnaire_uuid}`, "_blank"
        );
        if (win) {
            win.focus();
            return true;
        }
        return false;
    }
}

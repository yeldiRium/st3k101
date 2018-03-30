const $ = require("jquery");

$(document).ready(function () {
    $(".language_menu li").each(function (index, element) {
        $(element).on("click", function() {
            const languageShort = $(this).children("a").data("target-language");
            window.location.href = window.location.pathname + "?" +
                $.param({'locale': languageShort});
        })
    })
});
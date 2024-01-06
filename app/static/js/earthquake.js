!function () {
    "use strict";

    window.onload = function () {
        var button = document.getElementById("submit");
        button.onclick = function () {
            var dayCountInput = document.getElementById("day-count");
            var dayCount = dayCountInput.value;
            window.location.href = "/earthquake?last_day=" + dayCount;
        };
    };
}();
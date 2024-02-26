$(document).ready(function() {
    function updateClock() {
        var now = new Date();
        var hours = now.getHours();
        var minutes = now.getMinutes();
        var seconds = now.getSeconds();

        hours = (hours < 10) ? "0" + hours : hours;
        minutes = (minutes < 10) ? "0" + minutes : minutes;
        seconds = (seconds < 10) ? "0" + seconds : seconds;

        var currentTime = hours + ":" + minutes + ":" + seconds;

        var daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        var dayOfWeek = daysOfWeek[now.getDay()];
        var dayOfMonth = now.getDate();
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        var month = months[now.getMonth()];
        var year = now.getFullYear();

        var currentDate = dayOfWeek + ', ' + dayOfMonth + ' ' + month + ' ' + year;

        $("#clock").text(currentTime);
        $("#date").text(currentDate);
    }

    setInterval(updateClock, 1000);
    updateClock();
});
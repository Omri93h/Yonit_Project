$(document).ready(function() {
    $("#nav-meals").click(function(){
        $("#nav-meals-options").slideToggle();
    });
	
		nextMeal = 1590044480000;
		var x = setInterval(function() {
			var now = new Date().getTime();
			var distance = nextMeal - now;
			var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
			var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
			var seconds = Math.floor((distance % (1000 * 60)) / 1000);
			document.getElementById("timer").innerHTML = hours + "h " + minutes + "m " + seconds + "s ";
			if (distance < 0) {
				nextMeal+=86400000; // 24 hours im milli ---- to set always 9:30 (just for example)
			}
		}, 1000);
		return false;
	
});



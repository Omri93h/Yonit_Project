$(document).ready(function() {
    $("#nav-meals").click(function(){
        $("#nav-meals-options").slideToggle();
    });
	
	// if (window.location.pathname=='/index.html')      <<<<<<< DOES NOT WORK ON SERVER? BUT DO WORK ON LOCAL
	 {
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
				// to add next version :     document.getElementById("timer").innerHTML = "Meal has already should be given !";
			}
		}, 1000);
		return false;
	};
	return false;
});



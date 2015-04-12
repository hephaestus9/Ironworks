$(document).ready(function() {
	
	/* EDIT BELOW */
	var launchDate = new Date("December 31, 2013 24:00:00");
	var procentageDone = 50;
	var headerColor = 'yellow';
	var progressFillColor = 'green';
	
	/* DON'T EDIT BELOW */
	var secondsRemaining = Math.floor(launchDate.getTime() / 1000) - Math.floor(new Date().getTime() / 1000);
	countdown(secondsRemaining);
	updateProgress(procentageDone);
	setHeaderColor(headerColor);
	setProgressFillColor(progressFillColor);

});
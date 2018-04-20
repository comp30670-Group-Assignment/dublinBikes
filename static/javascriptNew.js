
// Hold marker data.
var markerArray = [];
var map;

function mapInit() {
	var mapCenter = {lat: 53.3498, lng: -6.2603};
    map = new google.maps.Map(document.getElementById('googleMap'), {
    zoom: 14, 
    center: mapCenter});
    
    // Count number of markers initiated.
    var markerCounter = 0;
    // Hold modal data.
    var modalArray = [];
  		
  	$.getJSON($SCRIPT_ROOT + '/_map_data', function(data) {
      				
      	// Create empty array 'index'
		var index = [];
		// Add (i.e. 'push') the next xID item to the array
      	for(var xID in data) {
      		index.push(xID);		
      	}
      			
      	// Fill map up with markers based on json data
        // Right now all markers are being generated, but they are being given all the same
        // content, when they should be given content depending on their own personal info.
		for(i = 0; i < index.length; i++) {
    		var mytext = index[i] + "<br> Station No.: " + "<br> Free bikes: ";
    		var myinfowindow = new google.maps.InfoWindow({content: mytext});
    		
    		// Push to array to store data returned by $.getJSON.
    		modalArray.push(data[index[i]]);
    		
    		var iconBase = '/static/';
			// Red
			if (data[index[i]].available_bikes < 5){
				var iconVal = iconBase + 'red.png';
    		// Green
    		} else if (data[index[i]].available_bikes > 30){
				var iconVal = iconBase + 'green.png';
    		//Amber
    		} else {
    			var iconVal = iconBase + 'amber.png';
    		}
             
			var position = new google.maps.LatLng(data[index[i]].latitude, data[index[i]].longitude);
        	var contentString = '<div class="infoWindowOpen">' +
        						'<h4 id="info-head">' + index[i] + '</h4>' +
        						'<p class="info-text">Available Bikes: ' + data[index[i]].available_bikes + '</p>' +
        						'<p class="info-text">Available Bike Stands: ' + data[index[i]].available_stands + '</p>' +
        						'<button type="button" class="btn map-button" id="mapBtn">Open Data</button>' +
        						'</div>';
        			
        	var myinfowindow = new google.maps.InfoWindow({content: contentString});
        			
    		var marker = new google.maps.Marker({
    			position: position, 
    			map: map,
    			infowindow: myinfowindow,
    			markerID: markerCounter,
    			icon: iconVal
    		});
    		
    		markerArray.push(marker);
    		
    		open = [];
    				
    		google.maps.event.addListener(marker, 'click', function() {
    		
    			var x = this.markerID;
        		
        		if (open.length != 0) {
        			for(var i = 0; i < open.length;i++) {
        				markerArray[open[i]]['infowindow'].close();
        			}
        		}
        		markerArray[x]['infowindow'].open(map, this);
        		
        		open.push(x)
        		
        		// Map modal.
				$(document).ready(function(){
    				$("#mapBtn").click(function(){
    					
    					file_num = x + 1;
    						
						// Load google charts
						google.charts.load('current', {'packages':['corechart']});
						google.charts.setOnLoadCallback(drawVisualisation);

						// Draw the chart and set the chart values
						function drawVisualisation() {
						
							$.getJSON($SCRIPT_ROOT + '/_predictions/' + file_num, function(data) {
			
								var stationID = x + 1;

								var dataParsed = JSON.parse(data[0]);
								
								var data = google.visualization.arrayToDataTable([
								['Hour', 'Predictor'],
								['00:00',  parseInt(dataParsed[stationID.toString()][0])],
								['01:00',  parseInt(dataParsed[stationID.toString()][1])],
								['02:00',  parseInt(dataParsed[stationID.toString()][2])],
								['03:00',  parseInt(dataParsed[stationID.toString()][3])],
								['04:00',  parseInt(dataParsed[stationID.toString()][4])],
								['05:00',  parseInt(dataParsed[stationID.toString()][5])],
								['06:00',  parseInt(dataParsed[stationID.toString()][6])],
								['07:00',  parseInt(dataParsed[stationID.toString()][7])],
								['08:00',  parseInt(dataParsed[stationID.toString()][8])],
								['09:00',  parseInt(dataParsed[stationID.toString()][9])],
								['10:00',  parseInt(dataParsed[stationID.toString()][10])],
								['11:00',  parseInt(dataParsed[stationID.toString()][11])],
								['12:00',  parseInt(dataParsed[stationID.toString()][12])],
								['13:00',  parseInt(dataParsed[stationID.toString()][13])],
								['14:00',  parseInt(dataParsed[stationID.toString()][14])],
								['15:00',  parseInt(dataParsed[stationID.toString()][15])],
								['16:00',  parseInt(dataParsed[stationID.toString()][16])],
								['18:00',  parseInt(dataParsed[stationID.toString()][17])],
								['19:00',  parseInt(dataParsed[stationID.toString()][18])],
								['20:00',  parseInt(dataParsed[stationID.toString()][19])],
								['21:00',  parseInt(dataParsed[stationID.toString()][20])],
								['22:00',  parseInt(dataParsed[stationID.toString()][21])],
								['23:00',  parseInt(dataParsed[stationID.toString()][22])],
								['24:00',  parseInt(dataParsed[stationID.toString()][23])]
								]);
						
								var options = {
								titleTextStyle: {bold: true},
								title : 'Station Occupancy Prediction',
								vAxis: {title: 'Bikes'},
								hAxis: {title: '24 Hours'},
								'width':650,
								'height':400,
								series: {2: {type: 'line'}}
								};
			
								var chart = new google.visualization.ComboChart(document.getElementById('modal-graph-1'));
								chart.draw(data, options);
							
							
							});
							
						}
						
						google.charts.setOnLoadCallback(drawVisualisation2);

						// Draw the chart and set the chart values
						function drawVisualisation2() {
						
							$.getJSON($SCRIPT_ROOT + '/_trends', function(data) {
			
								var stationID = x + 1;

													
								console.log(data[x])
								
								var data = google.visualization.arrayToDataTable([
								['Hour', 'Predictor'],
								['Monday',  parseInt(data[stationID.toString()][0])],
								['Tuesday',  parseInt(data[stationID.toString()][1])],
								['Wednesday',  parseInt(data[stationID.toString()][2])],
								['Thursday',  parseInt(data[stationID.toString()][3])],
								['Friday',  parseInt(data[stationID.toString()][4])],
								['Saturday',  parseInt(data[stationID.toString()][5])],
								['Sunday',  parseInt(data[stationID.toString()][23])]
								]);
						
								var options = {
								titleTextStyle: {bold: true},
								title : 'Daily Availability',
								vAxis: {title: 'Bikes'},
								hAxis: {title: 'Days of Week'},
								'width':650,
								'height':400,
								series: {2: {type: 'line'}}
								};
			
								var chart = new google.visualization.ComboChart(document.getElementById('modal-graph-2'));
								chart.draw(data, options);
							
							
							});
							
						}
    					
    					
        				$("#mapModal").modal();
        				$("#modal-map-head").html("<h2 id='modal-title' style='text-align:center;font-weight:bold'>"+index[x]+"</h2>");
    				});
				});
        		
			});
			
			markerCounter++;
    				
		}
				
	});

}
      	
window.setInterval(function(){
  	mapInit()
}, 300000);

// Trigger Google Maps marker infowindow.
function markerFlag(markerNum) {
	google.maps.event.trigger(markerArray[markerNum], 'click');
}

// Get station marker names and populate dropdown menu.
$.getJSON($SCRIPT_ROOT + '/_drop_data', function(data) {

	// Append marker locations to dropdown menu.
	for (var i = 0; i < data.length; i++) {
		$("#marker-loc").append("<a href='#' onclick='markerFlag("+i+")'>"+data[i]+"</a>");
	}

});
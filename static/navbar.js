$.getJSON($SCRIPT_ROOT + '/_weather', function(data){
    
    $(document).ready(function(){
        $("#rightie-top").text(Math.round(data["0"]["temp"])+ '°C')
        $("#rightie-bottom").text(data["0"]["description"])
        var image = data["0"]["icon"]
        $("#image").attr("src","http://openweathermap.org/img/w/" + image + ".png");
        
        
    });
    
});
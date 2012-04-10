/* 
Timeperiod.js

This file deals with the timeperiod view for the schedule app.
*/ 

$(document).observe("dom:loaded",function(){
    //$(".timeperiod_slug").observe("click",getTimePeriodData());
    $(".timeperiod_slug").observe("click",changecolor());
});

function getTimePeriodData(){
    slug = this.title
    $.ajax({
        "url"       : URL_BASE + "schedule/timeperiod/",
        "data"      : {"location": slug},
        "error"     : {},
        "success"   : loadTimePeriodData(data); 
    });

}

function loadTimePeriodData(data){
    var timeperiod_box = $(".timeperiod");
}

function changecolor(){
    $(".timeperiod_slug").append("<p>meow</p>");
}

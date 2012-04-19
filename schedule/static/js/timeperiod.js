/* 
Timeperiod.js

This file deals with the timeperiod view for the schedule app.
*/ 


/*
Loads the page with events.
*/
$(document).ready(function() {
    $(".timeperiod_selector").click(function() {
        getTimePeriodData(this.title);
    });
});

/*
Performs an Ajax call to grab the data. 
*/
function getTimePeriodData(slug){
    $.ajax({
        "url"       : "/schedule/timeperiods/info/",
        "data"      : {"name": slug},
        "error"     : function(){ $("#timeperiod_info").append("Error, no data associated with this timeperiod")},
        "success"   : function(data) { loadTimePeriodData(data);} 
    });
}

/*
Inserts the data into the page dynamically. 
*/
function loadTimePeriodData(data){
    var timeperiod_box = $(".timeperiod");
    data = JSON.parse(data);

    var timeperiod_info  = $("#timeperiod_info");
    timeperiod_info.removeClass("hidden").addClass("visible");

    var title = $("#timeperiod_title");
    title.empty()
    title.append(data['timeperiod']);

    var date = $("#timeperiod_date");
    date.empty()
    date.append(data['start_date'] + " - " + data['end_date']);
    
    var total = $("#timeperiod_total");
    total.empty()
    total.append(data['count'] + " can work this timeperiod.");

    people_label = $("#people_label");
    if (data['people'].length != 0){
        people_label.removeClass("hidden").addClass("visible");
        people_list = $("#timeperiod_people_list");
        people_list.empty();

        for (var i = 0; i < data['people'].length; i++){
            people_list.append("<li>" + data['people'][i] + "</li>");
        }

    }else{
        people_label.removeClass("visible").addClass("hidden");
    }
}


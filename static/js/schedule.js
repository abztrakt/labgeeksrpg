/*
Schedule.js

This file deals with the schedule itself. Allows users to interact with the schedule
*/

/* 
Loads the page with events.
*/

$(document).ready(function(){
    // Javascript associated with tabs.
    $(".tab_content").hide();
    $("ul.tabs li:first").addClass("active").show(); //Activate first tab
    $(".tab_content:first").show(); //Show first tab content

    //On Click Event
    $("ul.tabs li").click(function() {

        $("ul.tabs li").removeClass("active"); //Remove any "active" class
        $(this).addClass("active"); //Add "active" class to selected tab
        $(".tab_content").hide(); //Hide all tab content

        var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content
        $(activeTab).show(); 
        return false;
    });

    // Use a timepicker widget to select the times in an input field.
    $('.time_input').timepicker({
            showPeriod: true,
            amPmText: ['am', 'pm'],
            minutes: {
                starts: 0,
                ends: 30,
                interval: 30
            }
        });

    getPeopleList();

    // Bind the modifyClosingHours method to the buttons.
    $(".add_closing_hours").bind("click",true,modifyClosingHours);
    $(".remove_closing_hours").bind("click",false,modifyClosingHours);

    // Bind the modifySavingHours method to the buttons.
    $(".add_employee_hours").bind("click",true,modifyEmployeeHours);
    $(".remove_employee_hours").bind("click",false,modifyEmployeeHours);

    // Bind the save method to the save button.
    $("#save_hours").bind("click",saveClosingHours);

    // Handle the selecting of columns.
    $("table").selectable({
        filter: '.content',
        stop: function() {
            /*
            $(".ui-selected", this).each(function(){
                $(this).empty();
                var time = $(this).parent().children()[0].innerHTML;
                $(this).append(time);
            });
            */
            var selected = $(".ui-selected", this);
            var middleChild = $(selected.get(selected.size()/2));
            middleChild.tooltip({
                tip: '#tooltip',
                position: 'center right',
                offset: [0,15],
            });
            
        }
    }); 

});


function modifyEmployeeHours(event){
    var startTime = $(this).parent().children(".employee_starting_hours")[0].value;
    var endTime = $(this).parent().children(".employee_ending_hours")[0].value;
    var user = $(this).parent().children(".add_person")[0].value;

    var startTimeSplit = timeDict(startTime);
    var endTimeSplit = timeDict(endTime);

    var schedule = $(this).parent().parent().parent().parent().children(".schedule_grid")[0];
    var isAdding = event.data;

    var startIndex = 0;
    var endIndex = 0;
    
    for (var i = 0; i < schedule.children.length; i++) { 
        var schedule_row = schedule.children[i];
        var schedule_row_time = schedule_row.children[0].innerHTML;

        if (schedule_row_time == startTime){
            startIndex = i;
        }
        
        if (schedule_row_time == endTime){
            endIndex = i;
        }
    }
    
    var index = null;
    var schedule_row = schedule.children[startIndex];
    for (var i = 1; i < schedule_row.children.length; i ++){
        var element = $(schedule_row.children[i]);
        if (element.is(":empty") || element.text() == user){
            index = i;
            break; 
        }
    }

    if (index != null){
        for (var i = startIndex; i <= endIndex; i++){
            var schedule_row = $(schedule.children[i]);
            var element = $(schedule_row.children()[index]);
            
            if (isAdding){
                element.html(user);
            } else{
                element.empty()
            }
        }
    }
}

function modifyClosingHours(event){

    var startTime = $(this).parent().children(".closing_starting_hours")[0].value;
    var endTime = $(this).parent().children(".closing_ending_hours")[0].value;

    var startTimeSplit = timeDict(startTime);
    var endTimeSplit = timeDict(endTime);

    var schedule = $(this).parent().parent().parent().parent().children(".schedule_grid")[0];
    var isAdding = event.data;

    var startIndex = 0;
    var endIndex = 0;

    for (var i = 0; i < schedule.children.length; i++) { 
        var schedule_row = schedule.children[i];
        var schedule_row_time = schedule_row.children[0].innerHTML;

        if (schedule_row_time == startTime){
            startIndex = i;
        }
        
        if (schedule_row_time == endTime){
            endIndex = i;
        }
    }

    for (var i = startIndex; i <= endIndex; i++){
        var schedule_row = schedule.children[i];
        for (var j = 1; j < schedule_row.children.length; j ++){
                if (isAdding){
                    $(schedule_row.children[j]).addClass("closed_hours");
                    $(schedule_row.children[j]).html("closed");
                }else{
                    $(schedule_row.children[j]).removeClass("closed_hours");
                    $(schedule_row.children[j]).empty();
                }
        }
    }
}

function saveClosingHours(event){
    var schedule_days = $(".tab_container").children();
    var closing_hours = {};
    closing_hours['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken]').val();
    closing_hours['timeperiod'] = $('.timeperiod')[0].innerHTML; 
    closing_hours['location'] = $('.location')[0].innerHTML;    
    for (var i = 0; i < schedule_days.length; i++){
        var schedule_box = $(schedule_days[i]);
        var day = schedule_box.attr("id").toString();
        closing_hours[day] = [];
        var grid = $(schedule_box.children(".schedule_grid")[0]).children();
        for (var j = 0; j < grid.length; j++){
            var row = $(grid[j]);
            var time = row.children()[0].innerHTML;
            if (row.children(".closed_hours").length > 0){
                closing_hours[day].push(time);
            }
        }
    }

    $.ajax({
        "type"      : 'POST',
        "url"       : "/schedule/create/closing/",
        "data"      : $.param(closing_hours, true), 
        "error"     : function(){},
        "success"   : function(data){updateStatus(data)}
    });

}

function updateStatus(data){
    var data = JSON.parse(data);

    var schedule_status = $(".schedule_status");
    schedule_status.empty()

    schedule_status.append("<p>Closing Hours:</p>");
    var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for (var day in days){
        var hours = data[days[day]];

        if (hours != undefined){
            schedule_status.append("<p>" +days[day]+ "</p>");
            schedule_status.append("<ul>");
            for (var hour in hours){
                var in_time = hours[hour]['in_time'];
                var out_time = hours[hour]['out_time']; 
                schedule_status.append("<li>" + in_time + "-" + out_time + "</li>");
            }
            schedule_status.append("</ul>");
        }

    }

    schedule_status.show("fold");
}



/*
Takes a string representing a time and returns a time dictionary.
@param time := "hh:mm am/pm"
@return timeSplit := [hh,mm,am/pm]
*/
function timeDict(time){
    var timeSplit = {};
    var hourSplit = time.split(":");
    var minuteSplit = hourSplit[1].split(" ");
    timeSplit = {
        'hour': hourSplit[0],
        'minutes': minuteSplit[0],
        'period': minuteSplit[1]
    }
    return timeSplit;
}

function getPeopleList(){
    $.ajax({
        "url"       : "/schedule/people/",
        "data"      : {},
        "error"     : function(){},
        "success"   : function(data){populatePeopleList(data);}
    });
}

function populatePeopleList(data){

    data = JSON.parse(data);
    var peopleList = $(".add_person")
    if (data['people'].length != 0){
        for (var i = 0; i < data['people'].length; i++){
            peopleList.append("<option>" + data['people'][i] + "</option>");
        }
    }
    
}


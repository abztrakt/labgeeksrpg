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

    /*
    $(".content").click(function(){
        $(this).empty();
        $(this).toggleClass("selected");
        
        if ($(this).hasClass("selected")){
            var time = $(this).parent().children()[0].innerHTML;
            $(this).append(time);
        }else{
            $(this).empty();
        }
    });
    */

    // Bind the addClosingHours method to the button.
    $(".add_closing_hours").click(addClosingHours)

    getPeopleList();

    $(".add_person").change(function () {
        $(this).parent().text($(this).val());

        var table = $(this).parent("table");
        var date = $(table).find(".date th");
        $("#test").append(table.innerHTML);

    })
    .change();

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


function addClosingHours(){
    var startTime = $(this).parent().children(".closing_starting_hours")[0].value;
    var endTime = $(this).parent().children(".closing_ending_hours")[0].value;
    var schedule = $(this).parent().parent().parent().children(".schedule_grid")[0];

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
                $(schedule_row.children[j]).addClass("closed_hours");
                $(schedule_row.children[j]).html('closed');
        }
    }
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
    peopleList.append("<option> Add a person? </option>"); 
    if (data['people'].length != 0){
        for (var i = 0; i < data['people'].length; i++){
            peopleList.append("<option>" + data['people'][i] + "</option>");
        }
    }
    
}


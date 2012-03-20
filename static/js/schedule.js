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

    /*
    $(".test").click(function(){
        var str = $(this).text();
        $("#Monday td").css("background","white");
        $("#Monday td" + str).css("background","coral");

    });
    */
});

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


/* 
Review.js

This file deals with the reviews view for the people app.
*/ 


/*
Loads the page with events.
*/
$(document).ready(function() {
    $(".review_selector").click(function() {
        getReviewData(this.title);
    });

    $("#id_is_final").change(function() {
        if ($(this).is(':checked')){
            $("#is_final_message").removeClass("hidden").addClass("visible");
        }else{
            $("#is_final_message").removeClass("visible").addClass("hidden");
        }
    });
});

/*
Performs an Ajax call to grab the data. 
*/
function getReviewData(id){
    $.ajax({
        "url"       : document.location.href + 'info/',
        "data"      : {"id": id},
        "error"     : function(){ $("#timeperiod_info").append("Error, no data associated with this timeperiod")},
        "success"   : function(data) { loadReviewData(data);} 
    });
}

/*
Inserts the data into the page dynamically. 
*/
function loadReviewData(data){
    data = JSON.parse(data);

    var review_info = $("#review_info");
    review_info.removeClass("hidden").addClass("visible");

    var title = $("#review_title");
    title.empty();
    title.append(data['user']);

    var date = $("#review_date");
    date.empty()
    date.append(data['date']);

    score_list = $("#review_scores");
    score_list.empty();

    for(key in data['scores']){
        score_list.append("<li>" + key + ': ' + data['scores'][key] + "</li>");
    }

    comments_box = $("#review_comments");
    comments_box.empty();
    comments_box.append(data['comments']);
}


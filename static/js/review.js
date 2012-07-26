/* 
Review.js

This file deals with the reviews view for the people app.
*/ 


/*
Loads the page with events.
*/
$(document).ready(function() {
    $(".review_selector").click(function() {
        getReviewData(this.id);
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

    return_status = data['return_status'];
    if (return_status){
        var review_info = $("#review_info");
        review_info.removeClass("hidden").addClass("visible");

        var title = $("#review_title");
        title.empty();
        title.append(data['user']);

        var date = $("#review_date");
        date.empty()
        date.append(data['date']);

        review_list = $("#review_scores_comments");
        review_list.empty();
        var inline = [
            ' (N/A)',
            ' (unsatisfactory)',
            ' (needs work)',
            ' (satisfactory)',
            ' (very good)',
            ' (exemplary)'
        ];
        var intscore;
        var tooltips = {
            'Teamwork': 'Participates effectively in team efforts and encourages others. Treats people with fairness and respect. Carefully considers other points of view. Promotes collaboration amongst all student staff.',
            'Customer Service': 'Is professional in dealing with customers and satisfies their needs within the parameters of the service we provide.',
            'Dependability': 'Is responsible and punctual, has good attendance, and finds a substitute when unable to work.',
            'Integrity': 'Adheres to the UW principles and standards of conduct. Actively demonstrates commitment to UW computing policies. Honors commitments, earns trust.',
            'Communication': 'Expresses thoughts clearly in a way others understand and accept.',
            'Initiative': 'Offers suggestions for new or better methods of operations. Looks for opportunities for self improvment.',
            'Attitude': 'Is enthusiastic, interested, dilligent, and courteous.',
            'Productivity': 'Takes initiative to complete tasks and achieve goals. Plans and organizes work to improve output. Completes assigned projects by agreed completion date.',
            'Technical Knowledge': 'Has increased knowledge of hardware and/or software. Is up to date with the development of the UWTSC technical environment.',
            'Responsibility': 'Willingness to take on responsibility.',
            'Policies': 'Knows and enforces UW, C&C and staff policies.',
            'Procedures': 'Understands and follows departamental procedures.'
        };

        for(key in data['scores']){
            intscore = parseInt(data['scores'][key]);
            review_list.append("<li>" + key + ': ' + data['scores'][key] + inline[intscore] + '<br/><span class="tooltips">'+ tooltips[key] + "</span><p>" + data['comments'][key] + "</p></li>");
        }
        review_list.append("<li><strong>Average: " + data['average'] + "</strong></li>");
        review_list.append("<li><strong>Weighted Average: " + data['weighted'] + "</strong></li>");
        review_list.append("<li><strong>Overall: <p>" + data['overall'] + "</p></strong></li>");

    }
}

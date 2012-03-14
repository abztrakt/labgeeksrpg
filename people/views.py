from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
import json
from people.forms import *
from people.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

@login_required
def list_all(request):
    """ List all users in the system. (Alphabetically, ignoring case)
    """
    this_user = request.user
    if this_user.has_perm('people.add_uwltreview'):
        can_add_review = True
    else:
        can_add_review = False

    users = User.objects.filter(is_active=True).extra(select={'username_upper': 'upper(username)'}, order_by=['username_upper'])
    return render_to_response('list.html', locals(), context_instance=RequestContext(request))

@login_required
def view_profile(request, name):
    """ Show a user profile.
    """

    this_user = User.objects.get(username=name)
    if UserProfile.objects.filter(user=this_user): 
        #User has already created a user profile.
        profile = UserProfile.objects.get(user=this_user)

        if request.user.__str__() == name or request.user.is_superuser:
            edit = True

        if request.user.__str__() == name or request.user.has_perm('people.add_uwltreview'):
            can_view_review = True

        return render_to_response('profile.html', locals())
    else:
        #User HAS NOT created a user profile, allow them to create one.
        return create_user_profile(request,name)

@login_required
def create_user_profile(request,name):
    """ This view is called when creating or editing a user profile to the system.
        Allows the user to edit and display certain things about their information.
    """
    c = {}
    c.update(csrf(request))

    if request.user.__str__() != name and not request.user.is_superuser:
        # Don't allow editing of other people's profiles.
        return render_to_response('not_your_profile.html',locals(),context_instance=RequestContext(request))

    #Grab the user that the name belongs to and check to see if they have an existing profile.
    user = User.objects.get(username=name)
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = CreateUserProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            if profile:
                # Update the user profile
                profile = form.save()
            else:
                # Create a user profile, but DON'T add to database quite yet.
                profile = form.save(commit=False)

                # Add user to the profile and save
                profile.user = user
                profile.save()

                # Now, save the many-to-many data for the form (Required when commit=False)
                form.save_m2m()

            # Allow editing right after creating/editing a profile.
            edit = True
            # View the profile
            return render_to_response('profile.html',locals(),context_instance=RequestContext(request))
    else:
        form = CreateUserProfileForm(instance=profile)

    # Differentiate between a super user creating a profile or a person creating their own profile.
    this_user = request.user
    if profile:
        message = "You are editing a user profile for "
    else:
        message = "You are creating a user profile for "

    if this_user.__str__() == name:
        message += "yourself."
    else:
        message += name + "."
    # The following code is used for displaying the user's call_me_by or first name.
    try:
        profile = UserProfile.objects.get(user=this_user)
        if profile.call_me_by:
            this_user = profile.call_me_by
        else:
            this_user = this_user.first_name
    except:
        this_user = user.first_name

    return render_to_response('create_profile.html',locals(),context_instance=RequestContext(request))

@login_required
def view_and_edit_reviews(request,user):

    # Grab the user and any reviews they may have. 
    user = User.objects.get(username=user)
    this_user = request.user
    if this_user.has_perm('people.add_uwltreview') and this_user != user:
        can_add_review = True
    else:
        can_add_review = False

    if not can_add_review and this_user != user:
        return render_to_response('fail.html',locals(),context_instance=RequestContext(request))

    # TODO: Try to not use the is_superuser permission, instead maybe use a group permission.
    if this_user.is_superuser:
        final_reviewer = True
    else:
        final_reviewer = False

    try:
        badge_photo = UserProfile.objects.get(user=user).bagde_photo._get_url()
    except:
        badge_photo = None

    # Handle the form submission and differentiate between the sub-reviewers and the final reviewer.
    try:
        recent_review = UWLTReview.objects.filter(reviewer=this_user,user=user,is_final=False,is_used_up=False).order_by('-date')[0]
    except:
        recent_review = None

    if request.method == 'POST':
            
        if final_reviewer:
            form = CreateFinalUWLTReviewForm(request.POST, instance=recent_review)
        else:
            form = CreateUWLTReviewForm(request.POST, instance=recent_review)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.date = datetime.now().date()
            review.reviewer = this_user
            review.is_used_up = False

            # If the review is FINAL, mark the other reviews as used up and don't show use them for averaging the scores.
            if 'is_final' in form.cleaned_data.keys() and form.cleaned_data['is_final']:
                old_reviews = UWLTReview.objects.filter(user=user,is_final=False,is_used_up=False)
                for old_review in old_reviews:
                    old_review.is_used_up = True
                    old_review.save()
                review.is_used_up = False

            review.save()
            form.save_m2m()
            recent_review = review
            return HttpResponseRedirect('')
    else:
        if final_reviewer:
            form = CreateFinalUWLTReviewForm(instance=recent_review)
        else:
            form = CreateUWLTReviewForm(instance=recent_review)

    try:
        reviews = UWLTReview.objects.filter(user=user,is_used_up=False).order_by('-date')
    except UWLTReview.DoesNotExist:
        reviews = None

    # Gather the data from the reviews and separate out fields.    
    review_stats = {}

    # Used for table viewing.
    table_dict = {}
    if this_user == user:
        table_dict['user'] = 'Your review scores:'
    else:
        table_dict['user'] = "%s's review scores:" % user.username

    table_date_info = []
    table_scores = {}

    for review in reviews:
        scores = {
            'teamwork': review.teamwork,
            'customer service': review.customer_service,
            'dependability': review.dependability,
            'integrity': review.integrity,
            'communication': review.communication,
            'initiative': review.initiative,
            'attitude': review.attitude,
            'productivity': review.productivity,
            'technical knowledge': review.technical_knowledge,
            'responsibility': review.responsibility,
            'policies': review.policies,
            'procedures': review.procedures,
        }

        for key,value in scores.items():
            if review.is_final:
                if key in table_scores.keys():
                    table_scores[key].append(value)
                else:
                    table_scores[key] = [value]
            elif final_reviewer and review.reviewer != this_user:
                stats = {'value': value, 'reviewer':review.reviewer}
                if key in review_stats.keys():
                    review_stats[key].append(stats)
                else:
                    review_stats[key] = [stats]

        if review.is_final:
            table_date_info.append({'date':review.date,'id':review.id})

    table_dict['scores'] = table_scores
    table_dict['date'] = table_date_info

    # Create a list of all of the review fields and append review stats along with them. The stats won't be appended if the review isn't a final one.
    form_fields = []
    for field in form.visible_fields():
        stats = None
        if final_reviewer:
            name = ' '.join(str(x) for x in field.name.split('_'))
            if name in review_stats.keys():
                stats = review_stats[name]
                avg = sum(int(v['value']) for v in stats)/len(stats)
                stats.append({'value':avg,'reviewer': 'AVERAGE'})


        field_info = {
            'label_tag': field.label_tag,
            'help_text': field.help_text,
            'field': field,
            'name': field.name,
            'stats': stats
        }

        form_fields.append(field_info)

    # Notify the user of a previous review.
    recent_message = ''
    if recent_review:
        recent_message = 'Looks like you made a review for %s on %s. Saved entries have been filled out.' % (user,recent_review.date)

    # The following code is used for displaying the user's call_me_by or first name.
    try:
        profile = UserProfile.objects.get(user=this_user)
        if profile.call_me_by:
            this_user = profile.call_me_by
        else:
            this_user = this_user.first_name
    except:
        this_user = user.first_name

    # Return anything needed for the review form.
    args = {
        'request': request,
        'table_dict': table_dict,
        'form_fields': form_fields,
        'this_user': this_user,
        'user': user,
        'badge_photo': badge_photo,
        'can_add_review': can_add_review,
        'recent_message': recent_message,
    }
    return render_to_response('reviews.html', args, context_instance=RequestContext(request))

def view_review_data(request,user):
    user = User.objects.get(username=user)
    this_user = request.user
    data = request.REQUEST.copy()
    review_id = data.getlist('id')[0]
    review = UWLTReview.objects.get(id=review_id)
    if this_user.has_perm('people.add_uwltreview') and this_user != user:
        can_add_review = True
    else:
        can_add_review = False

    if not can_add_review and this_user != review.user or not review.is_final:
        result = json.dumps({
                'return_status': False,
                'message': 'You do not have permission to view this review.'
            })
        return HttpResponse(result)
    else:
        scores = {
                'Teamwork': review.teamwork,
                'Customer service': review.customer_service,
                'Dependability': review.dependability,
                'Integrity': review.integrity,
                'Communication': review.communication,
                'Initiative': review.initiative,
                'Attitude': review.attitude,
                'Productivity': review.productivity,
                'Technical knowledge': review.technical_knowledge,
                'Responsibility': review.responsibility,
                'Policies': review.policies,
                'Procedures': review.procedures,
            }
        result = json.dumps({
                'return_status': True,
                'user': str(review.user),
                'scores': scores,
                'date': review.date.strftime('%b. %d, %Y'),
                'comments': review.comments,
            })   
        return HttpResponse(result)

from labgeeksrpg.people.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms


class EmploymentStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(EmploymentStatus, EmploymentStatusAdmin)


class WorkGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(WorkGroup, WorkGroupAdmin)


class PayGradeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(PayGrade, PayGradeAdmin)


class TitleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Title, TitleAdmin)
admin.site.register(WageHistory)
admin.site.register(WageChangeReason)


class UWLTReviewWeightsAdmin(admin.ModelAdmin):
    list_display = ('name', 'effective_date',)

admin.site.register(UWLTReviewWeights, UWLTReviewWeightsAdmin)


class UWLTReviewAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'weights',)
    fields = ('weights',)

    def has_add_permission(self, request):
        return False

admin.site.register(UWLTReview, UWLTReviewAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'start_date', 'grad_date', 'supervisor', 'title', 'office',)
    search_fields = ('user', 'title', 'office', 'phone', 'alt_phone',)
    list_filter = ('status', 'start_date', 'grad_date', 'title', 'office',)
    actions = ['change_title', 'change_supervisor']

    class ModifyTitleForm(forms.Form):
        """ The form used by the change_location admin action.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        title = forms.ModelChoiceField(Title.objects)

    class ModifySupervisorForm(forms.Form):
        """ The form used by the change_supervisor admin action.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        supervisor = forms.ModelChoiceField(User.objects)

    def change_title(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifyTitleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.title = title
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "title for 1 person."
            else:
                message_bit = "title for %s people." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifyTitleForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_title'
        return render_to_response('admin/mod_title.html', {'mod_title_form': form, 'selected_action': selected_action}, context_instance=RequestContext(request, {'title': 'Change Title', }))
    change_title.short_description = "Change title for selected people"

    def change_supervisor(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifySupervisorForm(request.POST)
            if form.is_valid():
                supervisor = form.cleaned_data['supervisor']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.supervisor = supervisor
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "supervisor for 1 person."
            else:
                message_bit = "supervisor for %s people." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifySupervisorForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_supervisor'
        return render_to_response('admin/mod_supervisor.html', {'mod_supervisor_form': form, 'selected_action': selected_action}, context_instance=RequestContext(request, {'title': 'Change Supervisor', }))
    change_supervisor.short_description = "Change supervisor for selected people"
admin.site.register(UserProfile, UserProfileAdmin)

UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

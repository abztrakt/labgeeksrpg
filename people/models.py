from django.db import models
from datetime import date
from django.contrib.auth.models import User
from schedule.models import TimePeriod as s_TimePeriod


class EmploymentStatus(models.Model):
    """ Defines statuses that a Person could hold.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class WorkGroup(models.Model):
    """ Defines which team the person is on.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class PayGrade(models.Model):
    """ A tier for a position which determines the wage.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    wage = models.FloatField()

    def __unicode__(self):
        return self.name


class Title(models.Model):
    """ Provides a relation between WorkGroups and PayGrades.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField()
    workgroup = models.ForeignKey(WorkGroup)
    pay_grade = models.ForeignKey(PayGrade)

    def __unicode__(self):
        return self.name


class WageChangeReason(models.Model):
    """ Defines why a wage was given
    """
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class WageHistory (models.Model):
    """ Defines wage histories for users
    """
    class Meta:
        permissions = (
            ("view_wagehistory", "Can view wage history for users"),
        )

    effective_date = models.DateField()
    user = models.ForeignKey(User)
    wage = models.FloatField()
    wage_change_reason = models.ForeignKey(WageChangeReason)

    def __unicode__(self):
        return '%s - $%s' % (self.user, self.wage)


class UWLTReviewWeights(models.Model):
    """weights for UWLTreview weighted average
    """

    class Meta:
        verbose_name = "UWLT review weight"

    name = models.CharField(max_length=64)
    effective_date = models.DateField(default=date.today, blank=True)
    teamwork_multiplier = models.FloatField(default=1)
    customer_service_multiplier = models.FloatField(default=1)
    dependability_multiplier = models.FloatField(default=1)
    integrity_multiplier = models.FloatField(default=1)
    communication_multiplier = models.FloatField(default=1)
    initiative_multiplier = models.FloatField(default=1)
    attitude_multiplier = models.FloatField(default=1)
    productivity_multiplier = models.FloatField(default=1)
    technical_knowledge_multiplier = models.FloatField(default=1)
    responsibility_multiplier = models.FloatField(default=1)
    policies_multiplier = models.FloatField(default=1)
    procedures_multiplier = models.FloatField(default=1)

    def __unicode__(self):
        return self.name


class PerformanceReview(models.Model):
    """ Defines a review form used on staff
        Used a base class for any review model
    """
    user = models.ForeignKey(User, related_name='user_review')
    date = models.DateField()
    comments = models.TextField(null=True, blank=True)
    reviewer = models.ForeignKey(User)
    is_used_up = models.BooleanField()
    is_final = models.BooleanField()


class UWLTReview(PerformanceReview):
    """ A specific review model
    """

    class Meta:
        permissions = (
            ("finalize_uwltreview", "Can finalize UWLT Review"),
        )
        verbose_name = "UWLT review"

    teamwork = models.IntegerField(null=True, blank=True)
    teamwork_comments = models.TextField(null=True, blank=True)
    customer_service = models.IntegerField(null=True, blank=True)
    customer_service_comments = models.TextField(null=True, blank=True)
    dependability = models.IntegerField(null=True, blank=True)
    dependability_comments = models.TextField(null=True, blank=True)
    integrity = models.IntegerField(null=True, blank=True)
    integrity_comments = models.TextField(null=True, blank=True)
    communication = models.IntegerField(null=True, blank=True)
    communication_comments = models.TextField(null=True, blank=True)
    initiative = models.IntegerField(null=True, blank=True)
    initiative_comments = models.TextField(null=True, blank=True)
    attitude = models.IntegerField(null=True, blank=True)
    attitude_comments = models.TextField(null=True, blank=True)
    productivity = models.IntegerField(null=True, blank=True)
    productivity_comments = models.TextField(null=True, blank=True)
    technical_knowledge = models.IntegerField(null=True, blank=True)
    technical_knowledge_comments = models.TextField(null=True, blank=True)
    responsibility = models.IntegerField(null=True, blank=True)
    responsibility_comments = models.TextField(null=True, blank=True)
    policies = models.IntegerField(null=True, blank=True)
    policies_comments = models.TextField(null=True, blank=True)
    procedures = models.IntegerField(null=True, blank=True)
    procedures_comments = models.TextField(null=True, blank=True)
    missed_shifts = models.IntegerField(null=True, blank=True)
    missed_shifts_comments = models.TextField(null=True, blank=True)
    tardies = models.IntegerField(null=True, blank=True)
    tardies_comments = models.TextField(null=True, blank=True)
    weights = models.ForeignKey(UWLTReviewWeights, null=True, blank=True)

    def get_fields(self):
        return  [(field.name, field.value_to_string(self)) for field in UWLTReview._meta.fields]


class UserProfile(models.Model):
    """ Defines additional things we should know about users.
    """
    user = models.ForeignKey(User, unique=True, related_name='uwnetid')
    staff_photo = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)
    badge_photo = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)
    call_me_by = models.CharField(max_length=256, null=True, blank=True)
    status = models.ForeignKey(EmploymentStatus, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    grad_date = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey(User, related_name='supervisor', null=True, blank=True)
    title = models.ForeignKey(Title, null=True, blank=True)
    office = models.CharField(max_length=256, null=True, blank=True, default='')
    working_periods = models.ManyToManyField(s_TimePeriod, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    alt_phone = models.CharField(max_length=12, null=True, blank=True)
    wage = models.ManyToManyField(WageHistory, null=True, blank=True)

    def get_photo(self):
        if self.staff_photo and self.badge_photo:
            photo = self.staff_photo.url
        elif self.staff_photo and not self.badge_photo:
            photo = self.staff_photo.url
        elif not self.staff_photo and self.badge_photo:
            photo = self.badge_photo.url
        elif not self.staff_photo and not self.badge_photo:
            photo = "/static/img/stock_photo.jpg"
        else:
            photo = "/static/img/stock_photo.jpg"
        return photo

    def __unicode__(self):
        return "%s %s [%s]" % (self.user.first_name, self.user.last_name, self.user.username)

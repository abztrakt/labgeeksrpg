from django.core.management.base import BaseCommand, CommandError
from labgeeksrpg_config.models import Notification
import datetime
import urllib
import urllib2
from xml.dom.minidom import parse, parseString
from optparse import make_option


class Command(BaseCommand):

    args = ''
    help = 'Put the number of days or weeks in the argument and it will check a given timespan into the future. It will then get those holidays and create notifications.'

    option_list = BaseCommand.option_list + (
        make_option('-d', '--days',
                    action='store_true',
                    default=False,
                    help='Uses a timespan with a unit of days'),
        make_option('-w', '--weeks',
                    action='store_true',
                    default=False,
                    help='Uses a timespan with a unit of weeks'),
    )

    def handle(self, *args, **options):

        def add_zero(num):
            if num < 10:
                return '0' + repr(num)
            return '' + repr(num)

        now = datetime.date.today()
        end = now
        for duration in args:
            amount = int(duration)
            if options['days']:
                end = now + datetime.timedelta(days=amount)
            elif options['weeks']:
                end = now + datetime.timedelta(weeks=amount)

        start_date = repr(now.year) + add_zero(now.month) + add_zero(now.day)
        end_date = repr(end.year) + add_zero(end.month) + add_zero(end.day)

        response = urllib2.urlopen("http://myuw.washington.edu/cal/doExport.rdo?export.action=execute&export.format=xml&export.compress=false&export.name=Holidays&export.start.date=" + start_date + "&export.end.date=" + end_date)
        result = response.read()
        response.close()
        doc = parseString(result)
        calendar = doc.childNodes[0]
        if calendar.getElementsByTagName("Components"):
            components = calendar.getElementsByTagName("Components")[0]
            events = calendar.getElementsByTagName("VEVENT")
            for event in events:
                summary = event.getElementsByTagName("SUMMARY")
                holiday_name = summary[0].getElementsByTagName("value")[0].firstChild.nodeValue
                holiday_date = event.getElementsByTagName("DTSTART")[0].getElementsByTagName("value")[1].firstChild.nodeValue
                year = holiday_date[0:4]
                month = holiday_date[4:6]
                if month < 10:
                    month = month[1:]
                day = holiday_date[6:8]
                if day < 10:
                    day = day[1:]
                Notification.objects.get_or_create(title=holiday_name, due_date=datetime.datetime(int(year), int(month), int(day)))

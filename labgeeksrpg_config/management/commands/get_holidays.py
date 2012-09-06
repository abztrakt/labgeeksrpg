from django.core.management.base import BaseCommand, CommandError
from labgeeksrpg_config.models import Notification
import datetime
import urllib
import urllib2
from xml.dom.minidom import parse, parseString


class Command(BaseCommand):

    def handle(self, *args, **options):

        def add_zero(num):
            if num < 10:
                return '0' + repr(num)
            return '' + repr(num)

        num_of_days = 90
        now = datetime.date.today()
        end = now + datetime.timedelta(days=num_of_days)
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

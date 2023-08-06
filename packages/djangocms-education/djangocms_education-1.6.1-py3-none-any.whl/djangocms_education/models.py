from django.db import models
from datetime import datetime
from dateutil import relativedelta
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField


class Education(CMSPlugin):
    company = models.CharField(verbose_name='Company', max_length=255)
    job = models.CharField(verbose_name='Job', max_length=255)
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(verbose_name='End date', blank=True, null=True)
    description = HTMLField(verbose_name='Description', max_length=2048, null=True, blank=True)
    website = models.CharField(verbose_name='Website', max_length=255, null=True, blank=True)
    active_post = models.BooleanField(verbose_name='Active Position?')

    def __unicode__(self):
        return self.title

    def get_month_diff(self, d1, d2):

        delta = relativedelta.relativedelta(d2, d1)
        months = (delta.years*12) + delta.months

        return months

    @property
    def get_month_diff_string(self):

        if self.active_post:
            d2 = datetime.now()
        else:
            d2 = self.end_date

        month_diff = int(self.get_month_diff(self.start_date, d2))
        if month_diff < 12:
            diff_string = (str(month_diff) + ' ' + str(_('Months')))
            if month_diff <= 1:
                diff_string = (str(1) + ' ' + str(_('Month')))
        else:
            if month_diff % 12 == 0:
                year_diff = str(month_diff/12)
            else:
                year_diff = str(round(float(month_diff)/12, 1))
                print(year_diff)
            diff_string = (year_diff + ' ' + str(_('Years')))
            if year_diff == '1':
                diff_string = (str(1) + ' ' + str(_('Year')))

        return diff_string

    @property
    def get_relative_length(self):

        longest_post = self.get_longest_post()

        if self.active_post:
            end_date = datetime.now()
        else:
            end_date = self.end_date

        relative_percentage = (float(self.get_month_diff(self.start_date, end_date)) / float(longest_post)) * 100

        if relative_percentage <= 18:
            length_percentage = 18
        else:
            length_percentage = relative_percentage

        return int(length_percentage)

    def get_longest_post(self):

        longest = 0
        for education in Education.objects.all():

            if education.active_post:
                d2 = datetime.now()
            else:
                d2 = education.end_date

            diff = self.get_month_diff(education.start_date, d2)

            if diff > longest:
                longest = diff

        return longest

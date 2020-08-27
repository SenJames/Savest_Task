from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from django.db.models import Count
from django.utils.timezone import datetime
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from extensionApp.settings import EMAIL_HOST_USER
# Register your models here.
from extensionApp import settings
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from itertools import chain
from operator import attrgetter

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created', 'gender', 'make_active', 'status')
    list_filter = ('date_created', 'date_updated')
    # change_list_template = 'admin/profile/profile_change_list.html'

    actions = ['send_email']

    def send_email(self, request, queryset):
        print(request.POST)
        if 'apply' in request.POST:
            subject = request.POST.get('title')
            message = request.POST.get('msg')
            print(subject, message)
            recepient = []
            for item in queryset:
                email = item.user.email
                recepient.append(email)
            print(recepient)
            print(settings.EMAIL_HOST_USER)
            # recepient = str(sub['Email'].value())
            send_mail(subject, 
                message, settings.EMAIL_HOST_USER, recepient, fail_silently = False)
            self.message_user(request, 'Email Sent')
            return redirect('/admin/adminApp/profile/') 
            
        return render(
            request, 
            'admin/profile_intermediate.html', 
            context={'email':queryset}
        )
    send_email.short_description = 'Send Email'

    def status(self, obj):
        return obj.user.is_active
    status.short_description = 'Active'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<profile_id>.+)/update/$',
                self.admin_site.admin_view(self.btn_action),
                name='profile-update',
            ),
            url(
                r'^(?P<profile_id>.+)/deactivate/$',
                self.admin_site.admin_view(self.btn_action),
                name='profile-deact',
            ),
        ]
        return custom_urls + urls
    
    def make_active(self, obj):
        if obj.user.is_active == False:
            return format_html('<form method="POST"><a class="button" href="{}" name="toggle-act" id="{{obj.id}}">activate</a></form>', reverse('admin:profile-update', args=[obj.pk]))
        else:
            return format_html('<form method="POST"><a class="button" href="{}" name="toggle-deac" id="{{obj.id}}">deactivate</a></form>', reverse('admin:profile-deact', args=[obj.pk]))

    make_active.short_description = 'Set Status'
    make_active.allow_tags = True

    def update_status(self, request, profile_id, *args, **kwargs):
        print(request)
        return self.btn_action(
            request = request,
            profile_id = profile_id
        )

    def btn_action(self, request, profile_id):
        profile = self.get_object(request, profile_id)
        print(profile.user.is_active)
        if profile.user.is_active == False:
            print('yes False')
            profile.user.is_active = True
            profile.user.save()
        elif profile.user.is_active == True:
            profile.user.is_active = False
            print('yes True')
            profile.user.save()
        return redirect('/admin/adminApp/profile/') 





# class UserAdmin(admin.ModelAdmin):

class ProfileDetailsAdmin(admin.ModelAdmin):
    list_display = ('users','twenty_four','fourty_eight', 'oneMth')
    
    def users(self, obj):
        return obj.user
    
    def twenty_four(self, obj):
        created_user = User.objects.count()
        diff = timezone.now() - timedelta(days=1)
        created = Profile.objects.filter(date_created__gte=diff)
        print('yeah')
        print(created)
        return created.count()
    twenty_four.short_description = '24hrs Ago'
    
    
    def fourty_eight(self, obj):
        created_user = User.objects.count()
        diff = timezone.now() - timedelta(days=2)
        created = Profile.objects.filter(date_created__gte=diff)
        print('yeah')
        print(created)
        return created.count()
    fourty_eight.short_description = '48hrs Ago'
    

    def oneMth(self, obj):
        created_user = User.objects.count()
        diff = timezone.now() - timedelta(days=30)
        created = Profile.objects.filter(date_created__gte=diff)
        print('yeah')
        print(created)
        return created.count()
    oneMth.short_description = '30 Days Ago'
    


# admin.site.unregister(Group)
# admin.site.unregister(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileDetails, ProfileDetailsAdmin)


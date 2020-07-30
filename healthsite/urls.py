from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup_view, name="signup"),
    url(r'^meal/$', views.show_meal_plan, name='show_meal_plan'),
    url(r'^previousmeal/$', views.show_previous_meal_plan, name='show_previous_meal_plan'),
    url(r'^futuremeal/$', views.show_future_meal_plan, name='show_future_meal_plan'),
    url(r'^todaymeal/$', views.show_today_meal_plan, name='show_today_meal_plan'),
    url(r'^addmeal/$', views.add_meal, name='add_meal'),

    #url(r'^buy/$', views.buy, name='buy'),
    #url(r'^use/$', views.use, name='use'),
    #url(r'^utylize/$', views.utylize, name='utylize'),
]

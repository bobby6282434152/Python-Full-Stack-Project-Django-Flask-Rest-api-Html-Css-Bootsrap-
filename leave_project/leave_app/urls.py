from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # AUTH (JWT)
    path('register/', views.register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   
    # EMPLOYEE

    path('employees/', views.get_employees, name='get_employees'),
    path('employees/create/', views.create_employee, name='create_employee'),
    path('employees/update/<int:id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    
    # LEAVE
   
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/my/', views.my_leaves, name='my_leaves'),
    path('leave/all/', views.all_leaves, name='all_leaves'),

    
    # MANAGER ACTIONS
   
    path('leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),

    
    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
]
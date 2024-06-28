from django.contrib import admin
# from django import forms
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser, Parent, Guardian, Student, AdmissionForm, ClassGroup, Document, EmergencyContact
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(DefaultUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'class_groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number','role', 'class_groups', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'teacher':
            return qs.filter(class_groups__in=request.user.class_groups.all()).distinct()
        return qs
    
class AdmissionFormAdmin(admin.ModelAdmin):
    list_display = ('student', 'submission_date', 'status', 'assigned_teacher', 'applying_for_grade', 'term')
    list_filter = ('status', 'assigned_teacher', 'applying_for_grade', 'term')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'teacher':
            return qs.filter(assigned_teacher=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.assigned_teacher and request.user.role == 'teacher':
            obj.assigned_teacher = request.user
        super().save_model(request, obj, form, change)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'class_group')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'teacher':
            return qs.filter(class_group__in=request.user.class_groups.all()).distinct()
        return qs
    
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Parent)
admin.site.register(Guardian)
admin.site.register(Student, StudentAdmin)
admin.site.register(AdmissionForm, AdmissionFormAdmin)
admin.site.register(ClassGroup)
admin.site.register(Document)
admin.site.register(EmergencyContact)

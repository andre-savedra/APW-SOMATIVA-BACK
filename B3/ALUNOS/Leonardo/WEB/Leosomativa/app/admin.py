from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.accommodation import Accommodation
from .models.custom_user import CustomUser
from .models.guest import Guest
from .models.employee import Employee
from .models.reservation import Reservation
from .models.maintenanceHistory import MaintenanceHistory


# --- Custom User ---
@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'name', 'nationality', 'is_staff']
    list_display_links = ('id', 'email')
    search_fields = ('email', 'name')
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'nationality', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'nationality', 'password1', 'password2'),
        }),
    )

# --- Guest ---
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone']
    search_fields = ['name', 'email']

# --- Employee ---
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'registration_number', 'position', 'hire_date']
    list_filter = ['position']
    search_fields = ['user__email', 'user__name', 'registration_number']

# --- Accommodation ---
@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'type', 'status', 'max_guests', 'daily_rate', 'last_cleaning_date', 'last_cleaning_employee_name']
    list_filter = ['type', 'status']
    search_fields = ['number']

# --- Reservation ---
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'guest', 'accommodation', 'status', 'check_in', 'check_out', 'total_value']
    list_filter = ['status']
    search_fields = ['code', 'guest__user__email']

@admin.register(MaintenanceHistory)
class MaintenanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'accommodation', 'employee', 'status_before', 'status_after', 'date']
    list_filter = ['date', 'status_after', 'employee']
    search_fields = ['accommodation__number', 'employee__user__name', 'status_before', 'status_after']
    ordering = ['-date']


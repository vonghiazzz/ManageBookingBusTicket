from django.contrib import admin
from .models import *
from django.contrib.admin.actions import delete_selected
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password

from .models import Booking, Ticket, Bus  # Ensure Bus is imported

from django.contrib.auth.models import Group, Permission

from django.contrib.auth.forms import UserCreationForm



#Thêm trường khác vào bảng
from django.utils.html import mark_safe

# django-ckeditor
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget



# class CustomUserCreationForm(UserCreationForm):
#     phoneNumber = forms.CharField(max_length=10, required=True)
#     class Meta:
#         model = User
#         fields = ('phoneNumber')

class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username','email','first_name','last_name','password1','password2','phone_Number']


# Đè lại form Bus để sửa 
class BusForm(forms.ModelForm):
    #đè lại trường vehicleCondition để có form làm việc giống word
    # vehicleCondition=forms.CharField(widget=CKEditorUploadingWidget)
    def __init__(self, *args, **kwargs):
        super(BusForm, self).__init__(*args, **kwargs)
        # Ghi đè thuộc tính widget cho trường 'vehicleCondition'
        self.fields['vehicle_Condition'].widget = CKEditorUploadingWidget()


    class Meta:
        modes= Bus 
        fields='__all__'
        labels = {
            'vehicle_Condition': 'Vehicle Condition', # Đặt tên mặc định cho trường 'name'
            # 'total_Seats':'Total of Seats',
            'idType':'Type of Bus',
            # 'idTrip':'Name of Trip',
            'id_Driver':'ID Driver',
            # Các nhãn khác nếu cần
        }

class BusAdmin(admin.ModelAdmin):
    class Media: #Thêm css
        css={
            # 'all':('/static/css/main.css',) 
        }
        js={
            # 'all':('/static/js/main.js',) 
        }
    form = BusForm
    #Xuất ra trong trang quản lý admin của Ticket
    list_display=["id","created_date","id_Driver","active"] 
    #Chức năng search sẽ search được những nội dung dưới
    search_fields= ["created_date"] 
    #Show ra những filter của Ticket
    list_filter = ["active"]
    fields = ['active','id_Driver','idType', 'vehicle_Condition']
    # readonly_fields = ["reserved_Seats","total_Seats"]  

class CustomerAdmin(admin.ModelAdmin):
    list_display=["id","username","email","img","point"] 
    
    #Chức năng search sẽ search được những nội dung dưới
    search_fields= ["username","email"] 
    #Show ra những filter của Ticket
    # list_filter = ["idRole"]
    readonly_fields = ["last_login","date_joined","img", "point","password"]  
    fieldsets = (
        ('Account', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'img','avatar','phone_Number','point')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        
    )
    def img(self,user):
        # return mark_safe("<img src ='/static/{img_url}' alt='{alt}'width='120px'/>".format(img_url=user.avatar.name,alt=user.username))
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' alt='{user.username}' width='120px'/>")
        return "(No image)"

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


class DriverAdmin(admin.ModelAdmin):
    list_display=["id","username","email","img","totalDrivingTime","totalSalary"] 
    
    #Chức năng search sẽ search được những nội dung dưới
    search_fields= ["username","email"] 
    #Show ra những filter của Ticket
    # list_filter = ["idRole"]
    readonly_fields = ["last_login","date_joined","img", "totalDrivingTime","totalSalary"]  
    fieldsets = (
        ('Account', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'img','avatar','phone_Number','totalSalary','totalDrivingTime')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        
    )
  
    def img(self,user):
        # return mark_safe("<img src ='/static/{img_url}' alt='{alt}'width='120px'/>".format(img_url=user.avatar.name,alt=user.username))
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' alt='{user.username}' width='120px'/>")
        return "(No image)"

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

class UserAdmin(admin.ModelAdmin):
    list_display=["id","username","email","img"] 
    
    #Chức năng search sẽ search được những nội dung dưới
    search_fields= ["username","email"] 
    #Show ra những filter của Ticket
    # list_filter = ["idRole"]
    readonly_fields = ["last_login","date_joined","img","password"]  
    fieldsets = (
        ('Account', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'img','avatar','phone_Number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        
    )
    def img(self,user):
        # return mark_safe("<img src ='/static/{img_url}' alt='{alt}'width='120px'/>".format(img_url=user.avatar.name,alt=user.username))
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' alt='{user.username}' width='120px'/>")
        return "(No image)"

    
    #Băm password
    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
    



class TickForm(forms.ModelForm):
    class Meta:
            modes= Bus 
            fields='__all__'
            labels = {
                'img': 'Image', # Đặt tên mặc định cho trường 'name'
                'idSeatNumber':'Seat Number',
                'idBus':'ID Bus',
                'idTrip':'ID Trip',
             
                # Các nhãn khác nếu cần
            }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     id_bus = cleaned_data.get('idBu   s')

    #     trip_ids = [trip.id for trip in id_bus.trip.all()]
    #     if Ticket.objects.filter(name=name, idBus__trip__id__in=trip_ids).exists():
    #         raise ValidationError("Tên vé đã tồn tại trong một hoặc nhiều chuyến đi.")

    #     return cleaned_data

class TickAdmin(admin.ModelAdmin):
    class Media: #Thêm css
        css={
            # 'all':('/static/css/main.css',) 
        }
        js={
            # 'all':('/static/css/main.css',) 
        }
    form = TickForm
    #Xuất ra trong trang quản lý admin của Ticket
    list_display=["id","name","created_date","status","active"] 
    #Chức năng search sẽ search được những nội dung dưới
    search_fields= ["created_date"] 
    #Show ra những filter của Ticket
    list_filter = ["active","status"]
    #Thêm trường img
    readonly_fields=["avatar","idSeatNumber"]
    def avatar(self,ticket):
        if ticket.img:
            return mark_safe(f"<img src='{ticket.img.url}' alt='{ticket.name}' width='120px'/>")
        return "(No image)"
        # return mark_safe("<img src ='/static/{img_url}' alt='{alt}'width='120px'/>".format(img_url=ticket.img.name,alt=ticket.name))
    # def img(self,user):
    #     # return mark_safe("<img src ='/static/{img_url}' alt='{alt}'width='120px'/>".format(img_url=user.avatar.name,alt=user.username))
    #     if user.avatar:
    #         return mark_safe(f"<img src='{user.avatar.url}' alt='{user.username}' width='120px'/>")
    #     return "(No image)"

    




class BookAdmin(admin.ModelAdmin):
    
    #Thêm css,js cho Ticket
    class Media: #Thêm css
        css={
            # 'all':('/static/css/main.css',) 
        }
        js={
            # 'all':('/static/css/main.css',) 
        }
    # def delete_selected(self, request, queryset):
    #     # Bỏ qua hành động xóa mặc định bằng cách không gọi hàm delete_selected mặc định
    #     pass
    # Define the custom action function
    # actions = ['delete_selected_bookings']

    actions = ['delete_selected']
    # def delete_selected(self, request, queryset):
    #     for booking in queryset:
    #         if booking.id:  # Kiểm tra xem booking có được chọn không
    #             old_ticket = booking.idTicket
    #             print('old_ticket: ', old_ticket)
    #             booking.delete()
    #             if old_ticket:
    #                 old_ticket.status = False
    #                 old_ticket.save()
    #             # Cập nhật số ghế đã đặt cho xe buýt tương ứng
    #             if old_ticket.idTrip:
    #                 trip = old_ticket.idTrip
    #             else:
    #                 return
    #             if trip:
    #                 bus = trip.id_Buses
    #                 if bus:
    #                     bus.reserved_Seats = Ticket.objects.filter(idTrip__id_Buses=bus, status=True).count()
    #                     # print('bus.reserved_Seats: ',bus.reserved_Seats)

    #                     Bus.objects.filter(pk=bus.pk).update(reserved_Seats=bus.reserved_Seats)
    #                     # print('After update bus.reserved_Seats: ',bus.reserved_Seats)
    #             # else:
    #             #     # print(f"No ticket found for booking {booking.id}")
    #             #     return

    def delete_selected(self, request, queryset):
        for booking in queryset:
            if booking.id:
                old_ticket = booking.idTicket
                # print('old_ticket: ', old_ticket)
                
                # Xóa booking
                booking.delete()

                if old_ticket:
                    old_ticket.status = False
                    old_ticket.save()
                    # Kiểm tra và xử lý idTrip nếu tồn tại
                    if old_ticket.idTrip:
                        trip = old_ticket.idTrip
                        # if trip.id_Buses:
                        #     bus = trip.id_Buses
                        #     bus.reserved_Seats = Ticket.objects.filter(idTrip__id_Buses=bus, status=True).count()
                        #     Bus.objects.filter(pk=bus.pk).update(reserved_Seats=bus.reserved_Seats)
                        if trip:
                            trip.reserved_Seats = Ticket.objects.filter(idTrip=trip, status=True).count()
                            Trip.objects.filter(pk=trip.pk).update(reserved_Seats=trip.reserved_Seats)

                    else:
                        # Nếu không có idTrip, không cần xử lý gì thêm
                        print(f"No idTrip found for old_ticket {old_ticket.id}")

               

    
    # form = TickForm
    #Xuất ra trong trang quản lý admin của Ticket
    list_display=["id","idTicket","bookingDate","idCustomer","status"] 
    #Chức năng search sẽ search được những nội dung dưới
    search_fields= ["idTicket__name", "bookingDate"] 
    #Show ra những filter của Ticket
    list_filter = ["status"]


class SeatNumberAdminForm(forms.ModelForm):
    class Meta:
        model = SeatNumber
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        seat_number = cleaned_data.get('seat_number')
        idBus = cleaned_data.get('idBus')
        if seat_number and idBus:
            max_seat_number = idBus.totalSeats
            if seat_number > max_seat_number:
                raise forms.ValidationError(
                    f"The seat number must be less than or equal to {max_seat_number}"
                )

class SeatNumberAdmin(admin.ModelAdmin):
    form = SeatNumberAdminForm

class RouteAdminForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'


class RouteAdmin(admin.ModelAdmin):
    form = RouteAdminForm
    list_display=["id","name"]  



class TripAdminForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        # widgets = {
        #     'departureTime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        #     'arrivalTime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }
    def clean(self):
        cleaned_data = super().clean()
        startPoint = cleaned_data.get('departure_Station')
        endPoint = cleaned_data.get('ending_Station')
        # if not self.instance.pk:  # Chỉ kiểm tra khi tạo Trip mới
        #     trip_ids = [trip.id for trip in self.instance.id_Buses.all()]
        #     if Ticket.objects.filter(name=self.instance.name, idBus__trip__id__in=trip_ids).exists():
        #         raise ValidationError("Tên vé đã tồn tại trong một hoặc nhiều chuyến đi.")
        id_Buses = cleaned_data.get("idTrip_id_Buses")
        departure_Time = cleaned_data.get("departure_Time")
        arrival_Time = cleaned_data.get("arrival_Time")
        trip_name = f"{startPoint} - {endPoint} - {departure_Time}"

        if Ticket.objects.filter(name__startswith=trip_name).exists():
            raise ValidationError(f"Name of Ticket '{trip_name}' already exists.")
 
        if id_Buses:
            overlapping_trips = Trip.objects.filter(
                    id_Buses=id_Buses,
                    departure_Time__lte=arrival_Time + timedelta(hours=1),
                    arrival_Time__gte=departure_Time - timedelta(hours=1)
                ).exclude(pk=self.instance.pk)
            # print(overlapping_trips)
            # for trip in overlapping_trips:
            #     print(f"Overlapping Trip ID: {trip.id}, Departure Time: {trip.departure_Time}, Arrival Time: {trip.arrival_Time}")

            if overlapping_trips.exists():
                raise forms.ValidationError(f"Bus {id_Buses} is assigned to another trip during this period or within 1 hour after the trip.")

        #Check startPoint same endPoint
        if startPoint == endPoint:
            raise forms.ValidationError("Start point and end point must be different")
        
        # idTrip = cleaned_data.get("id")
        
        if departure_Time==None and arrival_Time==None:
            raise ValidationError("Departure time and Arrival time cannot be None.")
        #Check departure_Time must be before  today
        if departure_Time < timezone.now():
            raise ValidationError("Departure time cannot be in the past.")
        #Check arrival_Time must be after the departure_Time
        if departure_Time and arrival_Time <= departure_Time:
            raise ValidationError("Arrival time must be after the departure time.")

        # if id_Buses:
        #     for bus in id_Buses:
        #         # tickets_to_delete = Ticket.objects.filter(
        #         #     idBus=bus,
        #         #     idBus__trip__departure_Time=departure_Time,
        #         #     idBus__trip__arrival_Time=arrival_Time,
        #         #     idBus__trip__id = idTrip,
        #         # ).exclude(idBus__trip=self.instance)
                
        #         # if tickets_to_delete.exists():
        #         #     raise forms.ValidationError(f"Bus {bus.id} already has tickets for another trip with the same departure and arrival times.")
                
        #         # Kiểm tra xem bus đã có vé cho chuyến đi khác cùng thời gian chưa hay nằm trong thời gian nghỉ là 1h
        #         overlapping_trips = Trip.objects.filter(
        #             id_Buses=bus,
        #             departure_Time__lte=arrival_Time + timedelta(hours=1),
        #             arrival_Time__gte=departure_Time - timedelta(hours=1)
        #         ).exclude(pk=self.instance.pk)
        #         # print(overlapping_trips)
        #         # for trip in overlapping_trips:
        #         #     print(f"Overlapping Trip ID: {trip.id}, Departure Time: {trip.departure_Time}, Arrival Time: {trip.arrival_Time}")

        #         if overlapping_trips.exists():
        #             raise forms.ValidationError(f"Bus {bus.id} is assigned to another trip during this period or within 1 hour after the trip.")
        # Kiểm tra trùng lặp tên vé
        return cleaned_data


               

class TripAdmin(admin.ModelAdmin):
    form = TripAdminForm
    #Xuất ra trong trang quản lý admin của Ticket
    list_display=["id","name","departure_Time","arrival_Time","created_date","reserved_Seats", "total_Seats","active"] 
    #Chức năng search sẽ search được những nội dung dưới
    search_fields= ["created_date"] 
    #Show ra những filter của Ticket
    list_filter = ["active"]
    #Thêm trường img
    readonly_fields=["hours","reserved_Seats", "total_Seats"]
    # actions = ['delete_selected']
    # def delete_selected(self, request, queryset):
    #     for booking in queryset:
    #         if booking.id:  # Kiểm tra xem booking có được chọn không
    #             old_ticket = booking.idTicket
    #             # print(old_ticket)
    #             booking.delete()
    #             if old_ticket:
    #                 old_ticket.status = False
    #                 old_ticket.save()
    #                 # Cập nhật số ghế đã đặt cho xe buýt tương ứng
    #                 bus = old_ticket.idBus
    #                 # print(bus)
    #                 if bus:
    #                     bus.reserved_Seats = Ticket.objects.filter(idBus=bus, status=True).count()
    #                     Bus.objects.filter(pk=bus.pk).update(reserved_Seats=bus.reserved_Seats)
    



#Nhúng form user vào role để tiện thêm
# class UserInline(admin.StackedInline):
#     model = User
#     pk_name = 'idRole'

# class RoleAdmin(admin.ModelAdmin):
#     inlines = [UserInline]
#     list_display=["id", "name"]


# #Nhúng form bus vào trip để tiện thêm
# class BusInline(admin.StackedInline):
#     model = Bus
#     pk_name = 'idTrip'

# class TripAdmin(admin.ModelAdmin):
#     inlines = [BusInline]


# Custom admin site
class AppAdminSite(admin.AdminSite):
    site_header = "Bus ticket Management"
 
admin_site = AppAdminSite('myapp')

# Register your models here.
# admin.site.register(Role, RoleAdmin)
# admin.site.register(Bus,BusAdmin)
# admin.site.register(SeatNumber)
# admin.site.register(Trip,TripAdmin)
# admin.site.register(Type)
# admin.site.register(Ticket, TickAdmin)
# admin.site.register(Booking,BookAdmin)
# admin.site.register(User)

# Register your models here.    
# admin_site.register(Role, RoleAdmin)

admin_site.register(Driver,DriverAdmin)
admin_site.register(Customer,CustomerAdmin)
admin_site.register(Bus,BusAdmin)
admin_site.register(SeatNumber, SeatNumberAdmin)
admin_site.register(Trip, TripAdmin)
admin_site.register(Type)
admin_site.register(Ticket, TickAdmin)
admin_site.register(Booking,BookAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Route, RouteAdmin)
admin_site.register(Group)
admin_site.register(Permission)
























from django.shortcuts import render

# Create your views here.
from rest_framework import authentication,permissions

from rest_framework import generics

from service.permissions import OwnerOnly

from service.serializers import CustomerSerializer,WorkSerializer

from service.models import Customer,Work

from django.core.mail import send_mail

class CustomerListCreateView(generics.ListCreateAPIView):
    
    queryset = Customer.objects.all()
    
    serializer_class = CustomerSerializer
    
    authentication_classes = [authentication.TokenAuthentication]
    # authentication_classes=[authentication.BasicAuthentication]
    
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        return serializer.save(service_advisor=self.request.user)
    
class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    
    serializer_class = CustomerSerializer
    
    queryset = Customer.objects.all()
    
    authentication_classes = [authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAdminUser]
    
    def perform_update(self,serializer):
        
        work_status = serializer.validated_data.get("work_status")
        
        if work_status == "completed":
            
            print("snding email")
            
            subject = "vehicle service complition"
            
            vehicle_number = serializer.validated_data.get("vehicle_number")
            
            total = serializer.validated_data.get("get_work_total")
            
            message = f"your vehicle {vehicle_number} is ready to deliver . service amount{total}  "
            
            send_mail(subject,message,'sarathkv8895@gmail.com',{'amalroshank786@gmail.com'},fail_silently=False)
            
        serializer.save()
    
class WorkCreateView(generics.CreateAPIView):
    
    serializer_class = WorkSerializer
    
    authentication_classes = [authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAdminUser]
    
    
    def perform_create(self, serializer):
        
        id = self.kwargs.get("pk")
        
        cust_obj = Customer.objects.get(id=id)
        
        return serializer.save(customer_object = cust_obj)
    
class WorkUpdateDistoryView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = WorkSerializer
    
    queryset = Work.objects.all()
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [OwnerOnly]





# ANZC3U5HMG7HHGPXPZSFXNJR

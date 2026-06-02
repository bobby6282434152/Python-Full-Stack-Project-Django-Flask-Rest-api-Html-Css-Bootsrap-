from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee, Leave
from .serializer import EmployeeSerializer, LeaveSerializer


# ================= REGISTER =================
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role', 'Employee')

    if not username or not password:
        return Response({"error": "Username & Password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User(username=username)
    user.set_password(password)
    user.role = role   # 👈 IMPORTANT (used by signal)
    user.save()

    return Response({"message": f"{role} created successfully"})
# ================= LOGIN =================
@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password')
    )

    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "role": user.employee.role
    })


# ================= EMPLOYEE =================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employees(request):
    employees = Employee.objects.all()
    return Response(EmployeeSerializer(employees, many=True).data)


#CREATE EMPLOYEE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_employee(request):

    if request.user.employee.role != 'Manager':
        return Response({"error": "Only Manager can create"}, status=403)

    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role', 'Employee')

    if not username or not password:
        return Response({"error": "Username & Password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    #CREATE USER ONLY ONCE
    user = User(username=username)
    user.set_password(password)
    user.role = role   
    user.save()

    return Response({"message": f"{role} created successfully"})
# ================= LEAVE =================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_leave(request):
    serializer = LeaveSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(employee=request.user.employee, status='Pending')
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_leaves(request):
    leaves = Leave.objects.filter(employee=request.user.employee)
    return Response(LeaveSerializer(leaves, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_leaves(request):

    if request.user.employee.role != 'Manager':
        return Response({"error": "Access Denied"}, status=403)

    leaves = Leave.objects.all()
    return Response(LeaveSerializer(leaves, many=True).data)


# ================= MANAGER =================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_leave(request, leave_id):

    if request.user.employee.role != 'Manager':
        return Response({"error": "Only Manager"}, status=403)

    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'Approved'
    leave.save()

    return Response({"message": "Approved"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_leave(request, leave_id):

    if request.user.employee.role != 'Manager':
        return Response({"error": "Only Manager"}, status=403)

    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'Rejected'
    leave.save()

    return Response({"message": "Rejected"})


# ================= UPDATE =================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_employee(request, id):

    if request.user.employee.role != 'Manager':
        return Response({"error": "Only Manager"}, status=403)

    employee = get_object_or_404(Employee, id=id)

    employee.name = request.data.get('name', employee.name)
    employee.role = request.data.get('role', employee.role)
    employee.save()

    return Response({"message": "Updated"})


# ================= DELETE =================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_employee(request, id):

    if request.user.employee.role != 'Manager':
        return Response({"error": "Only Manager"}, status=403)

    employee = get_object_or_404(Employee, id=id)
    employee.delete()

    return Response({"message": "Deleted"})


# ================= DASHBOARD =================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):

    if request.user.employee.role != 'Manager':
        return Response({"error": "Access Denied"}, status=403)

    return Response({
        "total_employees": Employee.objects.count(),
        "total_leaves": Leave.objects.count(),
        "pending": Leave.objects.filter(status='Pending').count(),
        "approved": Leave.objects.filter(status='Approved').count(),
        "rejected": Leave.objects.filter(status='Rejected').count()
    })
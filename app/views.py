from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Member, Meter, Reading, Invoice
from app.serializers import MemberSerializer, ReadingSerializer, InvoiceSerializer, MeterSerializer

class MemberAPIView(APIView):
    def get(self, request):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MeterAPIView(APIView):
    def get(self, request):
        meters = Meter.objects.all()
        serializer = MeterSerializer(meters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MeterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeterDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Meter.objects.get(pk=pk)
        except Meter.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        meter = self.get_object(pk)
        serializer = MeterSerializer(meter)
        return Response(serializer.data)

    def put(self, request, pk):
        meter = self.get_object(pk)
        serializer = MeterSerializer(meter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        meter = self.get_object(pk)
        serializer = MeterSerializer(meter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        meter = self.get_object(pk)
        meter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MemberAPIView(APIView):
    def get(self, request):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = MemberSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MemberDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.

from app.models import Parcel
from app.serializers import ParcelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.core.paginator import Paginator


#main view for table
@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')


#CRUD class view
class ParcelEdit(APIView):

    #getting object from db
    def get_object(self, id):
        try:
            return Parcel.objects.get(id=id)
        except Parcel.DoesNotExist:
            raise Http404

    #working with GET request, sending data with pagination
    def get(self, request, format=None):
        parcels_list = Parcel.objects.filter(deleted_status="ACTIVE")
        paginator = Paginator(parcels_list, 25)
        all_pages = paginator.count
        page = request.GET.get('page')
        parcels = paginator.page(page)
        serializer = ParcelSerializer(parcels, many=True)
        out = {'total': str(all_pages), 'data': serializer.data}
        return Response(out)

    #working with POST request
    def post(self, request, format=None):
        serializer = ParcelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Working with PUT request
    def put(self, request, id, format=None):
        parcel = self.get_object(id)
        serializer = ParcelSerializer(parcel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    #working with DELETE request, deleted data are stored in db with flag 'DELETED'
    def delete(self, request, id, format=None):
        parcel = self.get_object(id)
        parcel.deleted_status = 'DELETED'
        parcel.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



































# #call start page - index.html
# def home(request):
#     assert isinstance(request, HttpRequest)
#     return render(request, 'index.html')
#
# #data manipulation on index.html
# def data(request):
#     if request.method == 'GET':
#         dict = request.GET
#         if 'method' in dict:
#             method=dict['method']
#         if 'model' in dict:
#             model=dict['model']
#         if 'limit' in dict:
#             limit=int(dict['limit'])
#         if 'page' in dict:
#             page=int(dict['page'])
#         if 'callback' in dict:
#             callback=dict['callback']
#         err = '{"meta": {"success":"false","msg":""}}'
#         ok = '{"meta": {"success":"false","msg":""}}'
#
#         if model == 'BookCrossing':
#             if method == 'Read':
#                 try:
#                     count = BookCrossing.objects.count()
#                     bookcrossing = BookCrossing.objects.all()[(page-1)*limit: page*limit]
#                     list = []
#                     for item in bookcrossing:
#                         dict_resp = {}
#                         dict_resp['id'] = str(item.id)
#                         dict_resp['first_name'] = item.first_name
#                         dict_resp['last_name'] = item.last_name
#                         dict_resp['sender_name'] = item.sender_name
#                         dict_resp['city'] = item.city
#                         dict_resp['delivery_status'] = item.delivery_status
#                         list.append(dict_resp)
#
#                     dict_out = {'data': list, 'meta': {'success': 'true','msg': '', 'total': str(count)}}
#                     json_format = json.dumps(dict_out)
#                     read_out = dict['callback'] + '(' + json_format + ')'
#                     return HttpResponse(read_out)
#                 except Exception:
#                     error_read = dict['callback'] +'({"data": "",' + err
#                     print('There is an error occurred, while trying to read data')
#                     return HttpResponse(error_read)
#             if method == 'Update':
#                 try:
#                     update_obj = BookCrossing.objects.get(id = dict['id'])
#                     update_obj.first_name = dict['first_name']
#                     update_obj.last_name = dict['last_name']
#                     update_obj.sender_name = dict['sender_name']
#                     update_obj.city = dict['city']
#                     update_obj.delivery_status = dict['delivery_status']
#                     update_obj.save()
#
#                     update_out = dict['callback'] + '({"data":{"id":' + str(update_obj.id) + '},' + ok
#                     return HttpRequest(update_out)
#                 except Exception:
#                     error_update = dict['callback'] + '({"data": {"id":' + dict['id'] +'},' + err
#                     print('There is an error occurred, while trying to update data')
#                     return HttpRequest(error_update)
#             if method == 'Create':
#                 try:
#                     create_obj = BookCrossing.objects.create(  \
#                         first_name      = dict['first_name'],  \
#                         last_name       = dict['last_name'],   \
#                         sender_name     = dict['sender_name'], \
#                         city            = dict['city'],        \
#                         delivery_status = dict['delivery_status'])
#
#                     create_out = dict['callback'] + '({"data":{"id":' + str(create_obj.id) + '},' + ok
#                     return HttpRequest(create_out)
#                 except Exception:
#                     error_create = dict['callback'] +'({"data":{"id":' + dict['id'] +'},' + err
#                     print('There is an error occurred, while trying to create data')
#                     return HttpRequest(error_create)
#             if method == 'Delete':
#                 try:
#                     delete_object = BookCrossing.objects.get(id = dict['id'])
#                     delete_object.deleted_status = 'DELETED'
#                     delete_object.save()
#
#                     delete_out = dict['callback'] + '({"data":null,' + ok
#                     return HttpRequest(delete_out)
#                 except Exception:
#                     error_delete = dict['callback'] + '({"data":null,' + err
#                     print('There is an error occurred, while trying to delete data')
#                     return HttpRequest(error_delete)

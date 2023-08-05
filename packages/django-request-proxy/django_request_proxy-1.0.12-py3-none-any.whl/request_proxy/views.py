import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# TODO: properly configure for custom permissions
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def proxy(request):
    try:
        full_path = request.get_full_path()
        path = full_path[11:18] + "/" + full_path[18:]
        if (request.method == "GET"):
            proxied_request = requests.get(path)
        elif (request.method == "POST"):
            proxied_request = requests.post(path)
        try:
            data = proxied_request.json()
        except:
            data = proxied_request.content
        return Response(status=proxied_request.status_code, data=data)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)
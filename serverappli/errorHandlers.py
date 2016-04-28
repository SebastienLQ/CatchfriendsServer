import logging
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)

def error404(request):
	logger.error("Someone hit a bad url : ", request)
	return HttpResponse(content="Bad URL", status=404)
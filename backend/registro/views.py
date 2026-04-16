from django.shortcuts import render

from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistroSerializer
from .services.orchestrator import RegistroOrchestrator
import logging

logger = logging.getLogger(__name__)


class RegistroView(APIView):
    """
    POST /api/registro/
    Recibe los datos del formulario y ejecuta el flujo completo de registro.
    """

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            registro = serializer.save()
            orchestrator = RegistroOrchestrator()
            stream = orchestrator.ejecutar(registro)

            logger.info(f"Registro iniciado para usuario {registro.usuario.email}")
            
            response = StreamingHttpResponse(
                stream,
                content_type="text/event-stream"
            )

            response['Cache-Control'] = 'no-cache'
            response['X-Accel-Buffering'] = 'no'

            return response

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # En producción esto iría a un sistema de logging (Sentry, etc.)
            logger.exception(f"Error en RegistroView: {str(e)}")
            return Response(
                {'error': 'Ocurrió un error interno. Por favor, intenta nuevamente más tarde.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
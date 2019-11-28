import io
import json

from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from rest_framework.views import APIView

from srenvio.utils import fedex_manager, weight_helpers
from srenvio.utils.responses import CustomResponse

from .models import Delivery, Parcel
from .serializers import DeliveryReadSerializer, DeliverySerializer

# Create your views here.


def _getFullParcel(parcial_parcel, track_id):
    carrier = ""
    if len(track_id) == 12:
        carrier = "FDXE"
    else:
        carrier = "FDXG"

    fedex_package = fedex_manager.checkFedexDelaiveryService(track_id, carrier)

    if fedex_package is None:
        return None

    total_weight = weight_helpers.getTotalWeight(float(parcial_parcel["weight"]), float(parcial_parcel["length"]),
                                                 float(parcial_parcel["width"]), float(parcial_parcel["height"]))
    over_weight = weight_helpers.getOverWeight(
        total_weight, fedex_package["real_weight"])

    full_parcel = parcial_parcel.copy()
    full_parcel.update(fedex_package)
    full_parcel["total_weight"] = total_weight
    full_parcel["over_weight"] = over_weight

    return full_parcel


def _create_pdf(deliveries, tracking_errors):

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    for delivery in deliveries:
        p.drawString(100, 780, "Número de guía :" +
                     delivery['tracking_number'])
        p.drawString(100, 760, "Peso usado :" +
                     str(delivery['parcel']['total_weight']))
        p.drawString(100, 740, "Peso real :" +
                     str(delivery['parcel']['real_weight']))
        if delivery['parcel']['over_weight'] > 0:
            p.drawString(100, 720, "Sobre peso :" +
                         str(delivery['parcel']['over_weight']))
        else:
            p.drawString(100, 720, "Sobre peso: NO SE HA GENERADO SOBREPESO")
        p.showPage()
    initial_y_value = 760
    if tracking_errors:
        p.drawString(100, 780, "Número de guía con errores :")
        for error in tracking_errors:
            p.drawString(120, initial_y_value, error)
            initial_y_value -= 20
            if initial_y_value < 200:
                p.showPage()
                initial_y_value = 760

    p.save()
    buffer.seek(0)
    return buffer


class DeliveryList(APIView):
    def post(self, request):
        file = request.FILES.get("json_file", None)
        if file is not None:
            data = file.read()
            data = json.loads(data)
        else:
            data = request.data
        deliveries = []
        tracking_errors = [] 
        for package in data:
            delivery_object = Delivery.objects.filter(
                tracking_number=package['tracking_number']).first()
            if not delivery_object:

                full_parcel = _getFullParcel(
                    package['parcel'], package['tracking_number'])
               
                if full_parcel is not None:
                    package['tracking_number'] = str(
                        package['tracking_number'])
                    package['parcel'] = full_parcel
                    delivery = DeliverySerializer(data=package)
                    delivery.is_valid(raise_exception=True)
                    delibery_created = delivery.save()
                    delivery_instance = DeliveryReadSerializer(
                        delibery_created).data
                    deliveries.append(delivery_instance)
                else:
                    tracking_errors.append(package['tracking_number'])
            else:
                delivery_instance = DeliveryReadSerializer(
                    delivery_object).data
                deliveries.append(delivery_instance)

        pdf = _create_pdf(deliveries, tracking_errors)

        filename = "report.pdf"
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="' + filename + '"'

       
        return response

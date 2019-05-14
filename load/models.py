from django.db import models
from django.core.exceptions import ValidationError
from users.models import Shipper, Carrier
from django.utils import timezone


class LoadManager(models.Manager):
    """
    A manager for the operations on the load objects.
    """

    def get_carrier_available_loads(self, request):
        """
        Get the list of all available loads.

        The loads that the shipper dropped will not be shown as available.

        :param django.http.HttpRequest request: Received request.
        :return: List of available loads for the Carrier
        :rtype: django.db.models.QuerySet
        """

        dropped_loads = self.get_carrier_rejected_loads(request)

        return self.filter(
            carrier=None).exclude(id__in=dropped_loads)

    def get_carrier_accepted_loads(self, request):
        """
        Get the list of loads that the carrier accepted.

        :param django.http.HttpRequest request: Received request.
        :return: List of accepted loads by the Carrier
        :rtype: django.db.models.QuerySet
        """

        carrier = Carrier.objects.get_carrier(request)

        return self.filter(carrier=carrier)

    def get_carrier_rejected_loads(self, request):
        """
        Get the list of loads that the carrier rejected.

        :param django.http.HttpRequest request: Received request.
        :return: List of rejected loads by the Carrier
        :rtype: django.db.models.QuerySet
        """

        carrier = Carrier.objects.get_carrier(request)
        return carrier.dropped_by.all()

    def get_shipper_available_loads(self, request):
        """
        Get the list of the shipper loads that are still available.

        :param django.http.HttpRequest request: Received request.
        :return: List of the Shipper available loads.
        :rtype: django.db.models.QuerySet
        """

        shipper = Shipper.objects.get_shipper(request)

        return self.filter(carrier=None, shipper=shipper)

    def get_shipper_accepted_loads(self, request):
        """
        Get the list of the shipper loads that were accepted.

        :param django.http.HttpRequest request: Received request.
        return: List of the Shipper accepted loads.
        :rtype: django.db.models.QuerySet
        """

        shipper = Shipper.objects.get_shipper(request)

        return self.exclude(carrier=None).filter(shipper=shipper)


class Load(models.Model):
    """Model for the loads.

    Stores the loads information in the DB fields: shipper, carrier, pickup_date, ref number, origin_city,
    destination_city, shipper_price, carrier_price, dropped_by.
    """

    def __str__(self):
        return self.ref

    def validate_date(date):
        if date < timezone.now().date():
            raise ValidationError("Date cannot be in the past")

    shipper = models.ForeignKey(
        Shipper, related_name='shipper', on_delete=models.PROTECT)
    carrier = models.ForeignKey(
        Carrier, related_name='carrier', on_delete=models.PROTECT, null=True, blank=True)
    pickup_date = models.DateField(validators=[validate_date])
    ref = models.CharField(max_length=200)
    origin_city = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=200)
    shipper_price = models.FloatField()
    carrier_price = models.FloatField()
    dropped_by = models.ManyToManyField(Carrier, related_name="dropped_by")

    objects = LoadManager()

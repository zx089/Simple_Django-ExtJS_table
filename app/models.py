from django.db import models

# Create your models here.


#Table data class
class Parcel(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    sender_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    delivery_status = models.CharField(max_length=255, null=True)
    deleted_status = models.CharField(max_length=255, default='ACTIVE')

    def __unicode__(self):
        return self.last_name

    # method for creating test data, by default it will create 1000 rows
    # to run it use django shell
    def create_data(count=1000, locale='en'):
        from elizabeth import Personal, Address

        person = Personal(locale)
        address = Address(locale)

        for i in range(count):
            parcel = Parcel(
                first_name=person.name(),
                last_name=person.surname(),
                sender_name=person.full_name(),
                city=address.city(),
                delivery_status='IN_PROCESS'
            )
            parcel.save()
        print('Database initiated. Rows: ' + str(count))


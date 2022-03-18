from django.db import models
from account.models import Branch, CustomUser as User
from django.forms.models import model_to_dict


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])

class Lead(models.Model, ModelDiffMixin):
    NEW = 'newlead'
    CONTACTED = 'contacted'
    DEMOSTART = 'demostart'
    DEMODONE = 'demodone'
    APPSTART = 'appstart'
    APPDONE = 'appdone'
    PROBATION = 'probation'
    CLIENT = 'client'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (DEMOSTART, 'Demo scheduled'),
        (DEMODONE, 'Demo completed'),
        (APPSTART, 'Application Sent'),
        (APPDONE, 'Application Signed'),
        (PROBATION, 'Probation'),
        (CLIENT, 'Client')
    ]

    STATE_CHOICES = [
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DC', 'District of Columbia'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming')
    ]

    company_name = models.CharField("Company name",max_length=255)
    street = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True, choices=STATE_CHOICES)
    website = models.CharField(max_length=255, blank=True, null=True)
    estimated_value = models.IntegerField(blank=True, null=True)

    contact_first_name = models.CharField(max_length=255)
    contact_last_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)
    contact_ext = models.CharField(max_length=32, blank=True)
    # second_phone = models.CharField(max_length=32, blank=True)
    contact_email = models.EmailField()
    # second_email = models.EmailField(max_length=255, blank=True)
    # contact_fax = models.CharField(max_length=32, blank=True)

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=NEW)
    branch = models.ForeignKey(Branch, related_name='assignedleads', blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(User, related_name='assignedleads', blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, related_name='leads', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    def save(self,*args,**kwargs):
        """
        save method override to include a record of any changes to notes
        """
        created = not self.pk
        super(Lead, self).save(*args,**kwargs)
        if created:
            Note.objects.create(
                body=f"Created by {self.created_by.get_full_name()}",
                lead=self
            )
        elif self.has_changed:
            status_choices = dict(self.STATUS_CHOICES)
            message = ""
            for field, values in self.diff.items():
                old_value = values[0] if field != 'status' else status_choices[values[0]]
                new_value = values[1] if field != 'status' else status_choices[values[1]]
                field = self._meta.get_field(field).verbose_name
                message += f"{field.capitalize()} changed from \"{old_value}\" to \"{new_value}\"\n"
            Note.objects.create(
                body=f"{message}Changed by {self.created_by.get_full_name()}",
                lead=self,
                created_by=None
            )

class Note(models.Model):
    body = models.TextField()
    lead = models.ForeignKey(Lead, related_name='notes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='notes', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.lead.pk) + ' - ' + str(self.created_at)

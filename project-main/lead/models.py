from django.db import models
from account.models import Branch, CustomUser as User

class Lead(models.Model):
    NEW = 'newlead'
    CONTACTED = 'contacted'
    DEMOSTART = 'demostart'
    DEMODONE = 'demodone'
    APPSTART = 'appstart'
    APPDONE = 'appdone'
    PROBATION = 'probation'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (DEMOSTART, 'Demo scheduled'),
        (DEMODONE, 'Demo completed'),
        (APPSTART, 'Application Sent'),
        (APPDONE, 'Application Signed'),
        (PROBATION, 'Probation')
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

    business_name = models.CharField(max_length=255)
    street = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True, choices=STATE_CHOICES)
    website = models.CharField(max_length=255, blank=True, null=True)
    estimated_value = models.IntegerField(blank=True, null=True)

    contact_person = models.CharField(max_length=255)
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

    def __str__(self):
        return self.business_name

class Note(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    lead = models.ForeignKey(Lead, related_name='notes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='notes', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
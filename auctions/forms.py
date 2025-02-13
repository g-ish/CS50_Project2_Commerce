from django import forms
from django.utils import timezone



FURNITURE = "Furniture"
ELECTRONICS = "Electronics"
SPORTS_EQUIPMENT = "Sports Equipment"
AUTOMOBILES = "Automobiles"
OTHER = "Other"
    
categories = [
    (FURNITURE, 'Furniture'),
    (ELECTRONICS, 'Electronics'),
    (SPORTS_EQUIPMENT, 'Sports Equipment'),
    (AUTOMOBILES, 'Automobiles'),
    (OTHER, 'Other'),
    ]


# Convert Django's time into HTML format 
def html_time():
    time = str(timezone.now())
    time = time.replace("\s", "T")
    return time

class NewAuction(forms.Form):
        
    item_title = forms.CharField(max_length=64, required=True, label="Item title")
    item_description = forms.CharField(widget=forms.Textarea, required=True, label="Item Description")
    item_category = forms.ChoiceField(choices=categories, required=True, label="Item Category") 
    starting_bid = forms.FloatField(min_value=0.00)

    # this is causing an eror, date works okay but datetime doesnt bring up the calendar. 
    expiry_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class':'datepicker', 
        'type': 'datetime-local',
        'value': html_time,
        'min': html_time}))
    # photo = forms.ImageField(label="Upload your photos", required=False)
    image_url = forms.URLField()

    

class NewComment(forms.Form):
    new_comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'style':'width: 50%'}))

class CategoryFilter(forms.Form):
        item_category = forms.ChoiceField(choices=categories, label="Item Category") 

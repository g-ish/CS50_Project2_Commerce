from django import forms


class NewAuction(forms.Form):
    
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

    
    item_title = forms.CharField(max_length=64, required=True, label="Item title")
    item_description = forms.CharField(widget=forms.Textarea, required=True, label="Item Description")
    item_category = forms.ChoiceField(choices=categories, required=True, label="Item Category") 
    starting_bid = forms.FloatField(min_value=0.00)

    # this is causing an erorr, date works okay but datetime doesnt bring up the calendar. 
    listing_duration = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime'}))
    # photo = forms.ImageField(label="Upload your photos", required=False)
    image_url = forms.URLField()

    




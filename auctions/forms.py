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
    # photo = forms.ImageField(label="Upload your photos", required=False)
    iamge_url = forms.URLField()

    




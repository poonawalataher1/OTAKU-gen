from django import forms

PANEL_LAYOUT_CHOICES = [
    ("1 Panel", "1 Panel"),
    ("2 Panel", "2 Panel"),
    ("4 Panel", "4 Panel"),
    ("6 Panel", "6 Panel"),
    ("9 Panel", "9 Panel"),
]

class PromptForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea, label="Enter your prompt")
    layout = forms.ChoiceField(choices=PANEL_LAYOUT_CHOICES)

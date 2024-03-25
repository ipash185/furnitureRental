from django import forms
from app.models import Threshold

class ThresholdForm(forms.Form):
    threshold_sofa = forms.IntegerField(label='Threshold Sofa')
    threshold_chair = forms.IntegerField(label='Threshold Chair')
    threshold_table = forms.IntegerField(label='Threshold Table')
    threshold_bed = forms.IntegerField(label='Threshold Bed')

    class Meta:
        model = Threshold
        fields = ('threshold_sofa', 'threshold_chair', 'threshold_table', 'threshold_bed')
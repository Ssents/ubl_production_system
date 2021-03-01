from django import forms

from .models import Order, Piece, ManpowerPlan

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("machine","production_type", "production_bond",
            "profile", "order_number", "order_colour", 
            "order_finish", "order_gauge", "order_width",
            "shift", "order_tonage", "order_completed")



class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = '__all__'


class ManpowerPlanForm(forms.ModelForm):
    class Meta:
        model = ManpowerPlan
        fields = '__all__'
        widgets = {
            'date':forms.DateInput(attrs={'class': 'form-control danda',
                                          'input_type':'date'}
                                    ),
            'shift': forms.TextInput(attrs={
                                            'class':'form-control'
                                     }),
                                     
        }
from django import forms

class TaskForm(forms.Form):
    title=forms.CharField(max_length=250)
    description=forms.CharField(max_length=250,widget=forms.Textarea,label='Task Description')
    due_date=forms.DateField(widget=forms.SelectDateWidget)
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[])

    # we have manually send related data to assigned_for form field to be shown as options
    # for that, we have to manually fetch the data 
    def __init__(self,*args,**kwargs):
        # print('At first: ',args,kwargs) #just checking the recieved data from view
        employees=kwargs.pop('employees',[]) #dictionary pop method
        # print('after poppinh:',args,kwargs) #checking what does pop() do
        # print('popped value: ',employees)
        super().__init__(*args,**kwargs) #data unpacking is a must

        #django form by default creates some field according to its attributes
        #all these field are stored in a  dictionary
        # print(self.fields)
        self.fields['assigned_to'].choices=[(emp.id,emp.name) for emp in employees]
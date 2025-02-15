from django import forms
from tasks.models import Task,TaskDetail

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
    
class TaskModelForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','due_date','assigned_to'] 

        widgets={'title':forms.TextInput(attrs={'class':'w-full border-2 border-gray-500 rounded-lg shadow-sm ','placeholder':'title'}),
            'description':forms.Textarea(attrs={'placeholder':'title','class':'w-full border-2 border-gray-500 rounded-lg shadow-sm'}),
            'due_date':forms.SelectDateWidget(attrs={
                'class':'w-full border-2 border-gray-500 rounded-lg shadow-sm'
            }),
                 'assigned_to':forms.CheckboxSelectMultiple}
        
class TaskDetailModelForm(forms.ModelForm):
    class Meta:
        model=TaskDetail
        fields=['priority','notes','asset']

        widgets={
            'priority':forms.Select(attrs={'class':'border-2 border-gray-500 rounded-lg shadow-sm'}),
            'notes':forms.Textarea(attrs={'class':'w-full border-2 border-gray-500 rounded-lg shadow-sm'})
        }

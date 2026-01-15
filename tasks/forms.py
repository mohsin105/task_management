from django import forms
from tasks.models import Task,TaskDetail, Project

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
        fields=['project','title','description','status','due_date','assigned_to'] 

        widgets={
            'project': forms.Select(
                attrs={
                    'class':'sm:w-full md:w-1/2 border-2 border-gray-500 p-4 my-2 rounded-md shadow-md'
                }
            ),
            'title':forms.TextInput(
                attrs={
                    'class':'w-full border-2 border-gray-500 p-4 my-2 rounded-md shadow-md ',
                    'placeholder':'title'
                    }),
            'description':forms.Textarea(
                attrs={
                    'placeholder':'title',
                    'class':'w-full border-2 border-gray-500 p-4 my-2 rounded-md shadow-md',
                    'rows':8,
                }),
            'status':forms.Select(
                attrs={
                    'class':'w-full p-4 my-2 rounded-md shadow-md border-2 border-gray-400 ',
                }
            ),
            'due_date':forms.DateInput(
                attrs={
                    'class':'w-full border-2 border-gray-500 p-4 my-2 rounded-md shadow-md ',
                    'type':'date'
                }),
            'assigned_to':forms.CheckboxSelectMultiple(
                attrs={
                    'class':'w-full border-2 p-4 my-2 rounded-md shadow-md'
                }
            )
        }
        
class TaskDetailModelForm(forms.ModelForm):
    class Meta:
        model=TaskDetail
        fields=['priority','notes','asset']

        widgets={
            'priority':forms.Select(
                attrs={
                    'class':'w-1/2 border-2 border-gray-500 p-4 my-2 rounded-lg shadow-md',
                }),
            'notes':forms.Textarea(
                attrs={
                    'class':'w-full border-2 border-gray-500 p-4 my-2 rounded-md shadow-md',
                    'placeholder':'Notes about the Task-Details'
                })
        }

class ProjectModelForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['name','description','start_date']

        widgets={
            'name':forms.TextInput(
                attrs={
                    'placeholder':'Project Name',
                    'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400'
                }
            ),
            'description':forms.Textarea(
                attrs={
                    'placeholder':'Description about the Project',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md',
                    'rows':8
                }
            ),
            'start_date':forms.DateInput(
                attrs={
                    'class':'w-1/2 p-4 my-2 border-gray-400 rounded-md shadow-xl',
                    'type':'date'
                }
            )
        }
    
    # def clean_name(self):
    #     data = self.cleaned_data.get("name")
        
    #     return data
    

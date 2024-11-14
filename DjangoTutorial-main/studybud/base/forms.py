from django.forms import ModelForm
from .models import Job, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import Settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Editted Registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ResumeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['resume']

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = self.instance
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            raise forms.ValidationError("Username already exists")
        return username

class ProfilePictureForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_picture']

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')

        if profile_picture:
            max_size = 5 * 320 * 320  # 5 MB size limit (adjust as needed)

            # If the image is larger than the max size, resize it
            if profile_picture.size > max_size:
                image = Image.open(profile_picture)
                
                # Resize the image (keep aspect ratio)
                max_width = 320  # Set the maximum width
                max_height = 320  # Set the maximum height
                image.thumbnail((max_width, max_height))

                # Save the resized image back to the file
                new_image = BytesIO()
                image.save(new_image, format='JPEG')  # or use PNG if needed
                new_image.seek(0)

                # Create a new InMemoryUploadedFile with the resized image
                profile_picture = InMemoryUploadedFile(
                    new_image, 'ImageField', profile_picture.name,
                    'image/jpeg', new_image.tell(), None
                )

        return profile_picture

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
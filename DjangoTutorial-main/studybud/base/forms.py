from django.forms import ModelForm
from .models import Job, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import Settings
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Editted Registration
class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('EMPLOYEE', 'Employee'),
        ('BUSINESS', 'Business'),
    ]

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="Which best describes you?", widget=forms.RadioSelect, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=True)
        if commit:
            user.save()
        return user

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
            max_size = 5 * 320 * 320  # 5 MB size limit
            max_width = 320  # Max width
            max_height = 320  # Max height

            # Load the image
            image = Image.open(profile_picture)

            # Convert to RGB if needed
            if image.mode in ("RGBA", "P"):  # Handle alpha or palette-based images
                image = image.convert("RGB")
            
            # Handle EXIF orientation if present
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = image._getexif()
                if exif and orientation in exif:
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # No EXIF data; skip adjustment
                pass

            # Resize the image if it exceeds the dimensions
            if profile_picture.size > max_size or image.size[0] > max_width or image.size[1] > max_height:
                image.thumbnail((max_width, max_height))

            # Save the resized image to a new file
            new_image = BytesIO()
            image.save(new_image, format='JPEG', optimize=True)
            new_image.seek(0)

            # Replace the uploaded file with the resized image
            profile_picture = InMemoryUploadedFile(
                new_image, 'ImageField', profile_picture.name,
                'image/jpeg', new_image.tell(), None
            )

        return profile_picture

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
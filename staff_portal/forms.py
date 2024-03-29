from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomStaffUser
from .models import Ingredient, Pizza, IngredientCategory
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    PasswordChangeForm as AuthPasswordChangeForm
)
from django.utils.translation import gettext_lazy as _


class StaffUserCreationForm(UserCreationForm):
    """
    Custom form for creating new staff users.


    """

    class Meta(UserCreationForm.Meta):
        model = CustomStaffUser
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super(StaffUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'id': 'register_username_id'}
        )

    def clean_username(self):
        """
        Validate the username to ensure it is not already in use.
        """
        username = self.cleaned_data.get('username')
        if CustomStaffUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use.")
        return username

        def clean(self):
            """
            Ensure that the two password entries match.
            """
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match.")


class CustomPasswordChangeForm(AuthPasswordChangeForm):
    """
    Custom form for changing passwords.
    """

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].error_messages = {'required': ''}


class IngredientForm(forms.ModelForm):
    """
    Custom form for creating and updating Ingredients
    """

    class Meta:
        model = Ingredient
        fields = ['name', 'category', 'description', 'origin', 'image']
        widgets = {
            'origin': forms.TextInput(attrs={'class': 'origin-input'}),
        }

    def clean_name(self):
        """
        Capitalize each word in the 'name' field.
        """
        return ' '.join(
            word.capitalize() for word in self.cleaned_data['name'].split()
        )

    def clean_image(self):
        """
        This method ensures that if no new image was uploaded in the form,
        the existing image is maintained. It raises a Validation Error
        if the uploaded file type is not an Image type.

        - If an image is found and it's not of an image file type, it raises a
          Validation Error
        - If no new image is uploaded, it retains the existing image
        - If there's no existing image, it defaults to None
        """
        image = self.cleaned_data.get('image', False)

        # Check if an image was uploaded and if it's the correct content type
        if image and hasattr(image, 'content_type'):
            if not image.content_type.startswith('image'):
                raise forms.ValidationError('Only image files are allowed.')
            return image

        # Retain the existing image if no new image is uploaded
        if self.instance and hasattr(self.instance, 'image'):
            return self.instance.image

        # If no new image and no existing image,
        # return None so the model's save method can set the default image
        return None


class MenuItemForm(forms.ModelForm):
    """
    A ModelForm for creating a Menu Item
    """

    # Define choices for the radio buttons.
    YES_NO_CHOICES = [
        (True, 'Yes'),
        (False, 'No')
    ]

    # ChoiceField for tomato sauce and mozzarella,
    # using radio buttons for selection.
    has_tomato = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Has Tomato Sauce?',
        widget=forms.RadioSelect
    )

    has_mozzarella = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label='Has Mozzarella?',
        widget=forms.RadioSelect
    )

    class Meta:
        """
        Meta class for the MenuItemForm.
        Specifies the model and fields to be used in the form.
        """

        # Links the form to the pizza model
        model = Pizza
        # Specify which fields of the Pizza model should appear in this form.
        fields = ['name', 'has_tomato', 'has_mozzarella', 'image']

    def clean(self):
        """
        Ensures each ingredient is unique
        """
        # Call the default clean method to get the cleaned data
        cleaned_data = super().clean()

        # Extracting ingredient IDs from the form data
        ingredient_ids = []
        for key, value in self.data.items():
            if key.startswith('ingredient_') and value:
                ingredient_ids.append(value)

        # Check for duplicate ingredient IDs
        # Comparing lengths: if the set's length (which removes duplicates)
        # is less than the list's,
        # it indicates duplicates in the original list.
        if len(ingredient_ids) != len(set(ingredient_ids)):
            # Prevents the form from being processed
            # and displays an error message to the user
            raise ValidationError("Each ingredient must be unique.")

        return cleaned_data

    def clean_name(self):
        # Capitalize each word in the name
        name_words = self.cleaned_data['name'].split()
        capitalized_words = (word.capitalize() for word in name_words)
        return ' '.join(capitalized_words)

    def clean_image(self):
        """
        This method ensures that if no new image was uploaded in the form,
        the existing image is maintained.
        It raises a Validation Error if the uploaded file is not an Image type.

        - If an image is found and it's not of an image file type, it raises a
          Validation Error
        - If no new image is uploaded, it retains the existing image
        - If there's no existing image, it defaults to None
        """
        image = self.cleaned_data.get('image', False)

        # Check if an image was uploaded and if it's the correct content type
        if image and hasattr(image, 'content_type'):
            if not image.content_type.startswith('image'):
                raise forms.ValidationError('Only image files are allowed.')
            return image

        # Retain the existing image if no new image is uploaded
        if self.instance and hasattr(self.instance, 'image'):
            return self.instance.image

        # If no new image and no existing image,
        # return None so the model's save method can set the default image
        return None

    def get_ingredient_choices(self):
        """
        Retrieves a structured list of ingredient choices categorized
        by their ingredient categories.

        Returns a list where each item is a tuple containing a category name
        and a list of ingredient choices.
        """
        # Get all ingredient categories.
        categories = IngredientCategory.objects.all()
        choices = []

        # Iterate over each category to build the choices structure.
        for category in categories:
            # Get ingredients belonging to the current category.
            category_ingredients = Ingredient.objects.filter(category=category)

            # Create a list of tuples for each ingredient in this category.
            # Each tuple contains the ingredient's ID and name.
            category_choices = [
                (ingredient.id, ingredient.name)
                for ingredient in category_ingredients
            ]

            # Append the category and its ingredients to the choices list.
            choices.append((category.name, category_choices))
        return choices

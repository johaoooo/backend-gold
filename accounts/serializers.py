from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    # Champs investisseur
    full_name = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    nationality = serializers.CharField(required=False, allow_blank=True)
    country_of_residence = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    company = serializers.CharField(required=False, allow_blank=True)
    position = serializers.CharField(required=False, allow_blank=True)
    investment_experience = serializers.ChoiceField(
        choices=['debutant', 'intermediaire', 'expert'],
        required=False,
        allow_blank=True
    )
    investment_areas = serializers.CharField(required=False, allow_blank=True)
    investment_min = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    investment_max = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    investor_type = serializers.ChoiceField(
        choices=['individual', 'family_office', 'institutionnel', 'business_angel', 'autre'],
        required=False,
        allow_blank=True
    )
    net_worth = serializers.CharField(required=False, allow_blank=True)
    motivation = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'role', 'phone',
            'full_name', 'birth_date', 'nationality', 'country_of_residence', 'city',
            'company', 'position', 'investment_experience', 'investment_areas',
            'investment_min', 'investment_max', 'investor_type', 'net_worth', 'motivation'
        ]

    def create(self, validated_data):
        # Extraire les champs investisseur
        investor_fields = [
            'full_name', 'birth_date', 'nationality', 'country_of_residence', 'city',
            'company', 'position', 'investment_experience', 'investment_areas',
            'investment_min', 'investment_max', 'investor_type', 'net_worth', 'motivation'
        ]
        
        user_data = {k: v for k, v in validated_data.items() if k not in investor_fields}
        investor_data = {k: v for k, v in validated_data.items() if k in investor_fields}
        
        user = User.objects.create_user(**user_data)
        
        # Remplir les champs investisseur
        for field, value in investor_data.items():
            if value:
                setattr(user, field, value)
        
        # Si le rôle est investisseur, il doit être approuvé par admin
        if user.role == 'investisseur':
            user.is_approved = False
        else:
            user.is_approved = True
            
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'phone', 'is_verified_kyc', 'is_approved',
            'full_name', 'birth_date', 'nationality', 'country_of_residence', 'city',
            'company', 'position', 'investment_experience', 'investment_areas',
            'investment_min', 'investment_max', 'investor_type', 'net_worth', 'motivation'
        ]
        read_only_fields = ['id', 'is_verified_kyc', 'is_approved']

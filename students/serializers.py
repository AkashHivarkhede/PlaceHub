from rest_framework import serializers
from .models import StudentProfile, Education


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = [
            'id',
            'student',
            'education_type',
            'institution_name',
            'board_or_university',
            'course_name',
            'specialization',
            'percentage',
            'cgpa',
            'passing_year',
            'created_at',
            'updated_at',
        ]


class StudentProfileSerializer(serializers.ModelSerializer):

    educational_background = EducationSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'alternate_phone_number',
            'address',
            'city',
            'state',
            'pincode',
            'cgpa',
            'passing_year',
            'is_placed',
            'is_active',
            'educational_background',
            'created_at',
            'updated_at',
        ]
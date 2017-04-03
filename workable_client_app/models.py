from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=255)
    full_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255, null=True)


class Status(models.Model):
    """Same as stage in candidate json output"""
    title = models.CharField(max_length=150)


class Skill(models.Model):
    title = models.CharField(max_length=150)


class Tag(models.Model):
    title = models.CharField(max_length=150)


class SocialProfile(models.Model):
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.URLField()


class WorkExperience(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    current = models.BooleanField()


class Education(models.Model):
    degree = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    current = models.BooleanField()


class Candidate(models.Model):
    # One line fields
    job = models.ForeignKey(Job, related_name='candidates')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, null=True)
    cover_letter = models.CharField(max_length=3000, null=True)
    summary = models.CharField(max_length=1000, null=True)
    resume_url = models.URLField(max_length=500, null=True)
    phone = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255)
    status = models.ForeignKey(Status, related_name='candidates')

    # ManyToMany fields
    skills = models.ManyToManyField(Skill)
    tags = models.ManyToManyField(Tag)
    work_experience = models.ManyToManyField(WorkExperience)
    social_profiles = models.ManyToManyField(SocialProfile)
    education = models.ManyToManyField(Education)

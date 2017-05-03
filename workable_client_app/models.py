from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=255)
    full_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255, null=True)
    wk_short_code = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Status(models.Model):
    """Same as stage in candidate json output"""
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Skill(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class SocialProfile(models.Model):
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    company = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    current = models.BooleanField()
    wk_id = models.CharField(max_length=15, unique=True)


class Education(models.Model):
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, null=True)
    field_of_study = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    wk_id = models.CharField(max_length=15, unique=True)


class Candidate(models.Model):
    # FKeys
    job = models.ForeignKey(Job, related_name='candidates')
    status = models.ForeignKey(Status, related_name='candidates')

    # One line fields
    wk_id = models.CharField(max_length=50, unique=True)
    updated_at = models.DateTimeField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, null=True)
    cover_letter = models.CharField(max_length=3000, null=True)
    summary = models.CharField(max_length=1000, null=True)
    resume_url = models.URLField(max_length=500, null=True)
    phone = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255, blank=True)

    # ManyToMany fields
    skills = models.ManyToManyField(Skill)
    tags = models.ManyToManyField(Tag)
    work_experience = models.ManyToManyField(WorkExperience)
    social_profiles = models.ManyToManyField(SocialProfile)
    education = models.ManyToManyField(Education)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class TimelineAction(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class TimelineStage(models.Model):
    title = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.title if self.title else ""


class TimelineMember(models.Model):
    wk_member_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class JobTimeline(models.Model):
    # action, stage name, created_at, member_name, and body
    job = models.ForeignKey(Job, related_name='activities')
    action = models.ForeignKey(TimelineAction)
    stage_name = models.ForeignKey(TimelineStage)
    member_name = models.ForeignKey(TimelineMember)
    body = models.CharField(max_length=3000, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return "{} {} {}".format(self.action, self.member_name, self.created_at)


class CandidateTimeline(models.Model):
    # action, stage name, created_at, member_name, and body
    candidate = models.ForeignKey(Candidate, related_name='activities')
    action = models.ForeignKey(TimelineAction)
    stage_name = models.ForeignKey(TimelineStage)
    member_name = models.ForeignKey(TimelineMember)
    body = models.CharField(max_length=3000, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return "{}".format(self.candidate)

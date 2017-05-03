import os
import json
import logging
import datetime
import requests
from urllib.parse import urljoin

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workable_api.settings")
django.setup()
from django.core.management.base import BaseCommand

from workable_api.secrets.secrets import *
from workable_client_app.models import *

logger = logging.getLogger(__name__)


# Workable API Client
class WorkableAPIClient:
    def __init__(self):
        self.subdomain = WORKABLE_DOMAIN
        self.root_endpoint = 'https://www.workable.com/spi/v3/accounts/'
        self.auth_token = 'Bearer {}'.format(WORKABLE_API_TOKEN)

    def get_response(self, endpoint):
        headers = {'Authorization': self.auth_token, 'Content-Type': 'application/json'}
        url = urljoin(self.root_endpoint, endpoint)
        r = requests.get(url, headers=headers)
        return r.json()

    def test_api(self):
        """Call to / endpoint"""
        resp = self.get_response('')
        print(resp)

    def get_jobs(self):
        api_endpoint = '{subdomain}/jobs'.format(subdomain=self.subdomain)
        resp = self.get_response(api_endpoint)
        return resp['jobs']

    def get_job_data(self, job_shortcode):
        api_endpoint = '{subdomain}/jobs/{shortcode}'.format(subdomain=self.subdomain, shortcode=job_shortcode)
        resp = self.get_response(api_endpoint)
        print(resp)

    def get_job_candidates(self, job_shortcode):
        api_endpoint = '{subdomain}/jobs/{job_shortcode}/candidates'.format(subdomain=self.subdomain, job_shortcode=job_shortcode)
        resp = self.get_response(api_endpoint)
        return resp['candidates']

    def get_candidate_info(self, job_shortcode, candidate_id):
        """
        Takes job_shortcode with candidate_id and returns full candidate info data.
        :param job_shortcode:
        :param candidate_id:
        :return:
        """
        api_endpoint = '{subdomain}/jobs/{job_shortcode}/candidates/{candidate_id}'.format(
            subdomain=self.subdomain, job_shortcode=job_shortcode, candidate_id=candidate_id
        )
        resp = self.get_response(api_endpoint)
        return resp['candidate']

    def get_job_activities(self, job_shortcode):
        api_endpoint = '{subdomain}/jobs/{job_shortcode}/activities'.format(subdomain=self.subdomain, job_shortcode=job_shortcode)
        resp = self.get_response(api_endpoint)
        return resp['activities']

    def process_job_activities(self, job_shortcode, job_obj):
        # Collect & save Job's Timeline
        job_activities = self.get_job_activities(job_shortcode=job_shortcode)
        for activity in job_activities:
            timeline_action_obj = TimelineAction.objects.get_or_create(title=activity['action'])[0]
            timeline_stage_obj = TimelineStage.objects.get_or_create(title=activity['stage_name'])[0]
            try:
                timeline_member_obj = TimelineMember.objects.get(wk_member_id=activity['member']['id'])
                timeline_member_obj.name = activity['member']['name']
                timeline_member_obj.save()
            except TimelineMember.DoesNotExist:
                timeline_member_obj = TimelineMember.objects.create(
                    wk_member_id=activity['member']['id'],
                    name=activity['member']['name']
                )
            JobTimeline.objects.get_or_create(
                job=job_obj,
                action=timeline_action_obj,
                stage_name=timeline_stage_obj,
                member_name=timeline_member_obj,
                body=activity['body'],
                created_at=activity['created_at']
            )

    def get_candidate_activities(self, candidate_id):
        api_endpoint = '{subdomain}/candidates/{candidate_id}/activities'.format(subdomain=self.subdomain, candidate_id=candidate_id)
        resp = self.get_response(api_endpoint)
        return resp['activities']

    def process_candidate_activities(self, candidate_id, candidate_obj):
        candidate_activities = self.get_candidate_activities(candidate_id)
        for activity in candidate_activities:
            timeline_action_obj = TimelineAction.objects.get_or_create(title=activity['action'])[0]
            timeline_stage_obj = TimelineStage.objects.get_or_create(title=activity['stage_name'])[0]
            try:
                timeline_member_obj = TimelineMember.objects.get(wk_member_id=activity['member']['id'])
                timeline_member_obj.name = activity['member']['name']
                timeline_member_obj.save()
            except TimelineMember.DoesNotExist:
                timeline_member_obj = TimelineMember.objects.create(
                    wk_member_id=activity['member']['id'],
                    name=activity['member']['name']
                )
            CandidateTimeline.objects.get_or_create(
                candidate=candidate_obj,
                action=timeline_action_obj,
                stage_name=timeline_stage_obj,
                member_name=timeline_member_obj,
                body=activity['body'],
                created_at=activity['created_at']
            )
        logger.info("Candidates Timeline Successfully Proceeded")


def main():
    try:
        logger.info("Process started at {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        workable_client = WorkableAPIClient()
        wk_jobs = workable_client.get_jobs()
        new_candidates_processed = 0
        old_candidates_processed = 0
        total_candidates_updated = 0

        # Find and iterate over each job
        for job in wk_jobs:
            # Add Job data into DB
            job_obj = Job.objects.get_or_create(
                title=job['title'],
                full_title=job['full_title'],
                department=job['department'],
                wk_short_code=job['shortcode']
            )[0]

            # Get all candidates for a job
            wk_candidates = workable_client.get_job_candidates(job['shortcode'])

            for candidate in wk_candidates:
                # Get candidate's full data
                wk_candidate_data = workable_client.get_candidate_info(job['shortcode'], candidate['id'])
                # print(json.dumps(wk_candidate_data))
                logger.info("Processing candidate: {} {}, ID: {}".format(
                    wk_candidate_data['firstname'], wk_candidate_data['lastname'], wk_candidate_data['id']))

                # When candidate profile updated the updated_at date field is also updating.
                # We will track whether candidate data was updated or not since last check.

                wk_candidate_updated_at = wk_candidate_data['updated_at']
                # wk_candidate_updated_at = datetime.datetime.strptime(wk_candidate_updated_at[:-1], "%Y-%m-%dT%H:%M:%S")

                try:
                    candidate_obj = Candidate.objects.get(wk_id=wk_candidate_data['id'])
                    # If candidate with 'id' exists then we need to check was it updated or no
                    # If it was updated then just update all candidate's data
                    old_candidates_processed += 1
                    if candidate_obj.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ") == wk_candidate_updated_at:
                        # print('Profile not updated!')
                        # Interrupt current candidate and move to the next iteration
                        continue
                    # Change updated_at date and keep going to update other fields
                    else:
                        candidate_obj.updated_at = wk_candidate_updated_at
                        total_candidates_updated += 1
                except Candidate.DoesNotExist:
                    # If candidate with 'id' doesn't exist then we need create a new Candidate record
                    # Prefill some static data
                    candidate_obj = Candidate(
                        wk_id=wk_candidate_data['id'],
                        updated_at=wk_candidate_updated_at,
                        first_name=wk_candidate_data['firstname'],
                        last_name=wk_candidate_data['lastname']
                    )
                    new_candidates_processed += 1
                # Then updating candidate_obj instances
                candidate_obj.job = job_obj
                candidate_obj.image_url = wk_candidate_data['image_url']
                candidate_obj.cover_letter = wk_candidate_data['cover_letter']
                candidate_obj.summary = wk_candidate_data['summary']
                candidate_obj.resume_url = wk_candidate_data['resume_url']
                candidate_obj.phone = wk_candidate_data['phone']
                candidate_obj.email = wk_candidate_data['email']

                # Stage/Status
                status_obj = Status.objects.get_or_create(title=wk_candidate_data['stage'])[0]
                candidate_obj.status = status_obj

                candidate_obj.save()

                # Skills
                try:
                    skills = wk_candidate_data['skills']
                    if skills:
                        for skill in skills:
                            skill_obj = Skill.objects.get_or_create(title=skill['name'])[0]
                            candidate_obj.skills.add(skill_obj)
                except KeyError:
                    pass

                # Tags
                try:
                    tags = wk_candidate_data['tags']
                    if tags:
                        for tag in tags:
                            tag_obj = Tag.objects.get_or_create(title=tag)[0]
                            candidate_obj.tags.add(tag_obj)
                except KeyError:
                    pass

                # Work experience
                try:
                    work_experience_list = wk_candidate_data['experience_entries']
                    if work_experience_list:
                        for exp in work_experience_list:
                            try:
                                exp_obj = WorkExperience.objects.get(wk_id=exp['id'])
                            except WorkExperience.DoesNotExist:
                                exp_obj = WorkExperience(wk_id=exp['id'])

                            exp_obj.title = exp['title']
                            exp_obj.start_date = exp['start_date']
                            exp_obj.end_date = exp['end_date']
                            exp_obj.company = exp['company']
                            exp_obj.industry = exp['industry']
                            exp_obj.current = exp['current']
                            exp_obj.save()
                            candidate_obj.work_experience.add(exp_obj)
                except KeyError:
                    pass

                # Social profiles
                try:
                    social_profiles = wk_candidate_data['social_profiles']
                    if social_profiles:
                        for sp in social_profiles:
                            sp_obj = SocialProfile.objects.get_or_create(type=sp['type'], name=sp['name'], url=sp['url'])[0]
                            candidate_obj.social_profiles.add(sp_obj)
                except KeyError:
                    pass

                # Education
                try:
                    wk_education_entries = wk_candidate_data['education_entries']
                    if wk_education_entries:
                        for edu_entry in wk_education_entries:
                            try:
                                education_obj = Education.objects.get(wk_id=edu_entry['id'])
                            except Education.DoesNotExist:
                                education_obj = Education(wk_id=edu_entry['id'], school=edu_entry['school'])

                            education_obj.degree = edu_entry['degree']
                            education_obj.field_of_study = edu_entry['field_of_study']
                            education_obj.start_date = edu_entry['start_date']
                            education_obj.end_date = edu_entry['end_date']
                            education_obj.save()
                            candidate_obj.education.add(education_obj)
                except KeyError:
                    pass
                # Save candidate instance to update it's data
                candidate_obj.save()

                # Process Candidate Activities
                workable_client.process_candidate_activities(wk_candidate_data['id'], candidate_obj)

                logger.info("Candidate: {} {} proceed successfully.".format(candidate_obj.first_name, candidate_obj.last_name))

        logger.info("Total old candidates proceeded: {}".format(old_candidates_processed))
        logger.info("Total new candidates proceeded: {}".format(new_candidates_processed))
        logger.info("Total candidates updated: {}".format(total_candidates_updated))
        logger.info("Finished successfully at {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logger.info("= " * 70)
    except Exception as e:
        logger.exception(e)


class Command(BaseCommand):
    help = 'To start the program run "python manage.py process_workable_api" command'

    def add_arguments(self, series_metrics):
        series_metrics.description = "Connects to JOB Board API(rossi-motors project), collects jobs and CV's data, " \
                                     "saves results into DataBase."

    def handle(self, *args, **options):
        main()


if __name__ == '__main__':
    main()

    # Test & Debug
    # workable_client = WorkableAPIClient()
    # workable_client.get_jobs()
    # workable_client.get_job_data('125CFA4F51')
    # workable_client.get_job_candidates('125CFA4F51')
    # workable_client.get_candidate_info('125CFA4F51', '14c06b7')  # Another John Doe
    # workable_client.get_candidate_info('125CFA4F51', '13b8300')  # John Doe

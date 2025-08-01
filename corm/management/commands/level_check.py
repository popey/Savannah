# dups = Contact.objects.filter(source__community_id=1).values('detail').annotate(dup_count=Count('member_id', distinct=True)).order_by().filter(dup_count__gt=1)

from django.core.management.base import BaseCommand, CommandError
import datetime
from django.shortcuts import reverse
from django.db.models import F, Q, Count, Max
from django.utils import timezone
from corm.models import Community, Member, Conversation, Contribution, Project, MemberLevel
from corm.models import pluralize
from notifications.signals import notify

from corm.webhooks import hook_triggered as send_hook

LEVEL_RELEVANCY_DAYS = 180

class Command(BaseCommand):
    help = 'Checks member activity and assigns them levels in a project'

    def add_arguments(self, parser):
        parser.add_argument('--community', dest='community_id', type=int)

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
        community_id = options.get('community_id')
        if community_id:
            communities = [Community.objects.get(id=community_id)]
        else:
            communities = Community.objects.filter(status=Community.ACTIVE)


        for community in communities:
            community_start = timezone.now()
            default_project, created = Project.objects.get_or_create(community=community, default_project=True, defaults={'name': community.name, 'owner':None, 'threshold_user':1, 'threshold_participant':10, 'threshold_contributor':1, 'threshold_core':10})
            all_projects = Project.objects.filter(community=community)

            # Check community-wide levels
            print("Checking member levels for %s" % community.name)
 
            convo_count = dict()
            contrib_count = dict()
            # Check per-project levels
            for project in all_projects:
                new_levels = dict()
                print("Checking member levels for %s / %s" % (community.name, project.name))
                now = timezone.now()
                MemberLevel.objects.filter(community=community, project=project, timestamp__lt=timezone.now() - datetime.timedelta(days=default_project.threshold_period)).delete()
                if self.verbosity >= 3:
                    print("%s project level deletes: %s" % (project.name, (timezone.now() - now).total_seconds()))

                now = timezone.now()
                speaker_filter = Q()
                if project.tag is not None:
                    speaker_filter = speaker_filter | Q(speaker_in__tags=project.tag)
                if project.member_tag is not None:
                    speaker_filter = speaker_filter | Q(tags=project.member_tag)
                if project.channels.count() > 0:
                    speaker_filter = speaker_filter | Q(speaker_in__channel__in=project.channels.all())
                members = Member.objects.filter(community=community).filter(speaker_in__timestamp__gte=timezone.now() - datetime.timedelta(days=project.threshold_period)).annotate(convo_count=Count('speaker_in__id', filter=speaker_filter, distinct=True), last_convo=Max('speaker_in__timestamp', filter=speaker_filter))
                if project.joined_start:
                    members = members.filter(first_seen__gte=project.joined_start)
                if project.joined_end:
                    members = members.filter(first_seen__lte=project.joined_end)
                for member in members:
                    if member.convo_count >= project.threshold_participant:
                        new_levels[member] = MemberLevel.PARTICIPANT
                        convo_count[member.id] = member.convo_count
                    elif member.convo_count >= project.threshold_user:
                        new_levels[member] = MemberLevel.USER
                        convo_count[member.id] = member.convo_count
                if self.verbosity >= 3:
                    print("%s project conversation levels: %s" % (project.name, (timezone.now() - now).total_seconds()))

                now = timezone.now()
                author_filter = Q()
                if project.tag is not None:
                    author_filter = author_filter | Q(contribution__tags=project.tag)
                if project.member_tag is not None:
                    author_filter = author_filter | Q(tags=project.member_tag)
                if project.channels.count() > 0:
                    author_filter = author_filter | Q(contribution__channel__in=project.channels.all())
                members = Member.objects.filter(community=community).filter(contribution__timestamp__gte=timezone.now() - datetime.timedelta(days=project.threshold_period)).annotate(contrib_count=Count('contribution__id', filter=author_filter, distinct=True), last_contrib=Max('contribution__timestamp', filter=author_filter))
                if project.joined_start:
                    members = members.filter(first_seen__gte=project.joined_start)
                if project.joined_end:
                    members = members.filter(first_seen__lte=project.joined_end)
                for member in members:
                    if member.contrib_count >= project.threshold_core:
                        new_levels[member] = MemberLevel.CORE
                        contrib_count[member.id] = member.contrib_count
                    elif member.contrib_count >= project.threshold_contributor:
                        new_levels[member] = MemberLevel.CONTRIBUTOR
                        contrib_count[member.id] = member.contrib_count
                if self.verbosity >= 3:
                    print("%s project contribition levels: %s\n" % (project.name, (timezone.now() - now).total_seconds()))

                for member, new_level in new_levels.items():
                    if hasattr(member, 'last_contrib'):
                        level, created = MemberLevel.objects.get_or_create(community=community, project=project, member=member, defaults={'level':new_level, 'timestamp':member.last_contrib, 'conversation_count':convo_count.get(member.id, 0), 'contribution_count':contrib_count.get(member.id, 0)})
                    else:
                        level, created = MemberLevel.objects.get_or_create(community=community, project=project, member=member, defaults={'level':new_level, 'timestamp':member.last_convo, 'conversation_count':convo_count.get(member.id, 0), 'contribution_count':contrib_count.get(member.id, 0)})
                    prev_level = level.level

                    if not created:
                        level.level = new_level
                        level.conversation_count = convo_count.get(member.id, 0)
                        level.contribution_count = contrib_count.get(member.id, 0)
                        level.save()

                    if created or new_level > prev_level:
                        event_name = 'EngagementLevel.up'
                    elif new_level < prev_level:
                        event_name = 'EngagementLevel.down'
                    else:
                        # No change in engagement level, skip firing webhook
                        continue
                    send_hook(
                        sender=self,
                        community=community,
                        event=event_name,
                        payload={
                                'project': {
                                    'id': project.id,
                                    'name': project.name,
                                    'default_project': project.default_project,
                                },
                                'member': member.serialize(),
                                'level': MemberLevel.LEVEL_MAP[new_level],
                                'previously': MemberLevel.LEVEL_MAP[prev_level] if not created else None,
                            }
                    )
            if self.verbosity >= 3:
                print("Time checking %s: %s\n" % (community, (timezone.now() - community_start).total_seconds()))


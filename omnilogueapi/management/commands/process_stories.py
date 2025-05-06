from django.core.management.base import BaseCommand
from omnilogueapi.models import Story, StorySection
import re


def process_markdown_links_in_content(content, story):
    """Process double-bracket markdown links in content"""
    if not content:
        return ""

    pattern = r"(\[\[.*?\]\])"
    segments = re.split(pattern, content)

    for index, segment in enumerate(segments):
        if segment.startswith("[[") and segment.endswith("]]"):
            segment_title = segment[2:-2]
            try:
                target_section_id = StorySection.objects.get(
                    story=story, title=segment_title
                ).id
                segments[index] = f"[{segment_title}]({target_section_id})"
            except StorySection.DoesNotExist:
                segments[index] = f"[{segment_title}](not-found)"

    return "".join(segments)


class Command(BaseCommand):
    help = "Process all markdown links in story sections"

    def handle(self, *args, **options):
        stories = Story.objects.all()

        self.stdout.write(f"Processing links for {stories.count()} stories...")

        for story in stories:
            self.stdout.write(f"Processing story: {story.title} (ID: {story.id})")

            sections = StorySection.objects.filter(story=story)
            processed_count = 0

            for section in sections:
                try:
                    # Process links in the section content
                    processed_content = process_markdown_links_in_content(
                        section.content, story
                    )

                    # Update the section with the processed content
                    if processed_content != section.content:
                        section.content = processed_content
                        section.save()
                        processed_count += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error processing section {section.id}: {str(e)}"
                        )
                    )

            self.stdout.write(
                f"Processed {processed_count} sections in story '{story.title}'"
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully processed all story sections")
        )

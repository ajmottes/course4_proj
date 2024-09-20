from django.db.models.signals import post_save
from django.dispatch import receiver

from movies.models import SearchTerm
from movies.tasks import notify_of_new_search_term

# The sender argument is used so that the hook is only called when a search term is saved
# THe uid field prevents duplicate receivers being instantiated
@receiver(post_save, sender=SearchTerm, dispatch_uid="search_term_saved")
# instance is the search term that was saved
# created is true if search term is created and false if it is updated
def search_term_saved(sender, instance, created, **kwargs):
    if created:
        # new SearchTerm was created
        #    print(f"A new SearchTerm was created: '{instance.term}'")
        notify_of_new_search_term.delay(instance.term)

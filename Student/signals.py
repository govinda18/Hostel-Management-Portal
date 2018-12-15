from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=HostelAllotment)
def generate_roominfo(sender, instance, created, **kwargs):
	if created:
		for roomno in range(instance.start_room,instance.end_room+1):
			roominfo = Roominfo()
			roominfo.room_no = roomno
			roominfo.scheme = instance
			roominfo.save() 
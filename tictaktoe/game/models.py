from django.db import models

class BoxNumber(models.Model):
	id= models.AutoField(primary_key=True)
	value = models.CharField(max_length=2)
	class Meta:
		db_table = u'box_number'
	def __unicode__(self):
		return self.value
# Create your models here.

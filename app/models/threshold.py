from django.db import models


class Threshold(models.Model):

    threshold_sofa = models.IntegerField(default=4)
    threshold_chair = models.IntegerField(default=4)
    threshold_table = models.IntegerField(default=4)
    threshold_bed = models.IntegerField(default=4)
    
    available_sofa = models.IntegerField(default=4)
    available_chair = models.IntegerField(default=4)
    available_table = models.IntegerField(default=4)
    available_bed = models.IntegerField(default=4)

    def __str__(self):
        if self.available_sofa < self.threshold_sofa:
            return "sofa"
        elif self.available_chair < self.threshold_chair:
            return "chair"
        elif self.available_table < self.threshold_table:
            return "table"
        elif self.available_bed < self.threshold_bed:
            return "bed"
        else:
            return "threshold"

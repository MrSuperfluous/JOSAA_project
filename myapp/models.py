from django.db import models


class Institute(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class AcademicProgram(models.Model):
    name = models.CharField(max_length=100)
    institute_name = models.ForeignKey(Institute, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('institute_name','name')

    def __str__(self):
        return self.name


# class AcademicProgram(models.Model):
#     name = models.CharField(max_length=100)
#     institutes = models.ManyToManyField(Institute, related_name='academic_programs')

#     def __str__(self):
#         return self.name


class SeatType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProgramRank(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    academic_program = models.ForeignKey(AcademicProgram, on_delete=models.CASCADE)
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE)
    year = models.IntegerField()
    round = models.IntegerField()
    opening_rank = models.IntegerField(null=True, blank=True)
    closing_rank = models.IntegerField(null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('institute', 'academic_program', 'year', 'round', 'seat_type', 'gender','opening_rank','closing_rank')

    def __str__(self):
        return f'{self.institute} - {self.academic_program} ({self.year})'

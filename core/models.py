from django.db import models

class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    course = models.IntegerField(blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    group_name = models.CharField(max_length=20, blank=True, null=True)
    is_head = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False  # Django не буде чіпати структуру таблиці
        db_table = 'students'

    # Це для красивого відображення зовнішніх ключів
    def __str__(self):
        return f"{self.surname} {self.name} ({self.group_name})"

class Subjects(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    hours = models.IntegerField(blank=True, null=True)
    semesters = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subjects'

    def __str__(self):
        return self.subject_name

class Exams(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_date = models.DateField(blank=True, null=True)
    # Django автоматично визначив ForeignKey
    student = models.ForeignKey(Students, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey(Subjects, models.DO_NOTHING, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exams'

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"
from django.db import models


class Book(models.Model):
    date = models.DateField(auto_now_add=True)
    memo = models.CharField(max_length=100)
    money = models.DecimalField(max_digits=10, decimal_places=0)
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.memo}: {self.money}"

    def get_absolute_url(self):
        return reverse('book:detail', kwargs={'pk': self.pk})
# Create your models here.

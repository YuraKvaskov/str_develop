from colorfield.fields import ColorField
from django.db import models


class EngineCat(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SparePart(models.Model):
    name = models.CharField(max_length=255)
    article = models.CharField(max_length=50, unique=True)
    materials = models.ManyToManyField(Material, related_name='spare_parts')  # Изменили на ManyToManyField
    special_feature = models.CharField(max_length=255, blank=True, null=True)
    material_properties = models.TextField(blank=True, null=True)
    engine_cat = models.ForeignKey(EngineCat, on_delete=models.CASCADE, related_name='spare_parts')
    groups = models.ManyToManyField(Group, related_name='spare_parts', blank=True)

    def __str__(self):
        return f"{self.name} ({self.article})"


class SparePartImage(models.Model):
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='spare_parts/')

    def __str__(self):
        return f"Image for {self.spare_part.name}"


class RepairKit(models.Model):
    name = models.CharField(max_length=255)
    article = models.CharField(max_length=50, unique=True)
    materials = models.ManyToManyField(Material, related_name='repair_kits')  # Изменили на ManyToManyField
    special_feature = models.CharField(max_length=255, blank=True, null=True)
    material_properties = models.TextField(blank=True, null=True)
    engine_cat = models.ForeignKey(EngineCat, on_delete=models.CASCADE, related_name='repair_kits')
    groups = models.ManyToManyField(Group, related_name='repair_kits', blank=True)
    parts = models.ManyToManyField(SparePart, through='RepairKitPart', related_name='repair_kits')

    def __str__(self):
        return f"{self.name} ({self.article})"


class RepairKitPart(models.Model):
    repair_kit = models.ForeignKey(RepairKit, on_delete=models.CASCADE)
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('repair_kit', 'spare_part')

    def __str__(self):
        return f"{self.spare_part.name} x{self.quantity} in {self.repair_kit.name}"


class RepairKitImage(models.Model):
    repair_kit = models.ForeignKey(RepairKit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='repair_kits/')

    def __str__(self):
        return f"Image for {self.repair_kit.name}"
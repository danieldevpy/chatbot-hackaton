from django.contrib.auth.models import AbstractUser
from django.db import models
from benefit.models import BenefitBase

class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True)
    benefits = models.ManyToManyField(BenefitBase, related_name="colaboradores")

    def json(self):
        """Função para retornar um json do usuário"""
        return {
            'name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'email': self.email,
            'cpf': self.cpf,
            'phone_number': self.phone_number,
            'benefits': [benefit.specific_benefit.json() for benefit in self.benefits.all() if benefit]
        }

    def text(self):
        benefit_text = ""
        for benefit in self.benefits.all():
            benefit_text += benefit.specific_benefit.text()
        return f"""
        Nome completo: {self.get_full_name()}
        Beneficios: {benefit_text}
        """
    def __str__(self):
        return self.username
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class BenefitBase(models.Model):
    name = models.CharField("Nome do Beneficio", max_length=100)
    description = models.TextField("Descrição do Beneficio", blank=True, null=True)
    content_type = models.ForeignKey(ContentType, verbose_name="Tipo de Beneficio", on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    specific_benefit = GenericForeignKey('content_type', 'object_id')
    info_extra = models.TextField("Informações extras")

    class Meta:
        verbose_name = "Benefício Base"
        verbose_name_plural = "Benefícios Base"

    def __str__(self) -> str:
        return self.name

    def calculate_value(self):
        """Método genérico para calcular o valor do benefício."""
        raise NotImplementedError("Subclasses devem implementar este método")
    
    def json(self):
        """Método genérico para gerar json."""
        raise NotImplementedError("Subclasses devem implementar este método")
    
    def text(self):
        raise NotImplementedError("x")

class TransportationVoucher(BenefitBase):
    monthly_amount = models.DecimalField("Valor Mensal", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = ("Vale Transporte")
        verbose_name_plural = ("Vales Transporte")

    def calculate_value(self):
        return self.monthly_amount
    
    def json(self):
        """Função para retornar um json"""
        return {
            'name': self.name,
            'description': self.description,
            'monthly_amount': float(self.monthly_amount)
        }
    
    def text(self):
        return f"""
            Nome do Beneficio: {self.name}
            Descrição: {self.description}
            Valor Mensal: {float(self.monthly_amount)}
            Informações extras: {self.info_extra}
        """

class MealVoucher(BenefitBase):
    value_per_meal = models.DecimalField("Valor por refeição", max_digits=10, decimal_places=2)
    quantity_of_meals = models.PositiveIntegerField("Quantidade de refeições")

    class Meta:
        verbose_name = ("Vale Refeição")
        verbose_name_plural = ("Vales Refeições")

    def calculate_value(self):
        return self.value_per_meal * self.quantity_of_meals

    def json(self):
        """Função para retornar um json"""
        return {
            'name': self.name,
            'description': self.description,
            'value_per_meal': float(self.value_per_meal),
            'quantity_of_meals': self.quantity_of_meals,
            'monthly_amount': float(self.calculate_value())
        }
    
    def text(self):
        return f"""
            Nome do Beneficio: {self.name}
            Descrição: {self.description}
            Valor por refeição: {float(self.value_per_meal)}
            Quantidade de refeições por mês: {self.quantity_of_meals}
            Valor Mensal: {float(self.calculate_value())}
            Informações extras: {self.info_extra}
        """
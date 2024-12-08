from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from .models import TransportationVoucher, MealVoucher

class BenefitBaseTestCase(TestCase):
    
    def setUp(self):
        """Configura os dados iniciais para os testes"""
        # Criando um tipo de conteúdo genérico
        self.content_type = ContentType.objects.create(model='benefitbase', app_label='yourapp')
        
        # Criando instâncias dos modelos
        self.transportation_voucher = TransportationVoucher.objects.create(
            name="Vale Transporte",
            description="Vale transporte mensal",
            content_type=self.content_type,
            object_id=1,
            monthly_amount=100.50
        )
        
        self.meal_voucher = MealVoucher.objects.create(
            name="Vale Refeição",
            description="Vale refeição diário",
            content_type=self.content_type,
            object_id=1,
            value_per_meal=20.0,
            quantity_of_meals=22
        )

    def test_transportation_voucher_calculate_value(self):
        """Testando o método 'calculate_value' para o TransportationVoucher"""
        self.assertEqual(self.transportation_voucher.calculate_value(), 100.50)

    def test_meal_voucher_calculate_value(self):
        """Testando o método 'calculate_value' para o MealVoucher"""
        expected_value = 20.0 * 22  # valor por refeição * quantidade de refeições
        self.assertEqual(self.meal_voucher.calculate_value(), expected_value)

    def test_transportation_voucher_json(self):
        """Testando o método 'json' para o TransportationVoucher"""
        expected_json = {
            'name': "Vale Transporte",
            'description': "Vale transporte mensal",
            'monthly_amount': 100.50
        }
        self.assertEqual(self.transportation_voucher.json(), expected_json)

    def test_meal_voucher_json(self):
        """Testando o método 'json' para o MealVoucher"""
        expected_json = {
            'name': "Vale Refeição",
            'description': "Vale refeição diário",
            'value_per_meal': 20.0,
            'quantity_of_meals': 22,
            'monthly_amount': 440.0  # 20.0 * 22
        }
        self.assertEqual(self.meal_voucher.json(), expected_json)


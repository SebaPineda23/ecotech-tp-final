import unittest

from sustentabilidad.emisiones import calcular_emisiones_carbono


class TestCalculoEmisiones(unittest.TestCase):

    def test_calculo_con_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_calculo_con_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(250, 0.5), 125.0)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_decimal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.5), 5.0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)

    def test_mensaje_de_error_consumo_negativo(self):
        with self.assertRaisesRegex(ValueError, "negativo"):
            calcular_emisiones_carbono(-50, 0.3)


if __name__ == "__main__":
    unittest.main()
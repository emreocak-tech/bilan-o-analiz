import unittest
import numpy as np
import pytest
from unittest.mock import MagicMock,patch
from bilanço_analiz import System
from bilanço_analiz import YardımcıAraçlar
@pytest.fixture()
def sistem():
    return System()
def test_cari_analiz(sistem):
    assert sistem.cari_oran()>0
def test_cari_oran_tahmin(sistem):
    sonuç=sistem.cari_oran_tahmin()
    assert isinstance(sonuç,(int,float,np.floating))
def test_likidite_oranı(sistem):
    assert sistem.likidite_oranı()>0
def test_likidite_tahmin(sistem):
    sonuç=sistem.likidite_tahmin()
    assert isinstance(sonuç,(int,float,np.floating))
def test_finansal_kaldıraç(sistem):
    assert sistem.finansal_kaldıraç_oranı()>0
def test_finansal_kaldıraç_tahmin(sistem):
    sonuç=sistem.finansal_kaldıraç_tahmin()
    assert isinstance(sonuç,(int,float,np.floating))
def test_roe_oranı(sistem):
    assert sistem.roe_oranı()>0
def test_roe_tahmin(sistem):
    sonuç=sistem.roe_tahmin()
    assert isinstance(sonuç,(int,float,np.floating))





class TestYapayZeka(unittest.TestCase):
    @patch('builtins.input', return_value='Test mesajı')
    @patch('bilanço_analiz.genai.Client')
    @patch('time.sleep', return_value=None)
    def test_yapay_zeka(self,mock_sleep,mock_client_class,mock_input):
        mock_client_instance=MagicMock()
        mock_client_class.return_value=mock_client_instance

        mock_cevap=MagicMock()
        mock_cevap.text="Sahte Cevap"
        mock_client_instance.models.generate_content.return_value = mock_cevap
        yardımcı=YardımcıAraçlar()
        sonuç=yardımcı.yapay_zeka()
        mock_input.assert_called_once()
        self.assertEquals(sonuç,"Sahte Cevap")
if __name__ == "__main__":
    unittest.main()


class test_dolar_tl(unittest.TestCase):
    @patch('bilanço_analiz.requests.get')
    def test_dolar_tl_başarılı(self,mock_get):
        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.json.return_value={
            "conversion_rates": {
                "TRY": 28.5
            }
        }
        mock_get.return_value=mock_response
        yardımcı_araç=YardımcıAraçlar()
        yardımcı_araç.dolar_tl()
    @patch('bilanço_analiz.requests.get')
    def test_dolar_tl_failure(self, mock_get):
        mock_response=MagicMock()
        mock_response.status_code=500
        mock_get.return_value=mock_response
        yardımcı_araç=YardımcıAraçlar()
        yardımcı_araç.dolar_tl()
        mock_get.assert_called_once()
if __name__ == "__main__":
    unittest.main()































































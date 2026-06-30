# Multi-Agent Pipeline

Bu doküman Job Analyzer → Resume Analyzer → Company Researcher akışının bu repo ile nasıl bağlanacağını özetler.

## Önerilen Sıra
1. **Job Analyzer**
   - JD'yi ayrıştır
   - must-have / nice-to-have / topic listesi üret
2. **Resume Analyzer**
   - Framework CV'yi kanıt bankasına dönüştür
   - gap ve coverage analizi yap
3. **Company Researcher**
   - Şirket sinyallerini ve söylem açılarını çıkar
4. **Fusion Layer**
   - Şema uyumlu çıktı üret
   - `build_report()` ve `rank_keyword_gaps()` sonuçlarını son prompta bağla

## Entegrasyon Notu
Bu repo'daki deterministik modüller, ajanların ürettiği serbest metni doğrulayan güvenlik katmanı olarak kullanılmalıdır.

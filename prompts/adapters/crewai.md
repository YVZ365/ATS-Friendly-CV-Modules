# CrewAI Adaptörü

Master Prompt'a ek olarak şu talimatları ekle:

```
## EK TALİMATLAR (CrewAI)
- Akışı üç ajan olarak düşün: Job Analyzer → Resume Analyzer → Company Researcher
- Her ajan kendi çıktısını JSON benzeri yapı ile sunsun
- Son birleştirme katmanında must-have, gap ve company-fit özetini ayrı başlıklarla ver
- Kaynağı olmayan iddiaları CV önerisine taşıma
```

## Güçlü Yanları
- Çok ajanlı görev ayrımı
- İş ilanı, CV ve şirket araştırmasını paralel düşünmeye uygun yapı

## Dikkat
- JSON alan adları repo şemalarıyla uyumlu tutulmalı
- Ajan çıktıları toplanmadan final CV önerisine geçilmemeli

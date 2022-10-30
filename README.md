# Drone Tabanlı Gözetleme

# TR 🇹🇷

Burada bulunan dosyalar TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı kapsamında 1919B012100897 nolu projenin yazılımsal kısmına aittir. Proje kapsamında DJITELLOPY isimli kütüphane kullanılarak drone tabanlı gözetleme gerçekleştirilmektedir. Proje kapsamında kullanılan yüz tespit ve teşhis modelleri bu kısıma eklenmemiştir. Bu modelleri sisteme ekledikten sonra proje çalışmaktadır.


## Proje Detayları

Proje kapsamında otonom şekilde hareket eden drone üzerinde bulunan kamera vasıtasıyla görüntüleri kaydeder. Görüntüleri kaydetme işlemi sırasında raspberry pi 4b isimli cihazdan yararlanılmıştır. Drone bu görüntüleri kaydettikten sonra python yardımıyla bu görüntüler üzerindeki yüzler tespit edilir ve bu görüntüler üzerinde yüz tanıma uygulanır. Bu yüz tanıma işlemi uygulandıktan sonra elde edilen yüzlerden "Derin Öğrenme" modelleri vasıtasıyla öznitelikler çıkartılır. Çıkarılan bu öznitelikler sırasında `"cosine similarity"` isimli benzerlik tespit yönteminden yararlanılmıştır. Bu yöntem sayesinde verilen iki vektörün benzerlikleri tespit edilebilmektedir. Bu benzerlik oranı  `0.45 den büyükse` iki yüz arasında benzerlik tespit edilmiş ve hedef kişi bulunmuştur.

![Schema](https://user-images.githubusercontent.com/46056478/198879615-b403816a-a252-4e7a-9afb-ca53a82dc8e8.png)

“djitellopy” isimli Python  kütüphanesi kullanılarak drone dan gelen görüntüler MB’e aktarılmıştır. Bu kütüpane sayesinde drone ile iletişim gerçekleştirilir. Bu iletişim sayesinde drone a ileri git, geri git vb. komutlar vererek drone un hareket etmesi sağlanır. 

Bu kütüphane yardımıyla alınan veriler “opencv” kullanılarak matrislere çevrilir. Bu veriler matrislere çevrildikten sonra ham olarak yerel dosyalara kaydedilir. Bu kaydetme işlemi sırasında “opencv” kütüphanesine ait “imwrite” fonksiyonu kullanılır. Kaydetme işleminde dosya adı dosyanın kaydedildiği tarih yapılmaktadır. Şekil 5’te görüntülerin kaydedildiği formata ait örnek gösterilmektedir. Bu dosyalar “droneKayit” isimli dosyanın içine kaydedilir. Bu kaydetme işlemi sırasında veriler ham olarak kaydedilir bu aşamada herhangi bir ön işleme yapılmaz, görüntüler “png” formatında kaydedilir.

Projede kullanılan program iki parçacıktan oluşur. İlk parçacık drone dan gelen görüntüleri kaydetmeye ve drone’u kontrol etmeye yarar. Diğer parçacık ise kaydedilen görüntüler üzerinde DÖ yöntemlerini kullanarak yüz tespiti ve teşhisi yapmaya yarar. İki farklı parçacık kullanılmasının sebebi DÖ modellerinin çalışması sırasında yaşanan gecikmelerin drone kontrolünü etkilemesinin önüne geçmektir. Proje kapsamında tek parçacık kullanıldığında drone kontrolünde yavaşlamalar ve aksaklıklar ortaya çıkmıştır. Bu yüzden iki farklı parçacık kullanılmış ve proje bu şekilde tamamlanmıştır.

Proje dosyalarında bulunan ana dizinde “goruntuler” isimli klasör vardır. Bu klasörde 3 farklı alt klasör bulunmaktadır. Bu alt klasörlerden ilki olan “bulunanKisiler” isimli klasöre tespit edilen kişiler kaydedilir. Diğer bir klasör olan “droneKayit” isimli klasörde ise drone’dan gelen ham görüntüler bulunmaktadır. “hedef” isimli son klasörde ise tespit edilmesi istenen kişilerin resimleri tutulmaktadır.

Ayrıca drone kontrolü kısmında bir Python kütüphanesi olan “pygame” isimli kütüphaneden yararlanılmıştır. Bu kütüphane sayesinde klavye girdilerinin ve drone dan gelen kamera görüntülerinin alınmasıdır. Bu kütüphane sayesinde drone’un ileri, geri, yukarı, aşağı gibi hareketleri klavyeden gelen girdiler yardımıyla yapılabilmektedir. 

Proje kapsamında drone 2 farklı şekilde çalışmaktadır. Bunlardan ilki drone’un kendi başına otonom olarak belirli bir doğrusal yörüngede hareket etmesi, diğeri ise drone’un klavyeden basılan tuşlar sayesinde kontrol edilmesidir. Proje kapsamında ilk kısım gerçekleştirilmiştir. Yani drone otonom bir şekilde doğrusal bir yörüngede kendi başına hareket etmektedir. Bu hareket işlemi sırasında Python kütüphanesi olan “time” kütüphanesinden yararlanılmıştır. Bu kütüphane ve “djitellopy” kütüphanesi sayesinde drone belirli bir mesafe gittikten sonra dönme (rotate) işlemi gerçekleştirilir. Dönme işlemi gerçekleştikten sonra drone tekrar aynı hızla ilerlemeye devam eder.

> Yüz tespit ve teşhis işlemi yapıldıktan sonra elde edilen sonuçlar “hedef” isimli dosyaya kaydedilir.


## Sonuçlar

![Sonuc](https://user-images.githubusercontent.com/46056478/198879881-beb95014-5b2a-4cb2-b658-f8866929797f.png)



## Kaynaklar

GitHub - damiafuentes/DJITelloPy: DJI Tello drone python interface using the official Tello SDK. Feel free to contribute! (n.d.). GitHub. Retrieved October 28, 2022, from https://github.com/damiafuentes/DJITelloPy

Python. (2022). Python.org. https://www.python.org/

GitHub - dji-sdk/Tello-Python: This is a collection of python modules that interact with the Ryze Tello drone. (n.d.). GitHub. Retrieved Oct 28, 2022, from https://github.com/dji-sdk/Tello-Python

OpenCV. (2022, Oct19). https://opencv.org/

PyGame. (2022). PyGame. https://www.pygame.org/


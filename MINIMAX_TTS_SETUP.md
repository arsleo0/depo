# Minimax TTS MCP Server - Kurulum Rehberi

Bu dokümantasyon, Minimax Text-to-Speech API'sini Claude Desktop ile nasıl entegre edeceğinizi gösterir.

## Özellikler

- 🎤 Metni yüksek kaliteli sese dönüştürme
- 🗣️ Çok sayıda ses seçeneği (erkek, kadın, çocuk vb.)
- ⚡ İki model: HD (yüksek kalite) ve Turbo (hızlı)
- 🎛️ Ses kontrolü: hız, ses seviyesi, pitch ayarları
- 💾 Otomatik ses dosyası kaydetme
- 🤖 Claude Desktop ile doğal dil entegrasyonu

## Gereksinimler

1. **Minimax Hesabı ve API Bilgileri**
   - Minimax hesabınızdan [https://www.minimax.io/](https://www.minimax.io/) API Key ve Group ID'nizi alın
   - API Key: Profil → API Keys → Create New Secret Key
   - Group ID: Profil → Account → Your Profile (19 haneli sayı)

2. **Python 3.10+**
   ```bash
   python3 --version
   ```

3. **Gerekli Paketler**
   ```bash
   pip install mcp aiohttp
   # veya
   pip install -r requirements.txt
   ```

## Kurulum Adımları

### 1. API Bilgilerini Hazırlayın

Minimax API bilgilerinizi iki şekilde kullanabilirsiniz:

**Seçenek A: Ortam Değişkenleri (Önerilen)**
```bash
export MINIMAX_API_KEY="your_api_key_here"
export MINIMAX_GROUP_ID="your_group_id_here"
```

**Seçenek B: Claude Desktop içinde manuel ayarlama**
(Claude'a "set_minimax_credentials" tool'u ile bilgileri verebilirsiniz)

### 2. Claude Desktop Yapılandırması

Claude Desktop yapılandırma dosyasını düzenleyin:

**Linux/Mac:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

Aşağıdaki konfigürasyonu ekleyin:

```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": [
        "/home/user/depo/godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "minimax-tts": {
      "command": "python3",
      "args": [
        "/home/user/depo/minimax_tts_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "MINIMAX_API_KEY": "YOUR_API_KEY_HERE",
        "MINIMAX_GROUP_ID": "YOUR_GROUP_ID_HERE"
      }
    }
  }
}
```

**Önemli:**
- `/home/user/depo/minimax_tts_mcp_server.py` kısmını gerçek dosya yolunuzla değiştirin
- `YOUR_API_KEY_HERE` ve `YOUR_GROUP_ID_HERE` kısımlarını gerçek bilgilerinizle değiştirin
- Windows'ta yollar şöyle olmalı: `"C:\\Users\\KullaniciAdi\\depo\\minimax_tts_mcp_server.py"`

### 3. Claude Desktop'ı Yeniden Başlatın

Yapılandırma değişikliklerinin geçerli olması için Claude Desktop'ı tamamen kapatıp yeniden açın.

## Kullanım

Claude Desktop'ta doğal dilde isteklerinizi yazın:

### Basit TTS Örneği
```
"Merhaba dünya, bu bir test mesajıdır" metnini sese dönüştür
```

### Ses Seçimi ile
```
"Welcome to our podcast" metnini Affectionate_Male_Voice sesi ile sese dönüştür
```

### Gelişmiş Ayarlar
```
"Bu heyecan verici bir duyuru!" metnini female-shaonv sesi ile, hızlı konuşarak ve yüksek tonla sese dönüştür
```

### Parametrelerle Tam Kontrol
Claude aşağıdaki parametreleri kullanır:
- `text`: Sese dönüştürülecek metin
- `voice_id`: Ses kimliği (örn: male-qn-qingse, female-shaonv)
- `model`: speech-02-hd veya speech-02-turbo
- `speed`: 0.5 - 2.0 arası (varsayılan: 1.0)
- `vol`: 0.1 - 10.0 arası (varsayılan: 1.0)
- `pitch`: -12 - 12 arası (varsayılan: 0)
- `output_format`: mp3, wav, pcm, flac
- `filename`: İsteğe bağlı dosya adı

### Mevcut Sesleri Listeleme
```
Minimax'te hangi sesler mevcut?
```

### API Durumunu Kontrol Etme
```
Minimax API bağlantı durumu nedir?
```

### Çıktı Dizinini Değiştirme
```
Ses dosyalarını /home/user/Music dizinine kaydet
```

## Mevcut Sesler

**Erkek Sesler:**
- `male-qn-qingse` - Standart erkek ses
- `Affectionate_Male_Voice` - Sevecen erkek sesi
- `Audiobook_Male_Voice` - Sesli kitap erkek sesi
- `News_Male_Voice` - Haber spikeri

**Kadın Sesler:**
- `female-shaonv` - Genç kadın sesi
- `Gentle_Female_Voice` - Yumuşak kadın sesi
- `Mature_Female_Voice_1` - Olgun kadın sesi
- `Sweet_Female_Voice` - Tatlı kadın sesi

**Özel Sesler:**
- `Cute_Child_Voice` - Çocuk sesi
- `Calm_Narration` - Sakin anlatım
- `Documentary_Narration` - Belgesel anlatımı

## Varsayılan Ayarlar

- **Çıktı Dizini:** `~/minimax_tts_outputs/`
- **Model:** `speech-02-hd` (yüksek kalite)
- **Ses:** `male-qn-qingse`
- **Format:** `mp3`
- **Hız:** `1.0`
- **Ses Seviyesi:** `1.0`
- **Pitch:** `0`

## Hata Ayıklama

### MCP Server Loglarını Görme

**Mac:** `Cmd + Option + Shift + i`
**Windows/Linux:** `Ctrl + Shift + i`

Console'da şöyle loglar göreceksiniz:
```
[MINIMAX-TTS-MCP] INFO: Minimax TTS MCP Server başlatılıyor...
[MINIMAX-TTS-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
[MINIMAX-TTS-MCP] INFO: TTS isteği gönderiliyor: 25 karakter, voice=male-qn-qingse
```

### Yaygın Hatalar

#### "API bilgileri ayarlanmamış" hatası
```bash
# Ortam değişkenlerini kontrol edin
echo $MINIMAX_API_KEY
echo $MINIMAX_GROUP_ID

# Veya Claude'da manuel ayarlayın:
set_minimax_credentials ile API key ve Group ID'yi ayarla
```

#### "Invalid API key" hatası
- API Key ve Group ID'nin doğru olduğundan emin olun
- API Key'in başında "Bearer " eklemeyin (otomatik eklenir)
- Bölge uyumsuzluğu olabilir, doğru endpoint'i kullandığınızdan emin olun

#### "mcp paketi bulunamadı"
```bash
pip install mcp aiohttp
```

#### "aiohttp paketi bulunamadı"
```bash
pip install aiohttp
```

### Manuel Test

Sunucuyu doğrudan test etmek için:
```bash
python3 minimax_tts_mcp_server.py
```

Eğer hiçbir hata vermeden beklemede kalıyorsa, server doğru çalışıyor demektir.

## Güvenlik Notları

- API anahtarlarınızı **asla** git'e commit etmeyin
- Ortam değişkenlerini kullanmayı tercih edin
- API anahtarlarınızı güvenli bir şekilde saklayın
- Gerekirse `.gitignore` dosyasına `*_config.json` ekleyin

## API Limitleri

Minimax API'sinin kullanım limitleri vardır:
- Dakika başına istek limiti
- Aylık karakter/ses limiti
- Abonelik planınıza göre değişir

Detaylar için [Minimax dokümantasyonuna](https://www.minimax.io/docs) bakın.

## Destek

Sorunlarınız için:
1. Developer Console loglarını kontrol edin
2. API bilgilerinizin doğru olduğundan emin olun
3. `get_api_status` tool'u ile bağlantı durumunu kontrol edin
4. Issue açın veya yardım isteyin

## Gelişmiş Özellikler

### Streaming Desteği (Gelecek Sürüm)
Şu anda ses dosyaları tamamen oluşturulduktan sonra kaydedilir. Gelecek versiyonlarda streaming desteği eklenebilir.

### Ses Klonlama (Voice Cloning)
Minimax API ses klonlama özelliği de sunar. İlgilenen geliştiriciler için tool'a eklenebilir.

## Lisans

MIT

## Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

# Text-generation-webui MCP Server - Claude Desktop Entegrasyonu

Bu MCP server, Claude Desktop uygulamasını **Text-generation-webui** ile entegre eder. Claude, lokal olarak fine-tune edilmiş LLM modellerinizle etkileşime geçebilir.

## 🎯 Özellikler

- 🤖 Text-generation-webui ile doğrudan bağlantı
- 📝 Chat tamamlama (instruction-following modeller için)
- 📄 Basit metin tamamlama
- 📋 Model listesi görüntüleme
- ⚙️ Esnek parametre ayarları (temperature, top_p, max_tokens)
- 🔐 API key desteği (opsiyonel)

## 📋 Gereksinimler

### 1. Text-generation-webui'yi Başlatma

Text-generation-webui'nizi **--api** bayrağı ile başlatmanız gerekiyor:

**Windows için:**
```cmd
cd C:\Users\mcgus\Documents\text-generation
start_windows.bat --api
```

veya komut satırından:
```cmd
python server.py --api
```

**Ek parametreler:**
- `--api-port 5000` - Varsayılan port 5000 (değiştirmek isterseniz)
- `--api-key yourkey` - API anahtarı ile güvenlik (opsiyonel)
- `--listen` - Ağdan erişim için (varsayılan localhost)

### 2. Python Gereksinimleri

```bash
# Python 3.10+ gerekli
python --version

# MCP SDK'yı yükle
pip install mcp

# aiohttp kütüphanesini yükle (HTTP istekleri için)
pip install aiohttp
```

## 🚀 Kurulum

### 1. Claude Desktop Yapılandırması

Claude Desktop yapılandırma dosyasını düzenleyin:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux/Mac:**
```
~/.config/Claude/claude_desktop_config.json
```

### 2. Yapılandırma Dosyasına Ekle

```json
{
  "mcpServers": {
    "textgen-webui": {
      "command": "python",
      "args": [
        "C:\\Users\\mcgus\\Documents\\depo\\textgen_webui_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Önemli:**
- Dosya yolunu kendi sisteminize göre değiştirin
- Windows'ta çift backslash (`\\`) kullanın
- `PYTHONUNBUFFERED=1` Python'un çıktıyı buffer'lamadan göndermesini sağlar

### 3. Claude Desktop'ı Yeniden Başlat

Yapılandırma değişikliklerinin geçerli olması için Claude Desktop'ı tamamen kapatıp yeniden açın.

## 💡 Kullanım

### İlk Bağlantı

Claude Desktop'ta önce bağlantı ayarlarını yapılandırın:

```
Text-generation-webui bağlantısını ayarla: http://127.0.0.1:5000
```

veya API key ile:

```
Text-generation-webui'ye bağlan, URL: http://127.0.0.1:5000, API key: your-api-key-here
```

### Modelleri Listele

```
Text-generation-webui'de hangi modeller yüklü?
```

### Model ile Sohbet

```
Fine-tune ettiğim modele şunu sor: "Python'da liste comprehension nasıl kullanılır?"
```

### Metin Tamamlama

```
Bu metni tamamla: "Yapay zeka ve makine öğrenmesi"
```

### Model Bilgisi

```
Şu anda hangi model aktif?
```

## 🛠️ Mevcut Araçlar (Tools)

| Tool | Açıklama | Parametreler |
|------|----------|-------------|
| `set_textgen_config` | Bağlantı ayarları | `base_url`, `api_key` (opsiyonel) |
| `list_models` | Yüklü modelleri listele | - |
| `chat_completion` | Chat formatında sohbet | `messages`, `max_tokens`, `temperature`, `top_p` |
| `text_completion` | Basit metin tamamlama | `prompt`, `max_tokens`, `temperature`, `top_p`, `stop` |
| `get_model_info` | Aktif model bilgisi | - |

## 🔧 Hata Ayıklama

### MCP server loglarını görme

MCP sunucusu tüm logları `stderr`'e yazar. Claude Desktop Developer Console'da görebilirsiniz:

**Windows:** `Ctrl + Shift + i`
**Mac:** `Cmd + Option + Shift + i`

Console'da şöyle loglar göreceksiniz:
```
[TEXTGEN-MCP] INFO: Text-generation-webui MCP Server başlatılıyor...
[TEXTGEN-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
[TEXTGEN-MCP] INFO: Tool çağrıldı: chat_completion with args: {...}
```

### Yaygın Hatalar

#### ❌ "Bağlantı ayarlandı ama sunucuya ulaşılamadı"

**Çözüm:**
1. Text-generation-webui'nin çalıştığından emin olun
2. `--api` bayrağı ile başlattığınızdan emin olun
3. Portu kontrol edin (varsayılan 5000)
4. Web tarayıcısında `http://127.0.0.1:5000/docs` adresini açıp API dokümantasyonunun görüntülendiğini kontrol edin

#### ❌ "mcp paketi bulunamadı"

**Çözüm:**
```bash
pip install mcp
```

#### ❌ "aiohttp bulunamadı"

**Çözüm:**
```bash
pip install aiohttp
```

#### ❌ "HTTP 404 Not Found"

**Çözüm:**
Text-generation-webui'nin OpenAI-compatible API'si aktif değil. `--api` bayrağı ile yeniden başlatın.

## 📝 Örnek Kullanım Senaryoları

### 1. Fine-tune edilmiş model ile sohbet

```
Claude: Text-generation-webui'ye bağlan: http://127.0.0.1:5000
Claude: Fine-tune ettiğim modele şunu sor: "Türkçe dilbilgisi kuralları nelerdir?"
```

### 2. Kod üretimi

```
Claude: Modelime Python'da REST API örneği yaz diye sor, max_tokens 1000 olsun
```

### 3. Metin tamamlama

```
Claude: Bu hikayeyi tamamla: "Karanlık bir gecede, ormanın derinliklerinde..."
```

### 4. Özel parametrelerle oluşturma

```
Claude: Çok yaratıcı bir hikaye üret, temperature 1.2 olsun
```

## 🎛️ Parametre Ayarları

### Temperature (Yaratıcılık)
- **0.0-0.3**: Çok deterministik, tutarlı sonuçlar
- **0.7-0.9**: Dengeli yaratıcılık (varsayılan)
- **1.0-2.0**: Çok yaratıcı, beklenmedik sonuçlar

### Top_p (Nucleus Sampling)
- **0.1-0.5**: Daha muhafazakar seçimler
- **0.9**: Dengeli (varsayılan)
- **1.0**: Tüm olası token'ları değerlendir

### Max_tokens
- Üretilecek maksimum token sayısı
- Varsayılan: 512
- Daha uzun metinler için artırın (örn: 1000, 2000)

## 🔐 API Anahtarı Kullanımı

Text-generation-webui'yi API key ile başlattıysanız:

```cmd
python server.py --api --api-key my-secret-key
```

Claude'a şöyle söyleyin:
```
Text-generation-webui'ye bağlan, URL: http://127.0.0.1:5000, API key: my-secret-key
```

## 📚 Ek Kaynaklar

- [Text-generation-webui GitHub](https://github.com/oobabooga/text-generation-webui)
- [Text-generation-webui OpenAI API Dokümantasyonu](https://github.com/oobabooga/text-generation-webui/blob/main/docs/12%20-%20OpenAI%20API.md)
- [MCP SDK Dokümantasyonu](https://modelcontextprotocol.io)

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

## 📄 Lisans

MIT

## 🆘 Destek

Sorun yaşıyorsanız:
1. Developer Console'daki logları kontrol edin (`Ctrl+Shift+i`)
2. Text-generation-webui'nin API dokümantasyonunu kontrol edin: `http://127.0.0.1:5000/docs`
3. Server'ı elle çalıştırıp hata olup olmadığını görün:
   ```bash
   python textgen_webui_mcp_server.py
   ```
4. Issue açın veya yardım isteyin

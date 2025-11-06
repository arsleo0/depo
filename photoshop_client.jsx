/*
 * Photoshop MCP Client - Photoshop içinde çalışan script
 * Python MCP sunucusuyla socket üzerinden haberleşir
 *
 * Kullanım: Photoshop içinde File > Scripts > Browse... ve bu dosyayı seçin
 * Veya: File > Scripts > photoshop_client.jsx (eğer Scripts klasörüne kopyaladıysanız)
 */

// Socket bağlantısı (basitleştirilmiş - gerçek implementasyon için BridgeTalk kullanın)
var SERVER_PORT = 49494;

// Komutları işleyen fonksiyonlar
var commandHandlers = {
    open_file: function(params) {
        var file = new File(params.filepath);
        if (file.exists) {
            app.open(file);
            return { success: true, message: "Dosya açıldı: " + params.filepath };
        } else {
            return { success: false, message: "Dosya bulunamadı: " + params.filepath };
        }
    },

    save_file: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;

        if (params.filepath) {
            var file = new File(params.filepath);
            doc.saveAs(file);
            return { success: true, message: "Dosya kaydedildi: " + params.filepath };
        } else {
            doc.save();
            return { success: true, message: "Dosya kaydedildi" };
        }
    },

    get_document_info: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;
        var info = {
            name: doc.name,
            width: doc.width.value,
            height: doc.height.value,
            resolution: doc.resolution,
            colorMode: doc.mode.toString(),
            bitDepth: doc.bitsPerChannel.toString(),
            layerCount: doc.layers.length,
            saved: doc.saved,
            path: doc.fullName ? doc.fullName.fsName : "Kaydedilmemiş"
        };

        return {
            success: true,
            message: "Doküman bilgileri alındı",
            data: info
        };
    },

    create_layer: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;
        var layer;

        if (params.type === "text") {
            layer = doc.artLayers.add();
            layer.kind = LayerKind.TEXT;
        } else {
            layer = doc.artLayers.add();
        }

        if (params.name) {
            layer.name = params.name;
        }

        return { success: true, message: "Katman oluşturuldu: " + layer.name };
    },

    delete_layer: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;

        if (params.layer_name) {
            try {
                var layer = doc.layers.getByName(params.layer_name);
                layer.remove();
                return { success: true, message: "Katman silindi: " + params.layer_name };
            } catch (e) {
                return { success: false, message: "Katman bulunamadı: " + params.layer_name };
            }
        } else {
            if (doc.activeLayer) {
                var layerName = doc.activeLayer.name;
                doc.activeLayer.remove();
                return { success: true, message: "Aktif katman silindi: " + layerName };
            } else {
                return { success: false, message: "Silinecek katman yok" };
            }
        }
    },

    list_layers: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;
        var layers = [];

        for (var i = 0; i < doc.layers.length; i++) {
            layers.push({
                name: doc.layers[i].name,
                visible: doc.layers[i].visible,
                opacity: doc.layers[i].opacity,
                kind: doc.layers[i].kind ? doc.layers[i].kind.toString() : "LayerSet"
            });
        }

        return {
            success: true,
            message: "Katmanlar listelendi (" + layers.length + " adet)",
            data: layers
        };
    },

    resize_image: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;
        doc.resizeImage(
            UnitValue(params.width, "px"),
            UnitValue(params.height, "px")
        );

        return {
            success: true,
            message: "Görsel boyutlandırıldı: " + params.width + "x" + params.height
        };
    },

    apply_filter: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;

        try {
            if (params.filter === "blur") {
                doc.activeLayer.applyBlur();
            } else if (params.filter === "sharpen") {
                doc.activeLayer.applySharpen();
            } else if (params.filter === "gaussianBlur") {
                doc.activeLayer.applyGaussianBlur(5.0);
            } else {
                return { success: false, message: "Bilinmeyen filtre: " + params.filter };
            }

            return { success: true, message: "Filtre uygulandı: " + params.filter };
        } catch (e) {
            return { success: false, message: "Filtre uygulanamadı: " + e.message };
        }
    },

    run_jsx: function(params) {
        try {
            var result = eval(params.code);
            return {
                success: true,
                message: "JSX kodu çalıştırıldı",
                data: result ? result.toString() : "undefined"
            };
        } catch (e) {
            return { success: false, message: "JSX hatası: " + e.message };
        }
    },

    export: function(params) {
        if (app.documents.length === 0) {
            return { success: false, message: "Açık doküman yok" };
        }

        var doc = app.activeDocument;
        var file = new File(params.filepath);

        try {
            if (params.format === "PNG") {
                var pngOptions = new PNGSaveOptions();
                doc.saveAs(file, pngOptions, true);
            } else if (params.format === "JPEG") {
                var jpegOptions = new JPEGSaveOptions();
                jpegOptions.quality = params.quality || 10;
                doc.saveAs(file, jpegOptions, true);
            } else if (params.format === "TIFF") {
                var tiffOptions = new TiffSaveOptions();
                doc.saveAs(file, tiffOptions, true);
            } else if (params.format === "PDF") {
                var pdfOptions = new PDFSaveOptions();
                doc.saveAs(file, pdfOptions, true);
            } else {
                return { success: false, message: "Desteklenmeyen format: " + params.format };
            }

            return {
                success: true,
                message: "Dışa aktarıldı: " + params.filepath + " (" + params.format + ")"
            };
        } catch (e) {
            return { success: false, message: "Dışa aktarma hatası: " + e.message };
        }
    }
};

// Ana fonksiyon - komut dosyası çalıştırıldığında
function main() {
    alert("Photoshop MCP Client Başlatıldı!\n\n" +
          "Bu script Photoshop'u Claude Desktop ile entegre eder.\n\n" +
          "Not: Socket iletişimi basitleştirilmiş versiyondur.\n" +
          "Tam özellikli kullanım için manuel olarak JSX komutlarını çalıştırabilirsiniz.");

    // Örnek kullanım: Doküman bilgilerini göster
    if (app.documents.length > 0) {
        var result = commandHandlers.get_document_info({});
        if (result.success) {
            var info = result.data;
            alert("Aktif Doküman:\n" +
                  "Ad: " + info.name + "\n" +
                  "Boyut: " + info.width + " x " + info.height + "\n" +
                  "Çözünürlük: " + info.resolution + " ppi\n" +
                  "Katman sayısı: " + info.layerCount);
        }
    } else {
        alert("Açık doküman yok. Bir PSD dosyası açın veya yeni bir doküman oluşturun.");
    }
}

// Tek bir komutu test etmek için bu fonksiyonu kullanın
function testCommand(commandName, params) {
    if (commandHandlers[commandName]) {
        var result = commandHandlers[commandName](params);
        alert(JSON.stringify(result, null, 2));
        return result;
    } else {
        alert("Bilinmeyen komut: " + commandName);
        return { success: false, message: "Bilinmeyen komut" };
    }
}

// Script'i çalıştır
main();

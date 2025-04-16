#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "SPIFFS.h"  // Pour enregistrer les résultats JSON dans un fichier

// Informations Wi-Fi
const char *ssid = "iPhone de Auxence";
const char *password = "auxence2701";

// Informations API YouTube
const char* apiKey = "";
const char* searchQuery = "cats";
const int maxResults = 5;

// Définition du bouton pour déconnexion
int btnGPIO = 0;
int btnState = false;

// Fonction pour sauvegarder les résultats en JSON
void saveJSON(String jsonData) {
    File file = SPIFFS.open("/youtube_results.json", FILE_WRITE);
    if (!file) {
        Serial.println("Erreur: Impossible d'ouvrir le fichier JSON pour écrire.");
        return;
    }
    file.print(jsonData);
    file.close();
    Serial.println("Les résultats ont été enregistrés dans youtube_results.json !");
}

// Fonction pour effectuer la requête YouTube
void fetchYouTubeResults() {
    Serial.println("Recherche YouTube en cours...");

    String url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + 
                 String(searchQuery) + "&maxResults=" + String(maxResults) + "&key=" + String(apiKey);

    HTTPClient http;
    http.begin(url);
    int httpCode = http.GET();

    if (httpCode > 0) {
        String payload = http.getString();
        Serial.println("Réponse reçue !");

        // Parser le JSON
        StaticJsonDocument<8192> doc;
        DeserializationError error = deserializeJson(doc, payload);
        if (error) {
            Serial.print("Erreur JSON: ");
            Serial.println(error.f_str());
            return;
        }

        // Création du fichier JSON avec les résultats
        StaticJsonDocument<8192> outputDoc;
        JsonArray videoArray = outputDoc.createNestedArray("videos");

        Serial.println("\nRésultats de la recherche:");
        for (JsonObject item : doc["items"].as<JsonArray>()) {
            String title = item["snippet"]["title"].as<String>();
            String videoId = item["id"]["videoId"].as<String>();
            String videoUrl = "https://www.youtube.com/watch?v=" + videoId;

            Serial.println(title + " - " + videoUrl);

            // Ajouter à la structure JSON
            JsonObject videoObject = videoArray.createNestedObject();
            videoObject["title"] = title;
            videoObject["url"] = videoUrl;
        }

        // Sauvegarde des résultats en JSON sur SPIFFS
        String jsonOutput;
        serializeJson(outputDoc, jsonOutput);
        saveJSON(jsonOutput);

    } else {
        Serial.print("Erreur HTTP: ");
        Serial.println(httpCode);
    }

    http.end();
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    // Initialisation SPIFFS pour stockage JSON
    if (!SPIFFS.begin(true)) {
        Serial.println("Erreur d'initialisation de SPIFFS !");
        return;
    }

    // Configuration du bouton
    pinMode(btnGPIO, INPUT);

    // Connexion au Wi-Fi
    Serial.println();
    Serial.print("[WiFi] Connexion à ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    int tryDelay = 500;
    int numberOfTries = 20;

    while (true) {
        switch (WiFi.status()) {
            case WL_NO_SSID_AVAIL: Serial.println("[WiFi] SSID introuvable"); break;
            case WL_CONNECT_FAILED: Serial.println("[WiFi] Échec de connexion"); return; break;
            case WL_CONNECTION_LOST: Serial.println("[WiFi] Connexion perdue"); break;
            case WL_DISCONNECTED: Serial.println("[WiFi] WiFi déconnecté"); break;
            case WL_CONNECTED:
                Serial.println("[WiFi] Connexion réussie !");
                Serial.print("[WiFi] Adresse IP: ");
                Serial.println(WiFi.localIP());
                fetchYouTubeResults();  // Lance la recherche YouTube après connexion
                return;
            default:
                Serial.print("[WiFi] État: ");
                Serial.println(WiFi.status());
                break;
        }
        delay(tryDelay);

        if (numberOfTries <= 0) {
            Serial.println("[WiFi] Échec de connexion !");
            WiFi.disconnect();
            return;
        } else {
            numberOfTries--;
        }
    }
}

void loop() {
    // Vérification du bouton pour déconnexion
    btnState = digitalRead(btnGPIO);

    if (btnState == LOW) {
        Serial.println("[WiFi] Déconnexion du Wi-Fi !");
        if (WiFi.disconnect(true, false)) {
            Serial.println("[WiFi] Déconnecté !");
        }
        delay(1000);
    }

    delay(1000);
}


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

typedef struct {
    char* data;
    size_t size;
} Response;

static size_t write_callback(void* ptr, size_t size, size_t nmemb, Response* resp) {
    size_t total = size * nmemb;
    resp->data = realloc(resp->data, resp->size + total + 1);
    memcpy(resp->data + resp->size, ptr, total);
    resp->size += total;
    resp->data[resp->size] = '\0';
    return total;
}

char* fetch_url(const char* url, int* success) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        *success = 0;
        return strdup("Failed to initialize curl");
    }

    Response resp = {malloc(1), 0};
    resp.data[0] = '\0';

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &resp);

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    *success = (res == CURLE_OK);
    if (res != CURLE_OK) {
        free(resp.data);
        return strdup(curl_easy_strerror(res));
    }
    return resp.data;
}

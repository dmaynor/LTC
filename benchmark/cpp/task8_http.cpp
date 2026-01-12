#include <string>
#include <curl/curl.h>

struct FetchResult {
    bool success;
    std::string body;
};

static size_t write_callback(char* ptr, size_t size, size_t nmemb, std::string* data) {
    data->append(ptr, size * nmemb);
    return size * nmemb;
}

FetchResult fetch_url(const std::string& url) {
    CURL* curl = curl_easy_init();
    if (!curl)
        return {false, "Failed to initialize curl"};

    std::string response;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK)
        return {false, curl_easy_strerror(res)};

    return {true, response};
}

function [success, body] = fetch_url(url)
    try
        body = webread(url);
        success = true;
    catch e
        success = false;
        body = e.message;
    end
end

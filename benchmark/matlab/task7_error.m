function [success, value, error] = parse_int(s)
    value = str2double(s);
    if isnan(value) || floor(value) ~= value
        success = false;
        value = 0;
        error = 'Invalid integer format';
    else
        success = true;
        value = int32(value);
        error = '';
    end
end

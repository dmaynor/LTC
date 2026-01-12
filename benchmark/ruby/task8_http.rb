require 'net/http'
require 'uri'

def fetch_url(url)
  uri = URI.parse(url)
  response = Net::HTTP.get_response(uri)
  { success: true, body: response.body }
rescue => e
  { success: false, error: e.message }
end

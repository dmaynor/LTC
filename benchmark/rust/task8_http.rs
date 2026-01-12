use std::io::Read;

fn fetch_url(url: &str) -> Result<String, Box<dyn std::error::Error>> {
    let response = ureq::get(url).call()?;
    let body = response.into_string()?;
    Ok(body)
}

import aiohttp

async def req(basket, coupon_code):
    url = f"https://checkout.tebex.io/api/baskets/{basket}/coupons/"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    
    data = {"couponCode": coupon_code}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                # Instead of raising an error for non-200 status codes, just check the status
                status_code = response.status
                try:
                    response_data = await response.json()
                    output = (coupon_code, response_data)
                except Exception:
                    output = "Error: Response body is not in JSON format."
                    
        except aiohttp.ClientError as error:
            output = ("Error:", error)

    return output



import requests, json, math
from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error
import logging

app = Flask(__name__)

baseurl = "https://api.yelp.com/v3/businesses/search"

@app.route("/map")
def map(address):
    params = {}
    baseurl = "https://www.google.com/maps/embed/v1/place"
    params['q'] = address
    params['key'] = "AIzaSyAy-E7Hnxze1LAVDvhJmW2oHxfseUXIbEQ"
    url = baseurl + "?" + urllib.parse.urlencode(params)
    #return render_template('pricelist.html', url=url)
    return url

@app.route("/")
def main_handler():
    app.logger.info("")
    return render_template('searchCity.html')

@app.route("/response")
def response_handler():
    city = request.args.get('city')
    app.logger.info(city)
    getprice = request.args.getlist('getprice')
    if city:
        price = ""
        if "1" in getprice:
            price += "1"
            if len(getprice) > 1:
                price += ", "
        if "2" in getprice:
            price += "2"
            if "1" not in getprice:
                getprice.append("")
        if len(getprice) > 2:
            price += ", "
        if "3" in getprice:
            price += "3"
        food = best_shop(term="food", location=city, price=price)
        restaurant = best_shop(term="restaurants", location=city, price=price)
        dessert = best_shop(term="dessert", location=city, price=price)
        drinks = best_shop(term="drinks", location=city, price=price)
        activity = best_shop(term="activities", location=city, price=price)
        title = "Top 5 Places to Visit in " + city
        return render_template('bestlist.html', title=title, food=food, restaurant=restaurant, dessert=dessert, drinks=drinks, activity=activity)
    else:
        title = "City Search Error"
        return render_template('bestlist.html', title=title)


baseurl = "https://api.yelp.com/v3/businesses/search"
def get_shops(location = "", radius = 16000, term = "", limit = 20, price = "", api_key = "C7mDFaAms-ANWBY6RNRNHbZcoOV024SjHsNLfMLnn0L_zQp3eGGhCGPqeEeEhGDfIzRz6PKACiyExV_Ffg736Bs_9NjMMhcmAEabW_tZWFz11egieQtHuLfLZMa1X3Yx"):
    shops = {}
    key = {'Authorization': 'Bearer %s' % api_key}
    shops['location'] = location
    shops['radius'] = radius
    shops['term'] = term
    shops['limit'] = limit
    shops['price'] = price
    req = requests.get(baseurl, params = shops, headers = key)
    allshops = json.loads(req.text)
    return allshops

def best_shop(term = "", location = "", price = ""):
    shops = get_shops(term = term, location = location, price = price)
    best = {'name': "", 'rating': 0}
    for shop in shops['businesses']:
        if shop['rating'] >= best['rating']:
            best['name'] = shop['name']
            best['rating'] = (float(shop['rating']) / 5.0) * 100.0
            best['price'] = shop['price']
            best['location'] = shop['location']
            best['url'] = shop['url']
            best['phone'] = shop['phone']
            address = shop['location']['address1'] + shop['location']['city'] + shop['location']['state'] + shop['location']['zip_code']
            best['map'] = map(address)
    return best

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)# plannerocity

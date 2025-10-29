// Execute next lines in the browser console in the Game page on GOG
var products = document.getElementsByClassName("product-row");
var res = {};
for(i = 0; i<products.length; i++) {
    res[products[i].getAttribute("gog-account-product")] = products[i].querySelector(".product-title__text").innerHTML;
};
res;

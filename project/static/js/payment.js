// zmena ukazovatela celkovej ceny v payment.html
var orderPrice = document.getElementById("orderPrice")
const originalPrice = parseFloat(orderPrice.innerHTML)
var prevDel = 0;
var prevPay = 0;


var delivery_radios = document.getElementsByClassName("deliveryTypes");
for (let index = 0; index < delivery_radios.length; index++) {
    let element = delivery_radios[index];
    element.addEventListener("change", function() {
        var val = parseFloat(element.value);
        changePrice(val, prevDel);
        prevDel = val;
    });
    
}

var pay_radios = document.getElementsByClassName("payTypes");
for (let index = 0; index < pay_radios.length; index++) {
    let element = pay_radios[index];
    element.addEventListener("change", function() {
        var val = parseFloat(element.value);
        changePrice(val, prevPay);
        prevPay = val;
    });
    
}


function changePrice(new_amount, reduce) {
    //var thePrice = originalPrice;
    var thePrice = parseFloat(orderPrice.innerHTML);
    thePrice += new_amount;
    thePrice -= reduce;
    orderPrice.innerHTML = thePrice.toFixed(2);
}


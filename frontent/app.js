// FastAPI server ka URL (local)
var BASE_URL = "http://127.0.0.1:8000";

function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for (var i = 0; i < uiBathrooms.length; i++) {
        if (uiBathrooms[i].checked) {
            return parseInt(uiBathrooms[i].value);
        }
    }
    return -1;
}

function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for (var i = 0; i < uiBHK.length; i++) {
        if (uiBHK[i].checked) {
            return parseInt(uiBHK[i].value);
        }
    }
    return -1;
}

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");

    var sqft = parseFloat(document.getElementById("uiSqft").value);
    var bhk = getBHKValue();
    var bath = getBathValue();
    var location = document.getElementById("uiLocations").value;
    var estPrice = document.getElementById("uiEstimatedPrice");

    // FastAPI me JSON body bhejte hain (Flask me form data tha)
    $.ajax({
        url: BASE_URL + "/predict_home_price",
        type: "POST",
        contentType: "application/json",   // ← important FastAPI ke liye
        data: JSON.stringify({
            total_sqft: sqft,
            bhk: bhk,
            bath: bath,
            location: location
        }),
        success: function (data) {
            console.log("Estimated price:", data.estimated_price);
            estPrice.innerHTML = "<h2>" + data.estimated_price + " Lakh</h2>";
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseText);
            estPrice.innerHTML = "<h2>Error! Check console.</h2>";
        }
    });
}

function onPageLoad() {
    console.log("document loaded");

    $.get(BASE_URL + "/get_location_names", function (data) {
        console.log("Locations loaded");
        if (data && data.locations) {
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            // Default option
            $('#uiLocations').append('<option value="" disabled selected>Choose a Location</option>');
            $.each(data.locations, function (i, loc) {
                $('#uiLocations').append(new Option(loc, loc));
            });
        }
    });
}

window.onload = onPageLoad;
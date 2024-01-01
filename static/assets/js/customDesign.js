projecturl = "http://127.0.0.1:8000/";
//projecturl = "http://furydgp.com/";

let canvas = new fabric.Canvas('tshirt-canvas-front');
let canvasBack = new fabric.Canvas('tshirt-canvas-back');

let canvasStates = [];
let currentStateIndex = -1;

// Function to save the current state of the canvas
function saveCanvasState() {
    currentStateIndex++;
    if (currentStateIndex < canvasStates.length) {
        canvasStates = canvasStates.slice(0, currentStateIndex);
    }
    canvasStates.push(JSON.stringify(activecanvas));
}

// Function to undo the last action on the canvas
function undo() {
    console.log("undo");
    if (currentStateIndex > 0) {
        console.log("undo inside");
        currentStateIndex--;
        activecanvas.clear();
        activecanvas.loadFromJSON(canvasStates[currentStateIndex], function () {
            activecanvas.renderAll();
        });
    }
}

// Function to redo the undone action on the canvas
function redo() {
    console.log("redo");
    if (currentStateIndex < canvasStates.length - 1) {
        console.log("redo inside");
        currentStateIndex++;
        activecanvas.clear();
        activecanvas.loadFromJSON(canvasStates[currentStateIndex], function () {
            activecanvas.renderAll();
        });
    }
}



//fuction to change color
function changeColor(color) {
    document.getElementById("tshirt-div").style.backgroundColor = color;
    document.getElementById("tshirt-div-back").style.backgroundColor = color;
}

//change image src function with name changetshirt
function changetshirt(front,back){
    // front=tshirtImage;
    // // replace "front" with "back" in tshirtImage
    // back=tshirtImage.replace("front","back");
    document.getElementById("tshirt-backgroundpicture").src = front;
    document.getElementById("tshirt-backgroundpicture-back").src = back;
}
let activecanvas=canvas;

document.querySelectorAll(".product-tab-info-link").forEach(function(button) {
    button.addEventListener("click", function() {
        if (this.getAttribute("data-bs-target") === "#nav-description") {
            console.log("Front tab is active");
            activecanvas=canvas;
        } else if (this.getAttribute("data-bs-target") === "#nav-additional-information") {
            console.log("Back tab is active");
            activecanvas=canvasBack;
        }
    });
});




//function to add text
function addText(){
    var message = document.getElementById("text-input").value;
    var text = new fabric.Text(message, {
        left: 100,
        top: 100,
        // arial
        fontFamily: 'Arial' ,
        fill: '#000000',
        fontSize: 20,
        lockUniScaling: true // disable uniform scaling
    });
    activecanvas.add(text);
    activecanvas.setActiveObject(text);
    text.bringToFront();
    document.getElementById("text-input").value="";
    
    // save canvas state
    saveCanvasState();

}

//put selected text in input
canvas.on('selection:created', function(options) {
    document.getElementById("text-input").value=options.target.text;
});

// unset input when no text is selected
canvas.on('selection:cleared', function(options) {
    document.getElementById("text-input").value="";
});

canvasBack.on('selection:created', function(options) {
    document.getElementById("text-input").value=options.target.text;
});

// unset input when no text is selected
canvasBack.on('selection:cleared', function(options) {
    document.getElementById("text-input").value="";
});

// on select object set it in his layer not bring it to front
canvas.on('object:selected', function(options) {
    options.target.bringToFront = false;
});


// on add object on canvas update canvas state
canvas.on('object:added', function(options) {
    // save canvas state
    saveCanvasState();
});

// on remove object on canvas update canvas state
canvas.on('object:removed', function(options) {
    // save canvas state
    saveCanvasState();
});

// on move object on canvas update canvas state
canvas.on('object:moving', function(options) {
    // save canvas state
    saveCanvasState();
});




// text-input onkeyup change text
document.getElementById("text-input").onkeyup = function() {
    //check if text is selected
    if(activecanvas.getActiveObject()){
        activecanvas.getActiveObject().set("text", this.value);
        activecanvas.renderAll();
    }
};



//function to change font family
function changeFontFamily(fontFamily){
    activecanvas.getActiveObject().set("fontFamily", fontFamily);
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}

//function to change font size
function changeFontSize(fontSize){
    activecanvas.getActiveObject().set("fontSize", fontSize);
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}

//function to change font color
function changeFontColor(fontColor){
    activecanvas.getActiveObject().set("fill", fontColor);
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}
// change border color  
function changeBorderColor(borderColor){
    activecanvas.getActiveObject().set("stroke", borderColor);
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}

function changeShadowColor(shadowColor) {
    var activeObject = canvas.getActiveObject();
    if (activeObject && shadowColor) {
        var shadow = activeObject.getShadow();
        shadow.color = shadowColor;
        activeObject.setShadow(shadow);
        activecanvas.renderAll();
    }

    // save canvas state
    saveCanvasState();
}



//function to change font style
function changeFontStyle(fontStyle){
    activecanvas.getActiveObject().set("fontStyle", fontStyle);
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}

// change border color  
function changeBorderColor(borderColor){
    activecanvas.getActiveObject().set("stroke", borderColor);
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();

}

//function to change text leter space
function changeTextLetterSpace(textLetterSpace){
    activecanvas.getActiveObject().set("charSpacing", textLetterSpace);
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}

// function to change text to bold and unbold
function changeBold(){
    var isBold = activecanvas.getActiveObject().get("fontWeight") == "bold";
    activecanvas.getActiveObject().set("fontWeight", isBold ? "normal" : "bold");
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}

// function to change text to italic and unitalic
function changeItalic(){
    var isItalic = activecanvas.getActiveObject().get("fontStyle") == "italic";
    activecanvas.getActiveObject().set("fontStyle", isItalic ? "normal" : "italic");
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}
// change changeUnderline
function changeUnderline(){
    var isUnderline = activecanvas.getActiveObject().get("underline") == "underline";
    activecanvas.getActiveObject().set("underline", isUnderline ? "" : "underline");
    activecanvas.renderAll();

    // save canvas state
    saveCanvasState();
}
// function to change text stroke width with 
function changeStrokeWidth(strokeWidth){
    strokeWidth = parseInt(strokeWidth, 10) || 1;
    activecanvas.getActiveObject().set("strokeWidth", strokeWidth);
    activecanvas.renderAll();
    
    // save canvas state
    saveCanvasState();
}


// design_resource []
var design_resource=[]


function addImage(imageURL) {
    fabric.Image.fromURL(imageURL, function (img) {
        // Set image width and height to 200px
        img.scaleToWidth(600);
        img.scaleToHeight(200);

        // Adjust top and left to center the image vertically
        img.set({
            top: (activecanvas.height - img.height * img.scaleY) / 2,
            left: (activecanvas.width - img.width * img.scaleX) / 2
        });
        // Add image to canvas
        activecanvas.add(img);
        // Save canvas state
        saveCanvasState();

        
    });
}

function scaleImageToFitCanvas(image, canvas) {
    var canvasAspectRatio = canvas.width / canvas.height;
    var imageAspectRatio = image.width / image.height;
    var scaleRatio;

    // Determine the scale ratio to maintain aspect ratio
    if (imageAspectRatio > canvasAspectRatio) {
        // Image is wider than canvas
        scaleRatio = canvas.width / image.width;
    } else {
        // Image is taller than canvas
        scaleRatio = canvas.height / image.height;
    }

    // Apply the scale ratio to the image
    image.scale(scaleRatio);

    // Center the image on the canvas
    image.set({
        left: (canvas.width - image.width * scaleRatio) / 2,
        top: (canvas.height - image.height * scaleRatio) / 2
    });
}


// COPY , cut , paste functions 
function copy(){
    activecanvas.getActiveObject().clone(function(cloned) {
        _clipboard = cloned;
    });
}

function cut() {
    var activeObject = activecanvas.getActiveObject();
    if (activeObject) {
        activeObject.clone(function(cloned) {
            _clipboard = cloned;
        });
        activecanvas.remove(activeObject);
        activecanvas.discardActiveObject();
        activecanvas.renderAll();
    }
}

function paste(){
    _clipboard.clone(function(clonedObj) {
        activecanvas.discardActiveObject();
        clonedObj.set({
            left: clonedObj.left + 10,
            top: clonedObj.top + 10,
            evented: true,
        });
        if (clonedObj.type === 'activeSelection') {
            clonedObj.canvas = activecanvas;
            clonedObj.forEachObject(function(obj) {
                activecanvas.add(obj);
            });
            clonedObj.setCoords();
        } else {
            activecanvas.add(clonedObj);
        }
        _clipboard.top += 10;
        _clipboard.left += 10;
        activecanvas.setActiveObject(clonedObj);
        activecanvas.requestRenderAll();
    });
}


//brind forward
function bringForward() {
    var activeObject = activecanvas.getActiveObject();
    console.log(activeObject);
    if (activeObject) {
        
        activecanvas.bringForward(activeObject);
        // unselect object
        activecanvas.discardActiveObject();
        
        // save canvas state
        saveCanvasState();
    }

    
}

//send backward
function sendBackwards() {
    var activeObject = activecanvas.getActiveObject();
    if (activeObject) {
        activecanvas.sendBackwards(activeObject);

        // unselect object
        activecanvas.discardActiveObject();

        // save canvas state
        saveCanvasState();
    }
}


// copy , paste , cut shortcut
document.addEventListener("keydown", function(e) {
    var keyCode = e.keyCode;
    if (e.ctrlKey && keyCode === 67) {
        copy();
    } else if (e.ctrlKey && keyCode === 86) {
        paste();
    } else if (e.ctrlKey && keyCode === 88) {
        cut();
    }else if (e.ctrlKey && keyCode === 90) {
        undo();
    }else if (e.ctrlKey && keyCode === 89) {
        redo();
    }else if (e.ctrlKey && keyCode === 38) {
        bringForward();
    }else if (e.ctrlKey && keyCode === 40) {
        sendBackwards();
    }
}, false);






// When the user clicks on upload a custom picture
document.getElementById('tshirt-custompicture').addEventListener("change", function(e){
    var reader = new FileReader();
    
    console.log("change");
    reader.onload = function (event){
        var imgObj = new Image();
        imgObj.src = event.target.result;

        // When the picture loads, create the image in Fabric.js
        imgObj.onload = function () {
            var img = new fabric.Image(imgObj);
            scaleImageToFitCanvas(img, activecanvas);
        
            activecanvas.centerObject(img);
            activecanvas.add(img);
            activecanvas.renderAll();
        
            
        };
    };

    // If the user selected a picture, load it
    if(e.target.files[0]){
        reader.readAsDataURL(e.target.files[0]);
    }
}, false);







// When the user selects a picture that has been added and press the DEL key
// The object will be removed !
document.addEventListener("keydown", function(e) {
    var keyCode = e.keyCode;
    
    // delete on DEL key or backspace key
    if(keyCode == 46){
        var activeObject = activecanvas.getActiveObject();

        if (activeObject) {
            // Remove the active object from the canvas
            activecanvas.remove(activeObject);
        }
    }
}, false);




var front_design_price= document.getElementById("front_design_price");
var back_design_price= document.getElementById("back_design_price");
var product_size= document.getElementById("product_size");
var quantity_price = document.getElementById("quantity_price");
document.getElementById("Quote_Buy_tab").addEventListener("click", function() {
    // get pruduct height from input with id "product_height"
    var productHeightByInches = document.getElementById("product_height").value;
    // get product height in screen by pixels
    var productHeightByPixels = document.getElementById("tshirt-div").offsetHeight;
    // check if productHeightByPixels is 0 get tshirt-div-back
    if (productHeightByPixels == 0) {
        productHeightByPixels = document.getElementById("tshirt-div-back").offsetHeight;
    }
    // calculate scale
    var scale = productHeightByPixels / productHeightByInches;
    // get front design height on screen
    // get the objects on the canvas
    var frontObjects = canvas.getObjects();
    var backObjects = canvasBack.getObjects();
    // calculate total height for front canvas
    var frontDesignHeight = calculateTotalArea(frontObjects);
    // calculate total height for back canvas
    var backDesignHeight = calculateTotalArea(backObjects);
    // calculate front design height by inches
    var frontDesignHeightByInches = frontDesignHeight / scale;
    // calculate back design height by inches
    var backDesignHeightByInches = backDesignHeight / scale;

    frontDesignHeightByInches = Math.round(frontDesignHeightByInches);
    backDesignHeightByInches = Math.round(backDesignHeightByInches);

    // set front_design_price to frontDesignHeightByInches
    front_design_price.innerHTML = frontDesignHeightByInches;
    // set back_design_price to backDesignHeightByInches
    back_design_price.innerHTML = backDesignHeightByInches;
    // get all  SizeItem 
    var SizeItem = document.querySelectorAll(".SizeItem");
    // loop through all SizeItem
    var totalSizePrice = 0;
    var quality = 0;
    var size = [];
    SizeItem.forEach(function(SizeItem) {
        // get data-size-price
        var SizeItemPrice = SizeItem.getAttribute("data-size-price");
        // get data-size
        var SizeItemSize = SizeItem.getAttribute("data-size-symbol");
        var SizeItemNumber = SizeItem.getElementsByTagName("input")[0].value;
        // check if SizeItemInput is null
        if (SizeItemNumber == "") {
            // set SizeItemInput to 0
            SizeItemNumber = 0;
        }
        // create object size with size and number
        size.push({symbol:SizeItemSize,quality:SizeItemNumber});
        // set quality to 
        quality = Number(SizeItemNumber) + quality;
        // calculate totalSizePrice
        totalSizePrice += SizeItemPrice * SizeItemNumber;
        
    });

    // call getQuote function
    getQuote(frontDesignHeightByInches, backDesignHeightByInches, quality,totalSizePrice);

    // set product_size to quality
    product_size.innerHTML = quality;
    // set quantity_price to totalSizePrice
    quantity_price.innerHTML = totalSizePrice;

});


// function to calculate total area of objects
function calculateTotalArea(objects) {
    var totalArea = 0;
    // loop through all objects
    objects.forEach(function(object) {
        // get object height on screen
        var objectHeight = object.getBoundingRect().height;
        // return object height
        totalArea += objectHeight;

        
    });
    return totalArea;
}
var hidden_total_price =0;
// function take frontdesign and backdesign height and quantity and call ajax to get price
function getQuote(frontDesignHeight, backDesignHeight, quantity,quantity_price) {
    
    // check if quantity not null or empty or 0
    if (quantity == "" || quantity == 0) {
        swal.fire("Please enter quantity");
        // return
        return;
    }
    // get csrf_token from form with id has input  "csrf_token"
    var crftoken = document.getElementById("crftokenform").getElementsByTagName("input")[0].value;
    var product_id = document.getElementById("product_id").value;
    // create form data
    var formData = new FormData();
    formData.append('front_design_height', frontDesignHeight);
    formData.append('back_design_height', backDesignHeight);
    formData.append('quantity', quantity);
    formData.append('quantity_price', quantity_price);
    formData.append('csrfmiddlewaretoken', crftoken);
    formData.append('product_id', product_id);

    // axios call to get quote
    axios.post(`${projecturl}product/get_quote/`, formData, {
        withCredentials: true,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(function (response) {
        // get from response front_design_price , back_design_price , total_price , quantity_price
        var front_design_price = response.data.front_design_price;
        var back_design_price = response.data.back_design_price;
        var total_price = response.data.total_price;
        var quantity_price = response.data.quantity_price;
        // total_price = round total_price
        total_price = Math.round(total_price);
        total_price= '$'+total_price;
        // get front_price by id
        // document.getElementById("front_price").innerHTML = front_design_price;
        // // get back_price by id
        // document.getElementById("back_price").innerHTML = back_design_price;
        // get quantity_price by id
        document.getElementById("quantity_price").innerHTML = quantity_price;
        // get total_price by id
        document.getElementById("total_price").innerHTML = total_price;
        hidden_total_price = total_price;
    })
    .catch(function (error) {
        console.log(error);
    });
}

// function apply_copoun 
function apply_copoun() {
    // get copoun code from input with id "copoun_code"
    var copoun_code = document.getElementById("copoun_code").value;
    // check if copoun_code is null or empty
    if (copoun_code == "") {
        // alert to the user to enter copoun code
        swal.fire("Please enter copoun code");
        // return
        return;
    }
    // get total_price from input with id "total_price"
    var total_price = document.getElementById("total_price").innerHTML;

    // check if total_price is null or empty
    if (total_price == "") {
        // alert to the user to enter quantity
        swal.fire("Please enter quantity");
        // return
        return;
    }
    total_price = hidden_total_price;
    // remove $ from total_price
    total_price = total_price.replace("$", "");


    // get csrf_token from form with id has input  "csrf_token"
    var crftoken = document.getElementById("crftokenform").getElementsByTagName("input")[0].value;
    // create form data
    var formData = new FormData();
    formData.append('copoun_code', copoun_code);
    formData.append('csrfmiddlewaretoken', crftoken);
    // apply total_price
    formData.append('total_price', total_price);
    // axios call to apply copoun
    axios.post(`${projecturl}product/apply_copoun/`, formData, {
        withCredentials: true,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(function (response) {
        var total_price = response.data.total_price;
        // add $ to total_price
        total_price = '$' + total_price;
        // get copoun_code by id
        document.getElementById("copoun_code").value = copoun_code;
        // get total_price by id
        document.getElementById("total_price").innerHTML = total_price;
    }
    )
    .catch(function (error) {
        // alert to the user that copoun code not valid
        swal.fire("Copoun code not valid");
    });

}

// Common function to handle the download process
function getTShirtImage(canvasId, backgroundImageId) {
    // Get the background image and canvas element
    var backgroundImage = document.getElementById(backgroundImageId);
    var canvas = document.getElementById(canvasId);

    // Create a new canvas to combine the images
    var combinedCanvas = document.createElement("canvas");
    combinedCanvas.width = canvas.width;
    combinedCanvas.height = canvas.height;
    var context = combinedCanvas.getContext("2d");

    // Draw the t-shirt background image
    context.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);

    // Draw the canvas design on top
    context.drawImage(canvas, 0, 0);

    // Return the combined image data
    return combinedCanvas.toDataURL("image/png");
}



//------------------------
// add to card
document.getElementById("addToCard").addEventListener("click", function() {
    // get product id from input with id "product_id"
    var product_id = document.getElementById("product_id").value;
    // get quantity from input with id "product_size"
    var quantity = document.getElementById("product_size").innerHTML;
    // get front design price from input with id "front_design_price"
    var front_design_price = document.getElementById("front_design_price").innerHTML;
    // get back design price from input with id "back_design_price"
    var back_design_price = document.getElementById("back_design_price").innerHTML;
    // get quantity price from input with id "quantity_price"
    var quantity_price = document.getElementById("quantity_price").innerHTML;
    // get total price from input with id "total_price"
    var total_price = document.getElementById("total_price").innerHTML;
    // remove $ from total_price
    total_price = total_price.replace("$", "");
    // get canvas background color 
    var canvasBackgroundColor = document.getElementById("tshirt-div").style.backgroundColor;

    // get size sybmol and quality from input with class "SizeItem"
    var SizeItem = document.querySelectorAll(".SizeItem");
    // loop through all SizeItem
    var size = [];
    SizeItem.forEach(function(SizeItem) {
        // get data-size
        var SizeItemSize = SizeItem.getAttribute("data-size-symbol");
        var SizeItemNumber = SizeItem.getElementsByTagName("input")[0].value;
        // check if SizeItemInput is null
        if (SizeItemNumber == "") {
            // set SizeItemInput to 0
            SizeItemNumber = 0;
        }
        // create object size with size and number
        size.push({symbol:SizeItemSize,quality:SizeItemNumber});
    });

    // convert front canvas as jpg data 
    canvas.discardActiveObject();
    canvas.renderAll();
    var frontimageData = canvas.toDataURL({
        format: 'jpeg',
        quality: 1
    });
    // convert back canvas as jpg data
    canvasBack.discardActiveObject();
    canvasBack.renderAll();
    var backimageData = canvasBack.toDataURL({
        format: 'jpeg',
        quality: 1
    });

    var front_tshirt_image = getTShirtImage("tshirt-canvas-front", "tshirt-backgroundpicture"); 
    var back_tshirt_image = getTShirtImage("tshirt-canvas-back", "tshirt-backgroundpicture-back");

    // get csrf_token from form with id has input  "csrf_token"
    var crftoken = document.getElementById("crftokenform").getElementsByTagName("input")[0].value;
    // confirm to the user to add to card
    var confirm = window.confirm("Are you sure you want to add to card?");
    // check if confirm is false
    if (confirm == false) {
        // return
        return;
    }
    // check if quantity not null or empty or 0
    if (quantity == "" || quantity == 0) {
        // alert to the user to enter quantity
        swal.fire("Please enter quantity");
        // return
        return;
    }


    // loop on front canvas objects and back canvas objects and get all images with original size
    // var frontObjects = canvas.getObjects();
    // var backObjects = canvasBack.getObjects();
    // // loop through all frontObjects
    // frontObjects.forEach(function(object) {
    //     // check if object type is image
    //     if (object.type == "image") {
    //         // get image src
    //         var imageSrc = object.getSrc();
    //         // put imageSrc in design_resource
    //         design_resource.push(imageSrc);
    //         // open new window with imageSrc
    //         window.open(imageSrc);
    //     }
    // });

    // // loop through all backObjects
    // backObjects.forEach(function(object) {
    //     // check if object type is image
    //     if (object.type == "image") {
    //         // get image src
    //         var imageSrc = object.getSrc();
    //         // put imageSrc in design_resource
    //         design_resource.push(imageSrc);
    //     }

    // });

    // console.log("design_resource=> " , design_resource);



    // return;



    console.log("add to card=> " , quantity);
    // create form data
    var formData = new FormData();
    formData.append('product_id', product_id);
    formData.append('quantity', quantity);
    formData.append('front_design_price', front_design_price);
    formData.append('back_design_price', back_design_price);
    formData.append('quantity_price', quantity_price);
    formData.append('total_price', total_price);
    formData.append('frontcanvas', frontimageData);
    formData.append('backcanvas', backimageData);
    formData.append('csrfmiddlewaretoken', crftoken);
    formData.append('canvasBackgroundColor', canvasBackgroundColor);
    // append backimageData , frontimageData 
    formData.append('front_design', backimageData);
    formData.append('back_design', frontimageData);
    // append size
    formData.append('size', JSON.stringify(size));
    // append front_tshirt_image , back_tshirt_image
    formData.append('front_tshirt_image', front_tshirt_image);
    formData.append('back_tshirt_image', back_tshirt_image);

    // axios call to add to card
    axios.post(`${projecturl}product/add_to_card/`, formData, {
        withCredentials: true,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(function (response) {
        // alert to the user that product added to card
        swal.fire("Product added to your card");
        console.log(response)
    }
    )
    .catch(function (error) {
        // alert to the user that product not added to card
        swal.fire("Product not added to your card");
    });
    
});

var designData={};

// get element by id loaddesign , save-design

document.getElementById("loaddesign").addEventListener("click", function() {
    loaddesign();
});

function saveDesign() {
    console.log("savedesign");
    // save canvas front, back, frontcanvase as jpg, backcanvas as jpg data in designData
    designData.front = JSON.stringify(canvas);
    designData.back = JSON.stringify(canvasBack);
    // get csrf_token from form with id has input  "csrf_token"
    var crftoken = document.getElementById("crftokenform").getElementsByTagName("input")[0].value;
    console.log(crftoken);
    // get front canvas as jpg data with original size
    canvas.discardActiveObject();
    canvas.renderAll();
    var frontimageData = canvas.toDataURL({
        format: 'jpeg',
        quality: 1
    });
    // get name from input with id "design-name"
    var designName = document.getElementById("design-name").value;
    // check if design name is empty    
    if (designName == "") {
        // show message to the user to enter design name under input with id "design-name" and focus on it
        document.getElementById("design-name").focus();
        document.getElementById("design-name").placeholder = "Please enter design name";
        return;
    }
    var formData = new FormData();
    formData.append('front', JSON.stringify(canvas));
    formData.append('back', JSON.stringify(canvasBack));
    formData.append('frontcanvas', frontimageData);
    formData.append('name', designName);
    formData.append('csrfmiddlewaretoken', crftoken);

    // axios call to save design
    axios.post(`${projecturl}product/save_design/`, formData, {
        withCredentials: true,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(function (response) {
        // alert to the user that design saved
        swal.fire("Design saved");
        // get product_designs_data
        var product_designs = response.data.product_design.product_design;
        // get dev by id load-design
        var loadDesign = document.getElementById("load-design");
        // append product_designs to loadDesign
        // src = frontimageData
        loadDesign.innerHTML += `
        <div class="p-3">
       <img
        src="${frontimageData}"
         alt=""
         width="100px"
         height="100px"
         onclick="loaddesign(${product_designs.frontcanvas}, ${product_designs.backcanvas})"
         id="loaddesign-${product_designs.id}"
         class=""
         />
         </div>
        
        `;

    })
    .catch(function (error) {

        // alert to the user that design not saved
        swal.fire("Design not saved");
        console.log(error);
    });
}
function loaddesign(front, back) {
   console.log("set design"); 

   // set front canvas from front
    canvas.loadFromJSON(front, function () {
         canvas.renderAll();
    });
    // set back canvas from back
    canvasBack.loadFromJSON(back, function () {
         canvasBack.renderAll();
    });
    
}


document.getElementById('undoButton').addEventListener('click', undo());
document.getElementById('redoButton').addEventListener('click', redo());








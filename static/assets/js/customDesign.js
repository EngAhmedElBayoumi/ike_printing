projecturl = "http://127.0.0.1:8000/";

let canvas = new fabric.Canvas('tshirt-canvas-front');
let canvasBack = new fabric.Canvas('tshirt-canvas-back');
// Initialize undo and redo stacks
var undoStack = [];
var redoStack = [];
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
}

//function to change font size
function changeFontSize(fontSize){
    activecanvas.getActiveObject().set("fontSize", fontSize);
    activecanvas.renderAll();
}

//function to change font color
function changeFontColor(fontColor){
    activecanvas.getActiveObject().set("fill", fontColor);
    activecanvas.renderAll();
}
// change border color  
function changeBorderColor(borderColor){
    activecanvas.getActiveObject().set("stroke", borderColor);
    activecanvas.renderAll();
}

function changeShadowColor(shadowColor) {
    var activeObject = canvas.getActiveObject();
    if (activeObject && shadowColor) {
        var shadow = activeObject.getShadow();
        shadow.color = shadowColor;
        activeObject.setShadow(shadow);
        activecanvas.renderAll();
    }
}



//function to change font style
function changeFontStyle(fontStyle){
    activecanvas.getActiveObject().set("fontStyle", fontStyle);
    activecanvas.renderAll();
}

// change border color  
function changeBorderColor(borderColor){
    activecanvas.getActiveObject().set("stroke", borderColor);
    activecanvas.renderAll();
}

//function to change text leter space
function changeTextLetterSpace(textLetterSpace){
    activecanvas.getActiveObject().set("charSpacing", textLetterSpace);
    activecanvas.renderAll();
}

// function to change text to bold and unbold
function changeBold(){
    var isBold = activecanvas.getActiveObject().get("fontWeight") == "bold";
    activecanvas.getActiveObject().set("fontWeight", isBold ? "normal" : "bold");
    activecanvas.renderAll();
}

// function to change text to italic and unitalic
function changeItalic(){
    var isItalic = activecanvas.getActiveObject().get("fontStyle") == "italic";
    activecanvas.getActiveObject().set("fontStyle", isItalic ? "normal" : "italic");
    activecanvas.renderAll();
}
// change changeUnderline
function changeUnderline(){
    var isUnderline = activecanvas.getActiveObject().get("underline") == "underline";
    activecanvas.getActiveObject().set("underline", isUnderline ? "" : "underline");
    activecanvas.renderAll();
}


//add image function by src
function addImage(imageURL){
    fabric.Image.fromURL(imageURL, function (img) {
        // get image width and height
        scaleImageToFitCanvas(img, activecanvas);
        activecanvas.add(img);
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
    }
}

//send backward
function sendBackwards() {
    var activeObject = activecanvas.getActiveObject();
    if (activeObject) {
        activecanvas.sendBackwards(activeObject);
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
    if(keyCode == 46 || keyCode == 8){
        activecanvas.remove(activecanvas.getActiveObject());
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
        alert("Please enter quantity");
        // return
        return;
    }
    // get csrf_token from form with id has input  "csrf_token"
    var crftoken = document.getElementById("crftokenform").getElementsByTagName("input")[0].value;
    // create form data
    var formData = new FormData();
    formData.append('front_design_height', frontDesignHeight);
    formData.append('back_design_height', backDesignHeight);
    formData.append('quantity', quantity);
    formData.append('quantity_price', quantity_price);
    formData.append('csrfmiddlewaretoken', crftoken);

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
        alert("Please enter copoun code");
        // return
        return;
    }
    // get total_price from input with id "total_price"
    var total_price = document.getElementById("total_price").innerHTML;

    // check if total_price is null or empty
    if (total_price == "") {
        // alert to the user to enter quantity
        alert("Please enter quantity");
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
        alert("Copoun code not valid");
    });

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
        alert("Please enter quantity");
        // return
        return;
    }

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

    // axios call to add to card
    axios.post(`${projecturl}product/add_to_card/`, formData, {
        withCredentials: true,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(function (response) {
        // alert to the user that product added to card
        alert("Product added to your card");
        console.log(response)
    }
    )
    .catch(function (error) {
        // alert to the user that product not added to card
        alert("Product not added to your card");
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
        alert("Design saved");
    })
    .catch(function (error) {

        // alert to the user that design not saved
        alert("Design not saved");
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












// Function to save the current state of the canvas
function saveState() {
    undoStack.push(JSON.stringify(activecanvas));
    redoStack = []; // Clear redo stack when a new action is performed
}

// Function to undo the last action
function undo() {
    if (undoStack.length > 1) {
        redoStack.push(undoStack.pop()); // Move the current state to redo stack
        activecanvas.loadFromJSON(undoStack[undoStack.length - 1], function () {
            activecanvas.renderAll();
        });
    }
}

// Function to redo the last undone action
function redo() {
    if (redoStack.length > 0) {
        undoStack.push(redoStack.pop()); // Move the current state to undo stack
        activecanvas.loadFromJSON(undoStack[undoStack.length - 1], function () {
            activecanvas.renderAll();
        });
    }
}


// on modify canvas call saveState function
activecanvas.on('object:modified', function () {
    saveState();
});

// ... (your existing code)

// You can then call undo() and redo() functions as needed, for example, when a button is clicked.
// For example, if you have undoButton and redoButton elements:
document.getElementById('undoButton').addEventListener('click', undo);
document.getElementById('redoButton').addEventListener('click', redo);








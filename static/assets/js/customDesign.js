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
        fontFamily: 'helvetica',
        fill: '#000000',
        fontSize: 20
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
        img.scaleToHeight(150);
        img.scaleToWidth(150);
        activecanvas.add(img);
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
    
    reader.onload = function (event){
        var imgObj = new Image();
        imgObj.src = event.target.result;

        // When the picture loads, create the image in Fabric.js
        imgObj.onload = function () {
            var img = new fabric.Image(imgObj);

            img.scaleToHeight(300);
            img.scaleToWidth(300); 
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

document.getElementById("Quote_Buy_tab").addEventListener("click", function() {
    // get pruduct height from input with id "product_height"
    var productHeight = document.getElementById("product_height").value;
    console.log(productHeight);
    // get the objects on the canvas
    var frontObjects = canvas.getObjects();
    var backObjects = canvasBack.getObjects();
    // calculate total area for front canvas
    var frontTotalArea = calculateTotalArea(frontObjects);
    // calculate total area for back canvas
    var backTotalArea = calculateTotalArea(backObjects);
    // Round the values to two decimal places after dividing by 96
    front_design_price.innerHTML = frontTotalArea + " inches";
    back_design_price.innerHTML = backTotalArea + " inches";
    calculatePrice();
});



function calculateTotalArea(objects) {
    // initialize total area
    var totalArea = 0;

    // loop through each object and add its area to the total
    for (var i = 0; i < objects.length; i++) {
        var object = objects[i];
        // assuming width and height are in pixels
        // adjust width and height based on the object's scale
        var scaledHeight = object.height * object.scaleY;
        // convert from pixels to inches
        scaledHeight /= 35;
        // calculate area and add to the total
        totalArea += scaledHeight;
    }

    return (totalArea).toFixed(2);
}





//----------------------------------calculate price call----------------------------------------------

function calculatePrice(){
    // get t-shirt height from activecanvas on screen
    var tshirtHeight = activecanvas.height;//<----------
    // get front design height on screen
    // get the objects on the canvas
    var frontObjects = canvas.getObjects();
    var backObjects = canvasBack.getObjects();
    // calculate total height for front canvas
    var frontDesignHeight = calculateTotalArea(frontObjects);//<----------
    // calculate total height for back canvas
    var backDesignHeight = calculateTotalArea(backObjects);//<----------
    // get product hidden input with id "product_id"
    var product_id = document.getElementById("product_id").value;

}





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
        console.log(response);
    })
    .catch(function (error) {
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


// get element by id Quote_Buy
// add event listener click







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








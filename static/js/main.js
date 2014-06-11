/**
 * Created by tmehta on 11/06/14.
 */
//Full Canvas
var state;
var last_action;
var line;
var curr_line_width = 3;

function setState(new_state) {
    state = new_state;
    /* modify the status span so the user knows what's being selected */
    state_p = document.getElementById("status");
    state_p.innerHTML = state;
}

function newLine() {
    setState("line");
}

function undo() {
    shapes.shift();
    drawShapes();
}

function redo() {
    if (last_action == "clear") {
        shapes = shapes_copy.slice(0);
        drawShapes();
        last_action = "redo";
    }
    if (shapes.length < shapes_copy.length) {
        shapes.unshift(shapes_copy[(shapes_copy.length - 1) - shapes.length]);
        drawShapes();
    }
}


function changeLineWidth() {
    var input = parseInt(prompt("Enter the Line Width Desired (Default was 5)"));
    if (!isNaN(input)) {
        curr_line_width = input;
        for (var i = 0; i < shapes.length; i++) {
            var shape = shapes[i];
            if (shape.isHighlighted) {
                shape.setLineWidth(curr_line_width);
            }
        }
        var line_width_p = document.getElementById("current_line_width");
        line_width_p.innerHTML = curr_line_width;
        drawShapes();

    }
}

function Shape() {
    this.color = "black";
    this.line_color;
    this.line_width = 3;
    this.isSelected = false;
    this.type_of_shape = "";
}

Shape.prototype.setColor = function (color) {
    this.color = color;
};
Shape.prototype.setOutlineColor = function (color) {
    this.line_color = color;
};
Shape.prototype.setStartPos = function (start_x, start_y) {
    this.start_x = start_x;
    this.start_y = start_y;
};
Shape.prototype.setEndPos = function (end_x, end_y) {
    this.end_x = end_x;
    this.end_y = end_y;
};
Shape.prototype.appendPos = function (x, y) {
    this.x.push(x);
    this.y.push(y);
}
Shape.prototype.setRef = function (clickX, clickY) {
    var ref_x = (this.start_x + this.end_x) / 2;
    var ref_y = (this.start_y + this.end_y) / 2;
    this.offset_x = clickX - ref_x;
    this.offset_y = clickY - ref_y;
};
Shape.prototype.move = function (clickX, clickY) {
    var ref_x = (this.start_x + this.end_x) / 2;
    var ref_y = (this.start_y + this.end_y) / 2;
    var dx = clickX - this.offset_x - ref_x;
    var dy = clickY - this.offset_y - ref_y;
    this.start_x += dx;
    this.start_y += dy;
    this.end_x += dx;
    this.end_y += dy;
};
Shape.prototype.setLineWidth = function (line_width) {
    this.line_width = line_width;
}
function Line(canvas) {
    this.x = new Array();
    this.y = new Array();
    this.dotted = false;
    this.head = "line"; // could be one of: 'nothing', 'arrow', 'line'
    this.context = canvas.getContext("2d");
    this.type_of_shape = "line";
}

Line.prototype = new Shape();
Line.prototype.setDotted = function (bo) {
    this.dotted = bo;
}
Line.prototype.setHead = function (t) {
    this.head = t;
}
Line.prototype.appendPos = function (x, y) {
    this.x.push(x);
    this.y.push(y);
}
STEP_CONST = 10;
Line.prototype.draw = function () {
    if (this.isHighlighted)
        this.context.globalAlpha = 1;
    else
        this.context.globalAlpha = 0.85;
    this.context.beginPath();
    if (this.dotted == true)
        this.context.setLineDash([8, 3]);
    else
        this.context.setLineDash([]);
    for (var i = 0; i < this.x.length; i++) {
        if (i == 0) {
            this.context.moveTo(this.x[i], this.y[i]);
        } else {
            this.context.lineTo(this.x[i], this.y[i]);
        }
    }
    ;

    //because i want to fill the arrow head, i have to start a new path (hence finishing this one here)..otherwise the fill() doesn't work right
    this.context.strokeStyle = this.line_color;
    this.context.lineWidth = this.line_width;
    this.context.stroke();

    if ((this.head == "line") || (this.head == "arrow")) {
        var dX = this.x[this.x.length - 1] - this.x[this.x.length - 1 - STEP_CONST];
        var dY = this.y[this.y.length - 1] - this.y[this.y.length - 1 - STEP_CONST];
        var R = Math.sqrt(Math.pow(dX, 2) + Math.pow(dY, 2));
        var xR = dX / R;
        var yR = dY / R;
        var offset = 0;

        if (this.head == "arrow") {
            offset = 5;
        }
        this.context.beginPath();
        this.context.lineTo(this.x[this.x.length - 1 - offset] + STEP_CONST * yR, this.y[this.y.length - 1 - offset] - STEP_CONST * xR);
        this.context.lineTo(this.x[this.x.length - 1 - offset] - STEP_CONST * yR, this.y[this.y.length - 1 - offset] + STEP_CONST * xR);
        if (this.head == "arrow") {
            this.context.lineTo(this.x[this.x.length - 1], this.y[this.y.length - 1]);
            this.context.fillStyle = this.line_color;
            this.context.fill();
        }
        this.context.stroke();
    }
};

function ColorButton(canvas, x, y, length, color) {
    this.context = canvas.getContext("2d");
    this.start_x = x;
    this.start_y = y;
    this.side_length = length;
    this.color = color;
    this.strokeColor = color;
}

ColorButton.prototype.draw = function () {
    this.context.globalAlpha = 0.85;
    this.context.beginPath();
    this.dir_x = (this.end_x - this.start_x) / Math.abs(this.end_x - this.start_x);
    this.dir_y = (this.end_y - this.start_y) / Math.abs(this.end_y - this.start_y);
    this.context.moveTo(this.start_x, this.start_y);
    this.context.lineTo(this.start_x + this.side_length, this.start_y);
    this.context.lineTo(this.start_x + this.side_length, this.start_y + this.side_length);
    this.context.lineTo(this.start_x, this.start_y + this.side_length);
    this.context.closePath();
    this.context.fillStyle = this.color;
    this.context.fill();
    if (this.isSelected) {
        this.context.strokeStyle = "black";
        this.context.lineWidth = 3;
    } else {
        this.context.strokeStyle = this.color;
        this.context.lineWidth = 1;
    }
    this.context.stroke();
};

ColorButton.prototype.testHit = function (testX, testY) {
    ref_x = this.start_x;
    ref_y = this.start_y;
    test_x_in_the_middle = ((this.start_x - testX) * (this.start_x + this.side_length - testX)) < 0;
    test_y_in_the_middle = ((this.start_y - testY) * (this.start_y + this.side_length - testY)) < 0;
    if (test_x_in_the_middle && test_y_in_the_middle) {
        return true;
    }
    return false;
};

function Head(canvas, x, y, w, h, elem) {
    this.context = canvas.getContext("2d");
    this.start_x = x;
    this.start_y = y;
    this.width = w;
    this.height = h;
    this.elem = elem;
    this.epislon = 12;
}

Head.prototype.draw = function () {
    this.context.globalAlpha = 0.85;
    this.context.beginPath();
    /*this.dir_x = (this.end_x - this.start_x) / Math.abs(this.end_x - this.start_x);
     this.dir_y = (this.end_y - this.start_y) / Math.abs(this.end_y - this.start_y);*/
    this.context.moveTo(this.start_x, this.start_y);
    this.context.lineTo(this.start_x + this.width, this.start_y);
    this.context.lineTo(this.start_x + this.width, this.start_y + this.height);
    this.context.lineTo(this.start_x, this.start_y + this.height);
    this.context.closePath();
    if (this.isSelected) {
        this.context.strokeStyle = "black";
        this.context.lineWidth = 3;
        this.context.stroke();
    }
    this.context.beginPath();
    if (this.elem == "line") {
        this.context.moveTo(this.start_x + this.width / 2, this.start_y);
        this.context.lineTo(this.start_x + this.width / 2, this.start_y + this.height);

    }
    if (this.elem == "arrow") {
        this.context.moveTo(this.start_x + this.width / 2 - this.epislon, this.start_y);
        this.context.lineTo(this.start_x + this.width / 2 - this.epislon, this.start_y + this.height);
        this.context.lineTo(this.start_x + this.width / 2 + this.epislon, this.start_y + this.height / 2);
        this.context.closePath();
    }
    this.context.strokeStyle = "black";
    this.context.lineWidth = 3;
    this.context.stroke();


};

Head.prototype.testHit = function (testX, testY) {

    ref_x = this.start_x;
    ref_y = this.start_y;
    test_x_in_the_middle = ((this.start_x - testX) * (this.start_x + this.width - testX)) < 0;
    test_y_in_the_middle = ((this.start_y - testY) * (this.start_y + this.height - testY)) < 0;
    if (test_x_in_the_middle && test_y_in_the_middle) {
        return true;
    }
    return false;
};

function Type(canvas, x, y, w, h, elem) {
    this.context = canvas.getContext("2d");
    this.start_x = x;
    this.start_y = y;
    this.width = w;
    this.height = h;
    this.elem = elem;
    this.epislon = 15;
}

Type.prototype.draw = function () {
    this.context.globalAlpha = 0.85;
    this.context.beginPath();
    /*this.dir_x = (this.end_x - this.start_x) / Math.abs(this.end_x - this.start_x);
     this.dir_y = (this.end_y - this.start_y) / Math.abs(this.end_y - this.start_y);*/
    this.context.moveTo(this.start_x, this.start_y);
    this.context.lineTo(this.start_x + this.width, this.start_y);
    this.context.lineTo(this.start_x + this.width, this.start_y + this.height);
    this.context.lineTo(this.start_x, this.start_y + this.height);
    this.context.closePath();
    if (this.isSelected) {
        this.context.strokeStyle = "black";
        this.context.lineWidth = 3;
        this.context.stroke();
    }
    this.context.beginPath();
    if (this.elem == true) {
        this.context.setLineDash([8, 3]);
    }
    if (this.elem == false) {
        this.context.setLineDash([]);
    }
    this.context.moveTo(this.start_x + this.epislon, this.start_y + this.height / 2);
    this.context.lineTo(this.start_x - this.epislon + this.width, this.start_y + this.height / 2);
    this.context.strokeStyle = "black";
    this.context.lineWidth = 3;
    this.context.stroke();
    this.context.setLineDash([]);

};

Type.prototype.testHit = function (testX, testY) {

    ref_x = this.start_x;
    ref_y = this.start_y;
    test_x_in_the_middle = ((this.start_x - testX) * (this.start_x + this.width - testX)) < 0;
    test_y_in_the_middle = ((this.start_y - testY) * (this.start_y + this.height - testY)) < 0;
    if (test_x_in_the_middle && test_y_in_the_middle) {
        return true;
    }
    return false;
};
// This array hold all the shapes on the canvas.
var shapes = [];
var shapes_copy = [];

var canvas;
var context;
var fill;
var fill_context;
var outline;
var outline_context;
var head;
var head_context;
var type;
var type_context;
var colors;
var curr_color = null;
var curr_head = null;
var curr_type = null;
var curr_outline_color = null;
var fill_buttons = [];
var outline_buttons = [];
var head_buttons = [];
var type_buttons = [];
var previousSelectedFillButtonIndex = 0;
var previousSelectedOutlineButtonIndex = 0;
var previousSelectedHeadButtonIndex = 0;
var previousSelectedTypeButtonIndex = 0;
window.onload = function () {
    canvas = document.getElementById("canvas");
    context = canvas.getContext("2d");
    /*fill = document.getElementById("fill");
     fill_context = fill.getContext("2d");*/
    outline = document.getElementById("other-outline");
    outline_context = outline.getContext("2d");
    head = document.getElementById("head");
    head_context = head.getContext("2d");
    type = document.getElementById("type");
    type_context = type.getContext("2d");

    canvas.onmousedown = canvasMouseDown;
    canvas.onmouseup = canvasMouseUp;
    canvas.onmouseout = canvasMouseUp;
    canvas.onmousemove = canvasMouseMove;
    canvas.onclick = canvasMouseClick;

    /*  fill.onclick = fillMouseClick;
     createColors(fill_buttons, fill, "fill");*/
    outline.onclick = outlineMouseClick;
    createColors(outline_buttons, outline, "outline");

    head.onclick = headMouseClick;
    createHeads(head_buttons, head);

    type.onclick = typeMouseClick;
    createTypes(type_buttons, type);
    drawButtons();

    var line_width_p = document.getElementById("current_line_width");
    line_width_p.innerHTML = curr_line_width;
    setState("line");
};
function createColors(buttons, panel, called_from) {
    colors = ["green", "blue", "red", "yellow", "magenta", "orange", "brown", "purple", "pink", "black"];
    var length = panel.height / 2;
    for (var i = 0; i < colors.length; i += 2) {
        buttons.push(new ColorButton(panel, i / 2 * length, 0, length, colors[i]));
        buttons.push(new ColorButton(panel, i / 2 * length, length, length, colors[i + 1]));
    }
    buttons[0].isSelected = true;
    if (called_from == "fill") {
        curr_color = colors[0];
        previousSelectedFillButtonIndex = 0;
    }
    if (called_from == "outline") {
        curr_outline_color = colors[0];
        previousSelectedOutlineButtonIndex = 0;
    }

};
heads_elem = ["nothing", "line", "arrow"];
function createHeads(buttons, panel) {
    var NUM = heads_elem.length;
    var length = panel.width / NUM;
    var epi = 4;
    buttons.push(new Head(panel, 0 * length, 0, length, panel.height, heads_elem[0]));
    buttons.push(new Head(panel, 1 * length, 0, length, panel.height, heads_elem[1]));
    buttons.push(new Head(panel, 2 * length, 0, length, panel.height, heads_elem[2]));
    buttons[0].isSelected = true;
    curr_head = heads_elem[0];
    previousSelectedHeadButtonIndex = 0;
};

types_elem = [true, false];
function createTypes(buttons, panel) {
    var NUM = types_elem.length;
    var length = panel.width / NUM;
    var epi = 4;
    buttons.push(new Type(panel, 0 * length, 0, length, panel.height, types_elem[0]));
    buttons.push(new Type(panel, 1 * length, 0, length, panel.height, types_elem[1]));
    buttons[0].isSelected = true;
    curr_type = types_elem[0];
    previousSelectedTypeButtonIndex = 0;
};


function clearCanvas() {
    last_action = "clear";
    shapes = [];
    drawShapes();
}

function drawShapes() {
    // Clear the canvas.
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Go through all the shapes.
    for (var i = shapes.length - 1; i >= 0; i--) {
        var shape = shapes[i];
        shape.draw();
    }
}

function drawButtons() {
    /*// Clear the canvas.
     fill_context.clearRect(0, 0, fill.width, fill.height);
     // Go through all the shapes.
     for(var i= 0; i < fill_buttons.length; i++) {
     fill_buttons[i].draw();
     }*/

    outline_context.clearRect(0, 0, outline.width, outline.height);
    for (var i = 0; i < outline_buttons.length; i++) {
        outline_buttons[i].draw();
    }

    head_context.clearRect(0, 0, head.width, head.height);
    for (var i = 0; i < head_buttons.length; i++) {
        head_buttons[i].draw();
    }

    type_context.clearRect(0, 0, type.width, type.height);
    for (var i = 0; i < type_buttons.length; i++) {
        type_buttons[i].draw();
    }
}


var click_event = false; // javascript's mouseclick event can happen even if user select, drag, and release the mouse, and it happens after mouseUp
// in our case, we'll not treat those as mouse click.  We'll detect actually click by a down and up without move
function canvasMouseDown(e) {
    // Get the canvas click coordinates.
    var clickX = e.pageX - canvas.offsetLeft;
    var clickY = e.pageY - canvas.offsetTop;
    click_event = true;
    if (state == "line") {
        // Create the new Line.
        line = new Line(canvas);
        line.appendPos(clickX, clickY);
        line.setLineWidth(curr_line_width);
        line.setDotted(curr_type);
        line.setHead(curr_head);
        line.setOutlineColor(curr_outline_color);
        if (curr_color != null) {
            line.setColor(curr_color);
        }
        return;
    }
    if (state == "DottedLine") {
        // Create the new Line.
        line = new Line(canvas);
        line.appendPos(clickX, clickY);
        line.setLineWidth(curr_line_width);
        line.setDotted(true);
        line.setOutlineColor(curr_outline_color);
        if (curr_color != null) {
            line.setColor(curr_color);
        }
        return;
    }

    var i = selectedShapeIndex(clickX, clickY);
    if (i != -1) {
        shapes[i].isSelected = true;
        shape = shapes.splice(i, 1);
        shape[0].setRef(clickX, clickY);
        shapes.unshift(shape[0]);
        return;
    }
}

function canvasMouseMove(e) {
    // Get the canvas click coordinates.
    var clickX = e.pageX - canvas.offsetLeft;
    var clickY = e.pageY - canvas.offsetTop;
    click_event = false;
    if ((state == "line") || (state == "DottedLine")) {
        if (line != null) {
            line.appendPos(clickX, clickY);
            drawShapes();
            line.draw();
        }
        return;
    }
    if (shapes[0].isSelected) {
        shapes[0].move(clickX, clickY);
        drawShapes();
    }
    return;

}

function canvasMouseUp(e) {
    // Get the canvas click coordinates.
    var clickX = e.pageX - canvas.offsetLeft;
    var clickY = e.pageY - canvas.offsetTop;

    if ((state == "line") || (state == "DottedLine")) {
        line.appendPos(clickX, clickY);
        shapes.unshift(line);
        //whenver there's new action, make a copy of shapes, this is to update shapes_copy in order to 'redo'
        shapes_copy = shapes.slice(0);
        drawShapes();
        line = null;
        resetState();
        return;
    }
    shapes[0].isSelected = false;
    return;

}

function resetState() {
    last_action = state;
    //setState("");
}

var num_highlighted = 0;

function canvasMouseClick(e) {
}

function fillMouseClick(e) {
    onColorClick(e, fill, fill_buttons, "fill")
}

function outlineMouseClick(e) {
    onColorClick(e, outline, outline_buttons, "outline")
}

function headMouseClick(e) {
    onColorClick(e, head, head_buttons, "head")
}

function typeMouseClick(e) {
    onColorClick(e, type, type_buttons, "type")
}

function onColorClick(e, panel, buttons, called_from) {
    var clickX = e.pageX - panel.offsetLeft - panel.style.borderWidth;
    var clickY = e.pageY - panel.offsetTop - panel.style.borderWidth;

    var i = selectedButtonIndex(buttons, clickX, clickY);
    if (i != -1) {
        buttons[i].isSelected = true;
        if (called_from == "fill") {
            if (previousSelectedFillButtonIndex != -1) {
                buttons[previousSelectedFillButtonIndex].isSelected = false;
            }
            curr_color = colors[i];
            /* set the colors of the highlighted items */
            setHighlightedColor("fill");
            previousSelectedFillButtonIndex = i;
        }
        if (called_from == "outline") {
            if (previousSelectedOutlineButtonIndex != -1) {
                buttons[previousSelectedOutlineButtonIndex].isSelected = false;
            }
            curr_outline_color = colors[i];
            /* set the colors of the highlighted items */
            setHighlightedColor("outline");
            previousSelectedOutlineButtonIndex = i;
        }
        if (called_from == "head") {
            if (previousSelectedHeadButtonIndex != -1) {
                buttons[previousSelectedHeadButtonIndex].isSelected = false;
            }
            curr_head = heads_elem[i];
            previousSelectedHeadButtonIndex = i;
        }
        if (called_from == "type") {
            if (previousSelectedTypeButtonIndex != -1) {
                buttons[previousSelectedTypeButtonIndex].isSelected = false;
            }
            curr_type = types_elem[i];
            previousSelectedTypeButtonIndex = i;
        }
        drawButtons();
    }
}

function setHighlightedColor(called_from) {
    for (var i = 0; i < shapes.length; i++) {
        var shape = shapes[i];
        if (shape.isHighlighted) {
            if (called_from == "fill") shape.setColor(curr_color);
            if (called_from == "outline") shape.setOutlineColor(curr_outline_color);
        }
    }
    drawShapes();
}

// find the selected shape based on input coordinate
// return the index of the selected shape.
function selectedShapeIndex(clickX, clickY) {
    for (var i = 0; i < shapes.length; i++) {
        var shape = shapes[i];
        if (shape.testHit(clickX, clickY)) {
            return i;
        }
    }
    return -1;
}

// find the selected shape based on input coordinate
// return the index of the selected shape.
function selectedButtonIndex(buttons, clickX, clickY) {
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        if (button.testHit(clickX, clickY)) {
            return i;
        }
    }
    return -1;
}
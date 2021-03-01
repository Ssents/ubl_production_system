window.onload = function(){ 
    var form_1 = document.getElementById("Form1");
    var form_2 = document.getElementById("Form2");
    var form_3 = document.getElementById("Form3");

    var next_1 = document.getElementById("Next1");

    var back_2 = document.getElementById("Back2");
    var next_2 = document.getElementById("Next2");

    var back_3 = document.getElementById("Back3");
    var to_dashboard = document.getElementById("ToDashboard");

    next_1.onclick = function(){
        form_1.style.visibility = "hidden";
        form_2.style.visibility = "visible";
        form_3.style.visibility = "hidden";
    };

    back_2.onclick = function(){
        form_1.style.visibility = "visible";
        form_2.style.visibility = "hidden";
        form_3.style.visibility = "hidden";
    };

    next_2.onclick = function(){
        form_1.style.visibility = "hidden";
        form_2.style.visibility = "hidden";
        form_3.style.visibility = "visible";
    };

    back_3.onclick = function(){
        form_1.style.visibility = "hidden";
        form_2.style.visibility = "visible";
        form_3.style.visibility = "hidden";
    };


};
var production_type = document.getElementById("productionTypeValidation");
var production_bond = document.getElementById("productionBondValidation");

var order_number = document.getElementById("orderNumberValidation");
var work_order_number = document.getElementById("workOrderNumberValidation");

production_type.addEventListener("change", function(){
    if(production_type.value && production_bond.value){

        if (production_type.value == "Standard" && production_bond.value =="Local"){

            order_number.value = "UBL";
            work_order_number.value = "UBL";
        }
        else if (production_type.value == "Standard" && production_bond.value =="Export"){

            order_number.value = "Export";
            work_order_number.value = "Export";
        }
        else{
            order_number.value = "";
            work_order_number.value = "";


        }
    }
});


production_bond.addEventListener("change", function(){

    if(production_type.value && production_bond.value){

        if (production_type.value == "Standard" && production_bond.value =="Local"){

            order_number.value = "UBL";

            work_order_number.value = "UBL";

        }
        else if (production_type.value == "Standard" && production_bond.value =="Export"){

            order_number.value = "Export";


            work_order_number.value = "Export";

        }
        else{
            order_number.value = "";

            work_order_number.value = "";


        }
    }
});
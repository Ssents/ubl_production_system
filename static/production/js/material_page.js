
var order_id = document.getElementById("order-id").value;
// var material_id = document.getElementById("coil-id").innerHTML;

var home_url = $('.home-url').text();

var general_url = "http://127.0.0.1:8000/machines/";
var part_url = "create-material/";

var create_url = home_url + part_url;
console.log(home_url);


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var coil_id = "";
var coil_number = "";
var initial_mass = "";
$(".avaiableMaterial tbody").on("click", ".createMaterial", function(){
    coil_id = $(this).closest('tr').attr('id');
    console.log('coil id: ',coil_id);
    coil_number = $(this).closest('tr').find('.coilNumber').text();
    initial_mass = $(this).closest('tr').find('.initialMass').text();
    console.log('coil number: ', coil_number, 'initial mass: ', initial_mass);

    $("#createMaterialForm #inputCoilNumber").html(coil_number);
    $('#createMaterialForm #inputInitialMass').html(initial_mass);

});

$('#createMaterialForm').on("click", "#confirmAddMaterial", function(){
    const csrftoken = getCookie('csrftoken');
    var final_mass = $('#createMaterialForm #inputFinalMass').val();
    if (coil_id && coil_number && initial_mass && final_mass){
        
        $.ajax({
            url: create_url,
            headers: { "X-CSRFToken": csrftoken },
            data: {
                'order_id': order_id,
                'coil_number': coil_number,
                'initial_mass': initial_mass,
                'final_mass': final_mass
            },
            dataType: 'json',
            success: function (data) {
                appendToMaterialTable(data.material_data);
                
            }
        });
        }
    });

$("form#material-form").submit(function() {
    var coil_number = document.getElementById("coil-number").value;
    var initial_mass = document.getElementById("initial-mass").value;
    var final_mass =document.getElementById("final-mass").value;

    const csrftoken = getCookie('csrftoken');

    if(coil_number && initial_mass && final_mass){

        $.ajax({
            url: create_url,
            headers: { "X-CSRFToken": csrftoken },
            data: {
                'order_id': order_id,
                'coil_number': coil_number,
                'initial_mass': initial_mass,
                'final_mass': final_mass
            },
            dataType: 'json',
            success: function (data) {
                    appendToMaterialTable(data.material_data);
                
            }
        });
    }
    else {
        alert("All fields must have a valid value.");
    }
    $('form#material-form').trigger("reset");
    return false;
});


function appendToMaterialTable(material_data){
    var coil_id = material_data.material_id;
    var machine_id = material_data.machine_id;
    var part_url = machine_id + '/order/' + order_id + '/coil/' + coil_id + '/pieces/';

    var pieces_url = general_url + part_url;
    // console.log(pieces_url);
    var table_item = `<tr id="${coil_id}">
                            <td name="coil_number" data-bs-toggle="modal" 
                                data-bs-target="#editMaterialForm"
                                class="editMaterial"><span class="coilNumber" >${material_data.coil_number}</span>
                                <i class="fas fa-edit"></i>
                            </td>
                            <td name="initial_mass" class="initialMass">${material_data.initial_mass}</td>
                            <td name="final_mass" class="finalMass">${material_data.final_mass}</td>
                            <td class="options row">
                                <button type="button" class="btn btn-primary col-md-6 
                                    updatePieces  toPieces">
                                    <a href=${pieces_url}>Pieces</a>
                                </button>
                                <button type="button" class="btn btn-danger col-md-6 deleteMaterial" 
                                data-bs-toggle="modal" data-bs-target="#deleteMaterialForm">
                                    Delete
                                </button>
                            </td>		      
                        </tr>`;

    $("#material-table tbody").append(table_item);
}


$(".table tbody").on("click",".updatePieces", function(){
    var tr_item = $(this).closest('tr').attr('id');

    var currentRow = $(this).closest('tr');
    var piece_length=currentRow.find("td:eq(0)").text();
    var prime_pieces = currentRow.find("td:eq(1)").text();
    var rejects_pieces = currentRow.find("td:eq(2)").text();
});




var material_id = 0;
var coil_number = 0;

$(".table tbody").on("click",".deleteMaterial", function(){
    material_id = $(this).closest('tr').attr('id');
    coil_number = $(this).closest("tr").find(".coilNumber").html();
    // $("#modalCoilNumber").text(coil_number);
    // deleteMaterialAjax(material_id);
    console.log(`Delete material ${coil_number} ?`);
    $("#modalCoilNumber").text(coil_number);

});


$("#deleteMaterialForm").on("click","#deleteMaterialConfirm", function(){
    deleteMaterialAjax(material_id);  
    // $("#deleteMaterialConfirm").style.display = "hidden";
});

function deleteMaterialAjax(id) {
    var partial_delete_url = 'delete-material/';
    var delete_url = general_url + partial_delete_url;

      $.ajax({
          url: delete_url,
          data: {
              'material_id': id,
          },
          dataType: 'json',
          success: function (data) {
              if (data.deleted) {
                console.log("Ajax loads the remove function");
                $("tbody #" + id).remove();
                
                console.log("Ajax removes the data, ", "tbody #", id);

              }
          }
      });

}


var coil_id = "";
var coil_number = "";
var initial_mass = "";
var final_mass = "";



$(".table tbody").on("click", ".editMaterial",function(){
    coil_id = $(this).closest('tr').attr("id");
    coil_number = $(this).closest('tr').find(".coilNumber").html();
    initial_mass = $(this).closest('tr').find(".initialMass").html();
    final_mass = $(this).closest('tr').find(".finalMass").html();

    // transfer the figures to the modal
    $("#inputCoilNumber").val(coil_number);
    $("#inputInitialMass").val(initial_mass);
    $("#inputFinalMass").val(final_mass);

    
});

$("#editMaterialForm").on('click', '#confirmEditMaterial', function(){

    coil_number = $("#inputCoilNumber").val();
    initial_mass = $("#inputInitialMass").val();
    final_mass = $("#inputFinalMass").val();

    edit_coil_ajax(coil_number, initial_mass, final_mass, coil_id);

});




function edit_coil_ajax(edited_data){
    var partial_delete_url = 'edit-material/';
    var edit_url = general_url + partial_delete_url;
    if(coil_id && coil_number && final_mass && initial_mass){


        const csrftoken = getCookie('csrftoken');

        $.ajax({
            url: edit_url,
            headers: { "X-CSRFToken": csrftoken },
            data: {
                'coil_id': coil_id,
                'coil_number': coil_number,
                'initial_mass': initial_mass,
                'final_mass': final_mass
            },
            dataType: 'json',
            success: function (data) {

                var material_data=data.material_data;    

                $('#' + material_data.material_id).find(".coilNumber").text(material_data.coil_number);
                $('#' + material_data.material_id).find(".initialMass").text(material_data.initial_mass);
                $('#' + material_data.material_id).find(".finalMass").text(material_data.final_mass);

                console.log(material_data.coil_number, material_data.initial_mass,
                    material_data.final_mass);

   
            }
        });
    }
    else {
        alert("All fields must have a valid value.");
    }
}
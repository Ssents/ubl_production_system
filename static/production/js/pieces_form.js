var machine_id = document.getElementById("machine_id").innerHTML;
var order_id = document.getElementById("order-id").innerHTML;
var material_id = document.getElementById("coil-id").innerHTML;

var general_url = "http://127.0.0.1:8000/machines/";
var part_url = machine_id + "/order/" + order_id + "/coil/" + material_id + "/create-pieces";

create_order_url = general_url + part_url;

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

$("form#addPiece").submit(function() {
    var piece_length = document.getElementById("new-length").value;
    var prime_pieces = document.getElementById("new-prime").value;
    var rejects_pieces =document.getElementById("new-reject").value;

    const csrftoken = getCookie('csrftoken');

    if(piece_length && prime_pieces && rejects_pieces){

        $.ajax({
            url: create_order_url,
            headers: { "X-CSRFToken": csrftoken },
            data: {
                'piece_length': piece_length,
                'prime_pieces': prime_pieces,
                'reject_pieces': rejects_pieces
            },
            dataType: 'json',
            success: function (data) {
                if (data.piece) {
                  appendToPiecesTable(data.piece);
                }
            }
        });
    }
    else {
        alert("All fields must have a valid value.");
    }
    $('form#addPiece').trigger("reset");
    return false;
});


function appendToPiecesTable(piece_data){
    // piece_data.machine_id;
    
    var table_item = `<tr id="${piece_data.id}">
                            <td name="piece_length" class="piece-length">${piece_data.piece_length}</td>
                            <td name="prime_pieces" class="prime-pieces">${piece_data.prime_pieces}</td>
                            <td name="reject_pieces" class="reject-pieces">${piece_data.reject_pieces}</td>
                            <td>
                                <div class="row">
                                    <button type="button" class="btn btn-primary col-md-6 updatePieces"
                                        data-bs-toggle="modal" data-bs-target="#editPiecesForm">Edit</button>
                                    <button type="button" class="btn btn-danger col-md-6 deletePieces"
                                        data-bs-toggle="modal" data-bs-target="#deletePiecesForm">Delete</button>
                                </div>
                            </td>	      
                        </tr>`;

    $("#pieces-table tbody").append(table_item);
}



// $(".table tbody").on("click",".updatePieces", function(){
//     var tr_item = $(this).closest('tr').attr('id');

//     var currentRow = $(this).closest('tr');
//     var piece_length=currentRow.find("td:eq(0)").text();
//     var prime_pieces = currentRow.find("td:eq(1)").text();
//     var rejects_pieces = currentRow.find("td:eq(2)").text();

//     console.log(tr_item,piece_length, prime_pieces, rejects_pieces);
    



// });




var piece_id = 0;

$(".table tbody").on("click",".deletePieces", function(){
    piece_id = $(this).closest('tr').attr('id');
    console.log("row id is", piece_id);
    // deletePieceAjax(piece_id);

});

$('#deletePiecesForm').on('click', '#confirmDelete', function() {
   deletePieceAjax(piece_id);
});

function deletePieceAjax(id) {
    var partial_delete_url = 'piece/delete/';
    var delete_url = general_url + partial_delete_url;
    console.log(delete_url, " id=", id);
    // $('#deletePiecesForm').on('click', '#confirmDelete', function() {
        const csrftoken = getCookie('csrftoken');

        $.ajax({
            url: delete_url,
            headers: { "X-CSRFToken": csrftoken },
            data: {
                'coil_id': id,
            },
            dataType: 'json',
            success: function (data) {
                    $("#pieces-table #" + id).remove();
            }
      });
    // });
  }

var coil_id = "";
var material_id = "";
var machine_id = "";
var piece_id = "";

var piece_length = "";
var prime_pieces = "";
var rejects_pieces = "";

  $(".table tbody").on("click", ".updatePieces",function(){
    coil_id = $("#coil-id").text();
    piece_id = $(this).closest('tr').attr('id');
    material_id = $("#material-id").text();
    machine_id = $("#machine-id").text();

    
    piece_length = $(this).closest('tr').find(".piece-length").html();
    prime_pieces  = $(this).closest('tr').find(".prime-pieces").html();
    rejects_pieces = $(this).closest('tr').find(".reject-pieces").html();

    // transfer the figures to the modal
    $("#inputPieceLength").val(piece_length);
    $("#inputPrimePieces").val(prime_pieces);
    $("#inputRejectPieces").val(rejects_pieces);

    
});

$("#editPiecesForm").on('click', '#confirmEditPieces', function(){

    piece_length = $("#inputPieceLength").val();
    prime_pieces = $("#inputPrimePieces").val();
    rejects_pieces = $("#inputRejectPieces").val();

    edit_pieces_ajax(piece_id, piece_length, prime_pieces, rejects_pieces);

    // $('#editMaterialFormContent').trigger("reset");
});





function edit_pieces_ajax(edited_data){
    var partial_edit_url = 'piece/update/';
    var edit_url = general_url + partial_edit_url;
    if(piece_id && piece_length && prime_pieces && rejects_pieces){


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
        const csrftoken = getCookie('csrftoken');

        $.ajax({
            url: edit_url,
            headers: { "X-CSRFToken": csrftoken },
            data: {
                'updated_piece_length': piece_length,
                'updated_prime_pieces': prime_pieces,
                'updated_reject_pieces': rejects_pieces,
                'piece_id': piece_id,
                'order_id': order_id,
                'coil_id': coil_id,
            },
            dataType: 'json',
            success: function (data) {

                var piece_data=data.piece_data;    
                
                // $('#' + piece_data.piece_id).attr('id').text(piece_data.piece);
                $('#' + piece_data.piece_id).find(".piece-length").text(piece_data.piece_length);
                $('#' + piece_data.piece_id).find(".prime-pieces").text(piece_data.prime_pieces);
                $('#' + piece_data.piece_id).find(".reject-pieces").text(piece_data.reject_pieces);

                console.log(piece_data.piece_id,piece_data.piece_length, piece_data.prime_pieces,
                    piece_data.reject_pieces);

   
            }
        });
    }
    else {
        alert("All fields must have a valid value.");
    }
}